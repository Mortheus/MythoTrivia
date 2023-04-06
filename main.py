from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.button import Button
from kivymd.uix.button import MDRoundFlatButton
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.floatlayout import MDFloatLayout
from Player import Player
from android_permissions import AndroidPermissions
from database import Database
from emailslib import send_email_confirmation
import random
import functools
import sys
from photocamera import PhotoScreen
from kivy.core.window import Window
from swipescreen import SwipeScreen
from kivymd.app import MDApp

myDB = Database()
myDB.connect_to_db()

# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()


# class to build GUI for a popup window
class P(GridLayout):
    pass


def popFun():
    show = P()
    window = Popup(title="Please enter valid information", content=show,
                   size_hint=(None, None), size=(400, 400))
    window.open()


class LoginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    text = ""

    def validate(self):
        print(myDB.client.test2.users.find_one({"email": self.email.text}))
        if myDB.client.test2.users.find_one({"email": self.email.text, "password": self.pwd.text}):
            sm.get_screen("settings").ids['img'].source = myDB.client.test2.users.find_one({"email": self.email.text})["profile_pic"]
            sm.get_screen("cam").ids['img'].source = myDB.client.test2.users.find_one({"email": self.email.text})["profile_pic"]
            sm.get_screen("logdata").ids['username'].text = myDB.client.test2.users.find_one({"email": self.email.text})["name"]
            sm.get_screen("settings").ids['username'].text = myDB.client.test2.users.find_one({"email": self.email.text})["name"]
            sm.get_screen("categories").ids['username'].text = myDB.client.test2.users.find_one({"email": self.email.text})["name"]
            sm.get_screen("play").ids['username'].text = myDB.client.test2.users.find_one({"email": self.email.text})["name"]
            sm.get_screen("stats").ids['username'].text = myDB.client.test2.users.find_one({"email": self.email.text})["name"]
            sm.get_screen("update_user").ids['username'].text =  myDB.client.test2.users.find_one({"email": self.email.text})["name"]
            sm.current = 'logdata'
            LoginWindow.text = self.email.text
            self.email.text = ""
            self.pwd.text = ""

        else:
            print("NU")
            popFun()
            self.email.text = ""
            self.pwd.text = ""

    @classmethod
    def get_current_user(cls):
        return cls.text


    def clear_input(self):
        lista_input_text = [i for i in self.__dict__.values() if isinstance(i, TextInput)]
        for txt in lista_input_text:
            txt.text = ""

class SignupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):

        player = Player(self.name2.text, self.pwd.text, self.email.text)
        if self.email.text.endswith("@gmail.com"):
            send_email_confirmation(self.email.text)
            myDB.insert_doc_to_collection('test2', 'users', player)
        else:
            popFun()

        if self.email.text != "":
            sm.current = 'login'
            self.name2.text = ""
            self.email.text = ""
            self.pwd.text = ""
        else:
            popFun()



class MyGrid(Screen):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.points = 0
        self.questions = 0
        self.asked = []
        self.number = 0

    def first_question(self):
        print(CategoriesWindow.pass_category())
        if CategoriesWindow.pass_category() == 'norse':
            entries = list(myDB.client.questions.norse.find())
        elif CategoriesWindow.pass_category() == 'greek':
            entries = list(myDB.client.questions.greek.find())
        elif CategoriesWindow.pass_category() == 'roman':
            entries = list(myDB.client.questions.roman.find())
        elif CategoriesWindow.pass_category() == 'combined':
            entries = list(myDB.client.questions.combined.find())

        pick_one = random.choice(entries)
        self.asked.append(pick_one)
        self.label = Label(text=pick_one["question"], size_hint=(0.86, 0.30), pos_hint={'x': 0.08, 'y': 0.55})
        self.add_widget(self.label)
        self.score = Label(text="Score: 0", pos_hint={"center_x": .5, "center_y": .6})
        self.add_widget(self.score)

        self.buttons = [MDRoundFlatButton(text=f"[color=000000]{i+j}[/color]", md_bg_color= (1,1,1,1), line_color="black") for i, j in zip(["C. ", "A. ", "D. ", "B. "], [string for string in pick_one["answers"]])]
        [setattr(button, "pos_hint", {'x': i, 'y': j}) for button, i, j in zip(self.buttons, (0.045, 0.045, 0.55, 0.55), (0.26, 0.414, 0.26, 0.414))]
        [setattr(button, "size_hint", (i, j)) for button, i, j in zip(self.buttons, (0.410, 0.410, 0.410, 0.410), (0.083, 0.083, 0.083, 0.083))]
        [button.bind(on_press=self.validate_answer) for button in self.buttons]

        add_wid = lambda x: self.add_widget(x)
        for button in self.buttons:
            add_wid(button)

        self.generate = MDRoundFlatButton(text="[color=000000]Next[/color]", pos_hint={'center_x': 0.5, 'center_y': 0.1}, size_hint=(.3, .075), md_bg_color= (1,1,1,1), line_color="black", font_size="25sp")
        self.generate.bind(on_press=self.generate_question)
        self.add_widget(self.generate)

    def on_pre_enter(self):
        print(CategoriesWindow.pass_category())
        self.current_cat = CategoriesWindow.pass_category()
        self.first_question()

    def prepare_for_next(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            [setattr(button, 'md_bg_color', (1, 1, 1, 1)) for button in self.buttons]
            setattr(self.score, "text", self.score.text[:7] + str(self.points))
            func(self, *args, **kwargs)
            if self.questions > 5:
                print(LoginWindow.get_current_user())
                current_user = myDB.client.test2.users.find_one({"email": LoginWindow.get_current_user()})
                if CategoriesWindow.pass_category() == 'greek':
                    if current_user["highest_score_greek"] < self.points:
                        myDB.client.test2.users.update_one({"email": LoginWindow.get_current_user()}, {"$set": {"highest_score_greek": self.points}})
                elif CategoriesWindow.pass_category() == 'roman':
                    if current_user["highest_score_roman"] < self.points:
                        myDB.client.test2.users.update_one({"email": LoginWindow.get_current_user()}, {"$set": {"highest_score_roman": self.points}})
                elif CategoriesWindow.pass_category() == 'norse':
                    if current_user["highest_score_norse"] < self.points:
                        myDB.client.test2.users.update_one({"email": LoginWindow.get_current_user()}, {"$set": {"highest_score_norse": self.points}})
                elif CategoriesWindow.pass_category() == 'combined':
                    if current_user["highest_score_combined"] < self.points:
                        myDB.client.test2.users.update_one({"email": LoginWindow.get_current_user()}, {"$set": {"highest_score_combined": self.points}})
                self.questions = 0
                self.points = 0
                self.asked = []
                self.number += 1
                myDB.client.test2.users.update_one({"email": LoginWindow.get_current_user()},
                                                   {"$set": {"games_played": self.number}})

                setattr(self.label, "text", "")
                for button in self.buttons:
                    setattr(button, "text", "")
                setattr(self.score, "text", "")
                sm.current = "logdata"

        return inner

    def get_button_list(self):
        return self.buttons

    @prepare_for_next
    def generate_question(self, instance):
        if self.current_cat == 'norse':
            entries = list(myDB.client.questions.norse.find())
        elif self.current_cat == 'greek':
            entries = list(myDB.client.questions.greek.find())
        elif self.current_cat == 'roman':
            entries = list(myDB.client.questions.roman.find())
        elif self.current_cat == 'combined':
            entries = list(myDB.client.questions.combined.find())
        pick = random.choice(entries)
        while pick in self.asked:
            print(pick)
            pick = random.choice(entries)
        self.asked.append(pick)
        setattr(self.label, "text", pick["question"])
        [setattr(button, "text", f"[color=000000]{i+j}[/color]") for button, i, j in zip(self.buttons, ["C. ", "A. ", "D. ", "B. "], [string for string in pick["answers"]])]
        self.questions += 1


    def validate_answer(self, instance):
        if self.current_cat == 'norse':
            quest = myDB.client.questions.norse.find_one({"question": self.label.text})
        elif self.current_cat == 'greek':
            quest = myDB.client.questions.greek.find_one({"question": self.label.text})
        elif self.current_cat == 'roman':
            quest = myDB.client.questions.roman.find_one({"question": self.label.text})
        elif self.current_cat == 'combined':
            quest = myDB.client.questions.combined.find_one({"question": self.label.text})
        if instance.text[17:-8] == quest["correct_answer"]:
            setattr(instance, 'md_bg_color', (0, 1, 0, 1))
            self.points += quest["points"]
        else:
            setattr(instance, 'md_bg_color', (1, 0, 0, 1))



class LogDataWindow(Screen):
    pass


class CategoriesWindow(Screen):
    selected_category = ""
    def on_pre_enter(self):
        self.find_category()

    def find_category(self):
        button_list = [sm.get_screen("categories").ids['greek'], sm.get_screen("categories").ids['roman'], sm.get_screen("categories").ids['norse'], sm.get_screen("categories").ids['combined']]
        for button in button_list:
            button.my_id = button.text
            button.bind(on_press=self.get_category)

    def get_category(self, instance):
        print(str(instance.my_id)[14:-8])
        CategoriesWindow.selected_category = str(instance.my_id)[14:-8].lower()


    @classmethod
    def pass_category(cls):
        return cls.selected_category



class ProfilePicture(Screen):


    def upload(self):
        path = Storage.get_path()
        self.ids.img.source = path
        sm.get_screen('settings').ids['img'].source = path
        sm.get_screen("cam").ids['img'].source = path
        myDB.client.test2.users.update_one({"email": LoginWindow.get_current_user()}, {"$set": {"profile_pic": path}})
        current_user = myDB.client.test2.users.find_one({"email": LoginWindow.get_current_user()})
        print(current_user)


    @classmethod
    def load_image(cls):
        user = LoginWindow.get_current_user()
        current_user = myDB.client.test2.users.find_one({"email": user})

class ProfileSettings(Screen):
    pass
class WindowManager(ScreenManager):
    pass

class Storage(SwipeScreen):

    @classmethod
    def selected(cls, filename):
        try:
            cls.path = filename[0]
            print(cls.path)
        except IndexError:
            sm.current = 'logdata'

    def preview_image(self, filename):
        Storage.selected(filename)
        self.ids.my_image.source = Storage.path

    @classmethod
    def get_path(cls):
        imag = cls.path
        return imag

class ChangePicture(Screen):
    def upload(self):
        if hasattr(Storage, "path"):
            path = Storage.get_path()
            self.ids.img.source = path

            sm.get_screen("settings").ids['img'].source = path
            myDB.client.test2.users.update_one({"email": LoginWindow.get_current_user()}, {"$set": {"profile_pic": path}})
            current_user = myDB.client.test2.users.find_one({"email": LoginWindow.get_current_user()})
            print(current_user)
        else:
            sm.current = 'settings'

    @classmethod
    def load_image(cls):
        user = LoginWindow.get_current_user()
        current_user = myDB.client.test2.users.find_one({"email": user})

class Statistics(Screen):
    def update_category(self, instance):
        text = instance.text[14:-8].lower()
        current_user = myDB.client.test2.users.find_one({"email": LoginWindow.get_current_user()})
        if text == "greek":
            self.ids['highest'].text = self.ids['highest'].text[:18]
            self.ids['highest'].text += str(current_user['highest_score_greek'])
            self.ids['played'].text = self.ids['played'].text[:24]
            self.ids['played'].text += str(current_user['games_played'])
        elif text == "roman":
            self.ids['highest'].text = self.ids['highest'].text[:18]
            self.ids['highest'].text += str(current_user['highest_score_roman'])
            self.ids['played'].text = self.ids['played'].text[:24]
            self.ids['played'].text += str(current_user['games_played'])
        elif text == "norse":
            self.ids['highest'].text = self.ids['highest'].text[:18]
            self.ids['highest'].text += str(current_user['highest_score_norse'])
            self.ids['played'].text = self.ids['played'].text[:24]
            self.ids['played'].text += str(current_user['games_played'])
        elif text == "combined":
            self.ids['highest'].text = self.ids['highest'].text[:18]
            self.ids['highest'].text += str(current_user['highest_score_combined'])
            self.ids['played'].text = self.ids['played'].text[:24]
            self.ids['played'].text += str(current_user['games_played'])

class ForgotPassword(Screen):
    def reset(self):
        myDB.client.test2.users.update_one({'email': self.ids['email'].text}, {"$set": {"password": self.ids['pwd'].text}})
        sm.current = 'login'
sm = WindowManager()

class UpdateSettings(Screen):
    def update(self):
        current_user = myDB.client.test2.users.find_one({"email": LoginWindow.get_current_user()})
        if self.ids['user'].text == "" and self.ids['pwd'].text == "":
            sm.current = 'settings'

        elif self.ids['user'].text and self.ids['pwd'].text == "":
            myDB.client.test2.users.update_one({'email': LoginWindow.get_current_user()}, {"$set": {'name': self.ids['user'].text}})
            sm.current = 'settings'

        elif self.ids['user'].text == "" and self.ids['pwd'].text:
            myDB.client.test2.users.update_one({'email': LoginWindow.get_current_user()}, {"$set": {'password': self.ids['pwd'].text}})
            sm.current = 'settings'
        else:
            print("Nu am intrat in ifu-ri")


if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity

    View = autoclass('android.view.View')


    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread
        # so use Window.width and Window.height
        if Window.width > Window.height:
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config

    Config.set('input', 'mouse', 'mouse, disable_multitouch')

class loginMain(MDApp):
    def build(self):
        kv = Builder.load_file('loginMain.kv')
        # sm = WindowManager()

        sm.add_widget(LoginWindow(name='login'))
        sm.add_widget(SignupWindow(name='signup'))
        sm.add_widget(LogDataWindow(name='logdata'))
        sm.add_widget(MyGrid(name='play'))
        sm.add_widget(PhotoScreen(name='photo'))
        sm.add_widget(ProfilePicture(name='profile'))
        sm.add_widget(Storage(name="storage"))
        sm.add_widget(CategoriesWindow(name="categories"))
        sm.add_widget(ProfileSettings(name='settings'))
        sm.add_widget(ChangePicture(name="cam"))
        sm.add_widget(Statistics(name="stats"))
        sm.add_widget(ForgotPassword(name="forgot"))
        sm.add_widget(UpdateSettings(name="update_user"))

        self.enable_swipe = False
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)
        return sm

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
        self.enable_swipe = True

    def swipe_screen(self, right):
        if self.enable_swipe:
            if right:
                sm.transition.direction='right'
                sm.current = "cam"
            else:
                sm.tranistion.direction='left'
                sm.current = 'settings'

if __name__ == "__main__":
    loginMain().run()
