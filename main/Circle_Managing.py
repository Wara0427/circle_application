import sqlite3

DB_name = 'circle_member.db'

#DBの初回起動
def start_db():
    #DBの作成
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()
    #テーブル作成（id, name, university, faculty, department, entry_year, grade, gender）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            university TEXT,
            faculty TEXT,
            department TEXT,
            entry_year INTEGER,
            grade INTEGER,
            gender TEXT
        )
    ''')

    #カレンダーのテーブル作成（id, date, title, details）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            details TEXT
        )
    ''')
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

def search_member(member_name):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    #同じ名前のメンバーが既に存在するかどうかを確認
    cursor.execute('SELECT id FROM members WHERE name = ?', (member_name,))

    #検索結果を1件取得する
    existing_member = cursor.fetchone() 

    if existing_member is None:
        flag=0
    else:
        flag=1

    return flag

def add_member(member_data):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    #同じ名前のメンバーが既に存在するかどうかを確認
    cursor.execute('SELECT id FROM members WHERE name = ?', (member_data['name'],))
    
    #検索結果を1件取得する
    existing_member = cursor.fetchone() 

    #登録したいメンバーが存在しなければ追加
    if existing_member is None:
        cursor.execute('''
                   INSERT INTO members (name, university, faculty, department, entry_year, grade, gender)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ''', (member_data['name'], member_data['university'], member_data['faculty'], member_data['department'],
                   member_data['entry_year'], member_data['grade'], member_data['gender'])
                   )
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

#メンバー一覧リストの取得
def get_members_list():
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM members')
    
    conn.commit() # 変更を確定
    members=cursor.fetchall() #変更点（戻り値の取得）
    conn.close()  # 接続を閉じる
    return members #変更点（戻り値）

#メンバー削除
def delete_member(member_name):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    cursor.execute('DELETE FROM members WHERE name = ?' , (member_name,))
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

#メンバー更新
def update_member(member_name, update_grade):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    cursor.execute('UPDATE members SET grade = ? WHERE name = ?' , (update_grade, member_name,))
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

#予定を追加
def add_schedule(activity_data):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()
    #指定した日に予定を追加
    cursor.execute('''
                   INSERT INTO activity_calendar (date, title, details)
                   VALUES (?, ?, ?)
                   ''', (activity_data['date'], activity_data['title'], activity_data['details'])
                   )
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

#予定を更新
def update_schedule(date, new_title, new_details, target_activity_order):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    #該当日の予定を検索
    cursor.execute('SELECT id FROM activity_calendar WHERE date = ?', (date,))
    
    #検索結果をすべて取得
    activities_in_calendar = cursor.fetchall() 

    #予定が存在すれば更新
    if len(activities_in_calendar) != 0:
        temp_id = activities_in_calendar[target_activity_order % len(activities_in_calendar)][0] #予定を識別する
        cursor.execute('UPDATE activity_calender SET title = ?, details = ? WHERE id = ?' , (new_title, new_details ,temp_id,))
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

＃予定を削除
def delete_schedule(date, target_activity_order):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    #該当日の予定を検索
    cursor.execute('SELECT id FROM activity_calendar WHERE date = ?', (date,))
    
    #検索結果をすべて取得
    activities_in_calendar = cursor.fetchall() 

    #予定が存在すれば削除
    if len(activities_in_calendar) != 0:
        temp_id = activities_in_calendar[target_activity_order % len(activities_in_calendar)][0] #予定を識別する
        cursor.execute('DELETE FROM activity_calender WHERE id = ?' , (temp_id,))

    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

#年月からその月の予定をすべて取得
def get_schedule(year, month):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    num_of_dates = calendar.monthrange(year, month)[1] #日数を取得
    schedules = []
    for day in range(1, num_of_dates + 1): #その月の日数分だけ総当たりする
        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        cursor.execute('SELECT title, details FROM activity_calendar WHERE date = ?', (date_str,))
        day_schedules = cursor.fetchall()
        if day_schedules:  #予定があれば保存
            schedules.append((date_str, day_schedules))
    
    conn.close() # 接続を閉じる
    return schedules

start_db()

taitai_data = {'name' : 'taiki', 'university' : 'Doshisha', 'faculty' : 'Sci and Eng', 'department' : 'Information', 
               'entry_year' : 2023, 'grade' : 3, 'gender' : 'Man'}
test_member = {
         'name': '鈴木 一郎', 'university': '〇〇大学', 'faculty': '△△学部', 
         'department': '××学科', 'entry_year': 2023, 'grade': 2, 'gender': '男性'
     }

add_member(taitai_data)
add_member(test_member)

#delete_member(taitai_data)
#update_member(test_member, 3)

get_members_list()





