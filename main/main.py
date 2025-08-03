from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

# kvファイルの<~Screen>とつながる
class MenuScreen(Screen): pass
class MemberScreen(Screen): 
    def AddMember(self): pass #あとで作る
class CalenderScreen(Screen): pass

class MyApp(App):
    def build(self):
        # main.kv を読み込む
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    MyApp().run()
