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
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

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
    conn.close()  # 接続を閉じる

#メンバー削除
def delete_member(member_data):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    cursor.execute('DELETE FROM members WHERE name = ?' , (member_data['name'],))
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

#メンバー更新
def update_member(member_data, update_grade):
    #DBへの接続
    conn = sqlite3.connect(DB_name)
    #オブジェクト作成
    cursor = conn.cursor()

    cursor.execute('UPDATE members SET grade = ? WHERE name = ?' , (update_grade, member_data['name'],))
    
    conn.commit() # 変更を確定
    conn.close()  # 接続を閉じる

start_db()

taitai_data = {'name' : 'taiki', 'university' : 'Doshisha', 'faculty' : 'Sci and Eng', 'department' : 'Information', 
               'entry_year' : 2023, 'grade' : 3, 'gender' : 'Man'}
test_member = {
         'name': '鈴木 一郎', 'university': '〇〇大学', 'faculty': '△△学部', 
         'department': '××学科', 'entry_year': 2023, 'grade': 2, 'gender': '男性'
     }

add_member(taitai_data)
#add_member(test_member)

#delete_member(taitai_data)
#update_member(test_member, 3)
get_members_list()