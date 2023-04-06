import sys
import time

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from database import Database
from kivy.uix.label import Label
import random
import functools
from kivy.core.window import Window
from kivy.graphics import *

from question import Question


db = Database()
db.connect_to_db()


# class MyGrid(GridLayout):
#     def __init__(self, **kwargs):
#         super(MyGrid, self).__init__(**kwargs)
#         self.cols = 2
#         self.points = 0
#         self.questions = 0
#         entries = list(db.client.test.questions.find())
#         pick_one = random.choice(entries)
#
#         self.label = Label(text=pick_one["question"])
#         self.add_widget(self.label)
#         self.score = Label(text="Score: 0")
#         self.add_widget(self.score)
#
#         self.buttons = [Button(text=i+j) for i, j in zip(["A. ", "B. ", "C. ", "D. "], [string for string in pick_one["answers"]])]
#         [button.bind(on_press=self.validate_answer) for button in self.buttons]
#
#         add_wid = lambda x: self.add_widget(x)
#         for button in self.buttons:
#             add_wid(button)
#
#         self.generate = Button(text="Next")
#         self.generate.bind(on_press=self.generate_question)
#         self.add_widget(self.generate)
#
#     def prepare_for_next(func):
#         @functools.wraps(func)
#         def inner(self, *args, **kwargs):
#             [setattr(button, 'background_color', (1, 1, 1, 1)) for button in self.buttons]
#             setattr(self.score, "text", self.score.text[:7] + str(self.points))
#             func(self, *args, **kwargs)
#             if self.questions > 3:
#                 print("ar trebui sa stop")
#                 sys.exit()
#
#         return inner
#
#     def get_button_list(self):
#         return self.buttons
#
#     @prepare_for_next
#     def generate_question(self, instance):
#         entries = list(db.client.test.questions.find())
#         pick = random.choice(entries)
#         setattr(self.label, "text", pick["question"])
#         [setattr(button, "text", i+j) for button, i, j in zip(self.buttons, ["A. ", "B. ", "C. ", "D. "], [string for string in pick["answers"]])]
#         self.questions += 1
#         print(self.questions)
#
#     def validate_answer(self, instance):
#         quest = db.client.test.questions.find_one({"question": self.label.text})
#         if instance.text[3:] == quest["correct_answer"]:
#             setattr(instance, 'background_color', (0, 1, 0, 1))
#             self.points += quest["points"]
#         else:
#             setattr(instance, 'background_color', (1, 0, 0, 1))
#


# class MyGrid(Screen):
#     def __init__(self, **kwargs):
#         super(MyGrid, self).__init__(**kwargs)
#         self.points = 0
#         self.questions = 0
#         # self.canvas.add(Rectangle(size_hint=(1, 1), pos_hint={'x': 1, 'y': 1}))
#         # setattr(self, 'background_color', (1, 0, 0, 1))
#         # Window.clearcolor = (1, 1, 1, 1)
#         entries = list(db.client.test.questions.find())
#         pick_one = random.choice(entries)
#
#         self.label = Label(text=pick_one["question"], size_hint=(0.86, 0.30), pos_hint={'x': 0.08, 'y': 0.55})
#         self.add_widget(self.label)
#         self.score = Label(text="Score: 0")
#         self.add_widget(self.score)
#
#         self.buttons = [Button(text=i+j) for i, j in zip(["A. ", "B. ", "C. ", "D. "], [string for string in pick_one["answers"]])]
#         [setattr(button, "pos_hint", {'x': i, 'y': j}) for button, i, j in zip(self.buttons, (0.045, 0.045, 0.55, 0.55), (0.26, 0.414, 0.26, 0.414))]
#         [setattr(button, "size_hint", (i, j)) for button, i, j in zip(self.buttons, (0.410, 0.410, 0.410, 0.410), (0.083, 0.083, 0.083, 0.083))]
#         [button.bind(on_press=self.validate_answer) for button in self.buttons]
#
#         add_wid = lambda x: self.add_widget(x)
#         for button in self.buttons:
#             add_wid(button)
#
#         self.generate = Button(text="Next", pos_hint={'x': 0.35, 'y': 0.125}, size_hint=(.3, .075))
#         self.generate.bind(on_press=self.generate_question)
#         self.add_widget(self.generate)
#
#     def prepare_for_next(func):
#         @functools.wraps(func)
#         def inner(self, *args, **kwargs):
#             [setattr(button, 'background_color', (1, 1, 1, 1)) for button in self.buttons]
#             setattr(self.score, "text", self.score.text[:7] + str(self.points))
#             func(self, *args, **kwargs)
#             if self.questions > 3:
#                 print("ar trebui sa stop")
#                 sys.exit()
#
#         return inner
#
#     def get_button_list(self):
#         return self.buttons
#
#     @prepare_for_next
#     def generate_question(self, instance):
#         entries = list(db.client.test.questions.find())
#         pick = random.choice(entries)
#         setattr(self.label, "text", pick["question"])
#         [setattr(button, "text", i+j) for button, i, j in zip(self.buttons, ["A. ", "B. ", "C. ", "D. "], [string for string in pick["answers"]])]
#         self.questions += 1
#         print(self.questions)
#
#     def validate_answer(self, instance):
#         quest = db.client.test.questions.find_one({"question": self.label.text})
#         if instance.text[3:] == quest["correct_answer"]:
#             setattr(instance, 'background_color', (0, 1, 0, 1))
#             self.points += quest["points"]
#         else:
#             setattr(instance, 'background_color', (1, 0, 0, 1))
#
#
#
# class MyApp(App):
#     def build(self):
#         return MyGrid()
#
#
# if __name__ == "__main__":
#     MyApp().run()
#     entries = db.client.test.questions.find()
#     entry_list = list(entries)
#     # for entry in entries:
#     #     print(entry)
#     print(random.choice(entry_list))

# import numpy as np
# import cv2
#
#
# cap = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = cap.read()
#     cv2.imshow('frame', frame)
#
#     if cv2.waitKey(1) == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from android.permissions import request_permissions, Permission
import time

request_permissions([
    Permission.CAMERA,
    Permission.WRITE_EXTERNAL_STORAGE,
    Permission.READ_EXTERNAL_STORAGE
])

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        # resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class TestCamera(App):

    def build(self):
        request_permissions()
        return CameraClick()


TestCamera().run()