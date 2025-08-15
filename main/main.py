from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color,Rectangle
from Circle_Managing import *
import calendar
from datetime import datetime,timedelta

# メッセージを表示（実行時、エラー時）
def show_popup(message):
    layout=BoxLayout(orientation='vertical',padding=10,spacing=10)
    show_word=Label(text=message,color=(0,0,0,1),font_name="fonts/meiryo.ttc")
    close_btn=Button(text="閉じる",size_hint=(1, 0.3),color=(1,1,1,1),background_normal="",background_color=(0.8,0.3,0.3,1),font_name="fonts/meiryo.ttc")

    popup=Popup(title="",separator_height=0,content=layout,size_hint=(None,None),size=(600,400),background="",background_color=(1,1,1,1))

    close_btn.bind(on_release=popup.dismiss)

    layout.add_widget(show_word)
    layout.add_widget(close_btn)

    popup.open()

# 入力をクリア（名簿追加時）
def reset_data(self):
    self.ids.name_input.text=""
    self.ids.university_input.text=""
    self.ids.faculty_input.text=""
    self.ids.department_input.text=""
    self.ids.entry_year_input.text=""
    self.ids.grade_input.text=""
    self.ids.gender_input.text=""

# kvファイルの<~Screen>とつながる
class MenuScreen(Screen): pass
class MemberScreen(Screen):
    # 表示する際自動的に更新
    def on_enter(self):
        self.members=get_members_list()
        self.show_header()
        self.show_members()

    def show_header(self):
        member_h=self.ids.members_header
        member_h.clear_widgets()

        header=["氏名","大学名","学部","学科","入学年度","学年","性別"]

        for h in header:
            member_h.add_widget(Label(text=h,color=(0,0,0,1),font_name="fonts/meiryo.ttc"))

    # メンバーの表示
    def show_members(self):
        member_obj=self.ids.members_object
        member_obj.clear_widgets()

        for member in self.members:
            _,name,university,faculty,department,entry_year,grade,gender=member

            row=BoxLayout(orientation='horizontal',size_hint_y=None,height=30)

            row.add_widget(Label(text=str(name), color=(0,0,0,1),font_name="fonts/meiryo.ttc"))
            row.add_widget(Label(text=str(university), color=(0,0,0,1),font_name="fonts/meiryo.ttc"))
            row.add_widget(Label(text=str(faculty), color=(0,0,0,1),font_name="fonts/meiryo.ttc"))
            row.add_widget(Label(text=str(department), color=(0,0,0,1),font_name="fonts/meiryo.ttc"))
            row.add_widget(Label(text=str(entry_year), color=(0,0,0,1),font_name="fonts/meiryo.ttc"))
            row.add_widget(Label(text=str(grade), color=(0,0,0,1),font_name="fonts/meiryo.ttc"))
            row.add_widget(Label(text=str(gender), color=(0,0,0,1),font_name="fonts/meiryo.ttc"))

            member_obj.add_widget(row)

class AddMemberScreen(Screen):

    def do_add(self,new_name,new_university,new_faculty,new_department,new_entry_year,new_grade,new_gender):

        # エラー処理
        error_list=[]
        labels = ["名前", "大学名", "学部", "学科", "入学年度", "学年", "性別"]
        values = [new_name, new_university, new_faculty, new_department, new_entry_year, new_grade, new_gender]

        for i in range(len(values)):
            if values[i] is None or values[i] == "":
                error_list.append(labels[i])

        if error_list:
            show_popup("以下を入力してください：\n" + "\n".join(error_list))
            return
        
        # データベースに追加するデータ
        new_member_data={'name': new_name, 'university': new_university, 'faculty': new_faculty, 
         'department': new_department, 'entry_year': new_entry_year, 'grade': new_grade, 'gender': new_gender
        }

        add_member(new_member_data)
        show_popup("追加完了しました！")
        reset_data(self)

class UpdateMemberScreen(Screen): pass
class DeleteMemberScreen(Screen):
        def do_delete(self,delete_name):
            delete_member(delete_name)
            show_popup("削除完了しました！")
            reset_data_del(self)
    
class CalendarScreen(Screen):
    # 初期化
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.today=datetime.today()
        self.current_year=self.today.year
        self.current_month=self.today.month

    # 表示する際自動的に更新
    def on_enter(self):
        self.update_calendar()
    
    # kvに返す
    def get_month_year(self):
        return f"{self.current_year}年{self.current_month}月"
    
    # 前の月に移動する処理
    def prev_month(self):
        if self.current_month==1:
            self.current_month=12
            self.current_year-=1

        else:
            self.current_month-=1

        self.update_calendar()
    
    # 次の月に移動する処理
    def next_month(self):
        if self.current_month==12:
            self.current_month=1
            self.current_year+=1
        
        else:
            self.current_month+=1

        self.update_calendar()

    # グラフの概形（サイズや罫線など）
    def make_cell(self, text, text_color, bg_color):
        wrapper = BoxLayout(padding=1)  
        border_color=(0,0,0,1)

        with wrapper.canvas.before:
            Color(*border_color)  
            rect = Rectangle(pos=wrapper.pos, size=wrapper.size)

    
        def update_rect(*args):
            rect.pos = wrapper.pos
            rect.size = wrapper.size
        wrapper.bind(pos=update_rect, size=update_rect)

        btn = Button(
            text=text,
            color=text_color,
            background_color=bg_color,
            background_normal='',
            font_name="fonts/meiryo.ttc",
        )
        wrapper.add_widget(btn)
        return wrapper
    
    # カレンダーの中身を作成
    def update_calendar(self):
        header=self.ids.calendar_header
        grid=self.ids.calendar_grid
        header.clear_widgets()
        grid.clear_widgets()

        # 曜日ヘッダ
        weekday=["日","月","火","水","木","金","土"]
        for i,w in enumerate(weekday):
            if i == 0:  
                color = (1, 0, 0, 1)  
            elif i == 6:  
                color = (0, 0, 1, 1)  
            else:
                color = (0, 0, 0, 1)  
            header.add_widget(Button(text=w, color=color, background_color=(0.9, 0.9, 0.9, 1),background_normal='',size_hint_y=None,height=40,font_name="fonts/meiryo.ttc"))

        month_days = calendar.monthcalendar(self.current_year, self.current_month)
        for week in month_days:
            for i,day in enumerate(week):
                if day == 0:
                    grid.add_widget(self.make_cell("", (0, 0, 0, 1), (1, 1, 1, 1)))  
                else:
                    if i == 0:
                        color = (1, 0, 0, 1)  # 日曜
                    elif i == 6:
                        color = (0, 0, 1, 1)  # 土曜
                    else:
                        color = (0, 0, 0, 1)
                    grid.add_widget(self.make_cell(str(day), color, (1, 1, 1, 1)))
        
        self.ids.month_label.text = self.get_month_year()




class MyApp(App):
    def build(self):
        # main.kv を読み込む
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    start_db()
    MyApp().run()



