from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
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
    window = Popup(title="popup", content=show,
                   size_hint=(None, None), size=(300, 300))
    window.open()


class playWindow(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.inside = FloatLayout()
        entries = myDB.client.test.questions.find_one()
        self.label = Label(text=entries["question"])
        self.add_widget(self.label)
        buttons = [Button(text=i+j) for i, j in zip(["A. ", "B. ", "C. ", "D. "], [string for string in entries["answers"]])]
        [button.bind(on_press=self.validate_answer) for button in buttons]
        add_wid = lambda x: self.inside.add_widget(x)
        for button in buttons:
            add_wid(button)
        print(buttons)

    def validate_answer(self, instance):
        quest = myDB.client.test.questions.find_one({"question": self.label.text})
        if instance.text[3:] == quest["correct_answer"]:
            setattr(instance, 'background_color', (0, 1, 0, 1))
        else:
            setattr(instance, 'background_color', (1, 0, 0, 1))

class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def validate(self):
        if myDB.client.test2.users.find_one({"email": self.email.text, "password": self.pwd.text}):
            sm.current = 'logdata'
            self.email.text = ""
            self.pwd.text = ""

        else:
            print("NU")
            popFun()
            self.email.text = ""
            self.pwd.text = ""


    def clear_input(self):
        """
        imi fac o lista cu obiectele care sunt de tip TextInput
        lista obtinuta din dict atribut: valoare a clasei de baza
        dupa le setez atributul de .text pe "", ca sa dispara din widget
        """
        lista_input_text = [i for i in self.__dict__.values() if isinstance(i, TextInput)]
        for txt in lista_input_text:
            txt.text = ""


class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):

        player = Player(self.name2.text, self.pwd.text, self.email.text)
        myDB.insert_doc_to_collection('test2', 'users', player)
        send_email_confirmation(self.email.text)

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
        # self.canvas.add(Rectangle(size_hint=(1, 1), pos_hint={'x': 1, 'y': 1}))
        # setattr(self, 'background_color', (1, 0, 0, 1))
        # Window.clearcolor = (1, 1, 1, 1)
        entries = list(myDB.client.test.questions.find())
        pick_one = random.choice(entries)

        self.label = Label(text=pick_one["question"], size_hint=(0.86, 0.30), pos_hint={'x': 0.08, 'y': 0.55})
        self.add_widget(self.label)
        self.score = Label(text="Score: 0")
        self.add_widget(self.score)

        self.buttons = [Button(text=i+j) for i, j in zip(["A. ", "B. ", "C. ", "D. "], [string for string in pick_one["answers"]])]
        [setattr(button, "pos_hint", {'x': i, 'y': j}) for button, i, j in zip(self.buttons, (0.045, 0.045, 0.55, 0.55), (0.26, 0.414, 0.26, 0.414))]
        [setattr(button, "size_hint", (i, j)) for button, i, j in zip(self.buttons, (0.410, 0.410, 0.410, 0.410), (0.083, 0.083, 0.083, 0.083))]
        [button.bind(on_press=self.validate_answer) for button in self.buttons]

        add_wid = lambda x: self.add_widget(x)
        for button in self.buttons:
            add_wid(button)

        self.generate = Button(text="Next", pos_hint={'x': 0.35, 'y': 0.125}, size_hint=(.3, .075))
        self.generate.bind(on_press=self.generate_question)
        self.add_widget(self.generate)

    def prepare_for_next(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            [setattr(button, 'background_color', (1, 1, 1, 1)) for button in self.buttons]
            setattr(self.score, "text", self.score.text[:7] + str(self.points))
            func(self, *args, **kwargs)
            if self.questions > 3:
                print("ar trebui sa stop")
                sm.current = "logdata"

        return inner

    def get_button_list(self):
        return self.buttons

    @prepare_for_next
    def generate_question(self, instance):
        entries = list(myDB.client.test.questions.find())
        pick = random.choice(entries)
        setattr(self.label, "text", pick["question"])
        [setattr(button, "text", i+j) for button, i, j in zip(self.buttons, ["A. ", "B. ", "C. ", "D. "], [string for string in pick["answers"]])]
        self.questions += 1
        print(self.questions)

    def validate_answer(self, instance):
        quest = myDB.client.test.questions.find_one({"question": self.label.text})
        if instance.text[3:] == quest["correct_answer"]:
            setattr(instance, 'background_color', (0, 1, 0, 1))
            self.points += quest["points"]
        else:
            setattr(instance, 'background_color', (1, 0, 0, 1))


class logDataWindow(Screen):
    pass


class ProfilePicture(Screen):
    def upload(self):
        self.ids.img.source = Storage.get_path()


class windowManager(ScreenManager):
    pass


class Storage(SwipeScreen):

    @classmethod
    def selected(cls, filename):
        cls.path = filename[0]
        print(cls.path)

    def preview_image(self, filename):
        Storage.selected(filename)
        self.ids.my_image.source = Storage.path

    @classmethod
    def get_path(cls):
        imag = cls.path
        print(cls.path)
        return imag


kv = Builder.load_file('loginMain.kv')
sm = windowManager()


sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(MyGrid(name='play'))
sm.add_widget(PhotoScreen(name='photo'))
sm.add_widget(ProfilePicture(name='profile'))
sm.add_widget(Storage(name="storage"))


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

class loginMain(App):
    def build(self):
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
                sm.current = "profile"

if __name__ == "__main__":
    loginMain().run()
