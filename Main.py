import webbrowser
import googletrans
import cv2
import gtts
import playsound
import pyttsx3
import wikipedia
from Jarvis import JarvisAssistant
import re
import os
import random
import pprint
import datetime
import speech_recognition as sr
import requests
import sys
import urllib.parse
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
import socket
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config

obj = JarvisAssistant()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices');
# print(voices[0].id)
engine.setProperty('voices', voices[len(voices) - 1].id)

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["hello", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["always there for you Diya", "i am ready Diya",
                 "your wish my command Diya", "how can i help you Diya?", "i am online and ready Diya"]

EMAIL_DIC = {
    'myself': 'atharvaaingle@gmail.com',
    'my official email': 'atharvaaingle@gmail.com',
    'my second email': 'atharvaaingle@gmail.com',
    'my official mail': 'atharvaaingle@gmail.com',
    'my second mail': 'atharvaaingle@gmail.com'
}

CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]


# =======================================================================================================================================================

# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# To convert voice into text

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query


# for news updates
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey="YOUR_API_HERE"'

    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")


def translate():
    recognizer = sr.Recognizer()
    translator = googletrans.Translator()
    in_lan = 'hi'
    out_lan = 'en'
    try:
        with sr.Microphone() as source:
            print('Ready...')
            voice = recognizer.listen(source)
            text = recognizer.recognize_google(voice, language=in_lan)
            print(text)
    except:
        pass

    translated = translator.translate(text, dest=out_lan)
    print(translated.text)
    return translated.text


app_id = config.wolframalpha_id


def computational_intelligence(question):
    try:
        client = wolframalpha.Client(app_id)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        return None


def startup():
    speak("All systems have been activated")


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")
    speak("I am Jarvis. Online and ready Diya. Please tell me how may I help you")


# if __name__ == "__main__":


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        startup()
        wish()

        while True:
            query = takecommand().lower()
            if "open notepad" in query:
                npath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            elif 'hi' in query or 'hello' in query:
                speak('Hello sir, how may I help you?')

            elif "open adobe reader" in query:
                apath = "C:\\Program Files (x86)\\Adobe\\Reader 11.0\\Reader\\AcroRd32.exe"
                os.startfile(apath)

            elif "open command prompt" in query:
                os.system("start cmd")

            elif "open camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break;
                cap.release()
                cv2.destroyAllWindows()

            elif "play music" in query:
                music_dir = "E:\\music"
                songs = os.listdir(music_dir)
                # rd = random.choice(songs)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))


            #
            # elif "ip address" in query:
            #     ip = get('https://api.ipify.org').text
            #     speak(f"your IP address is {ip}")

            elif "wikipedia" in query:
                speak("searching wikipedia....")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("according to wikipedia")
                speak(results)
                # print(results)
            elif "translate" in query:
                speak(translate())

            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")

            elif "open facebook" in query:
                webbrowser.open("www.facebook.com")

            elif "open stackoverflow" in query:
                webbrowser.open("www.stackoverflow.com")

            elif "open google" in query:
                speak("sir, what should i search on google")
                cm = takecommand().lower()
                webbrowser.open(f"{cm}")

            # elif "send whatsapp message" in query:
            #     kit.sendwhatmsg("+91_To_number_you_want_to_send", "this is testing protocol", 4, 13)
            #     time.sleep(120)
            #     speak("message has been sent")

            # elif "song on youtube" in query:
            #     kit.playonyt("see you again")

            elif 'timer' in query or 'stopwatch' in query:
                speak("For how many minutes?")
                timing = takecommand()
                timing = timing.replace('minutes', '')
                timing = timing.replace('minute', '')
                timing = timing.replace('for', '')
                timing = float(timing)
                timing = timing * 60
                speak(f'I will remind you in {timing} seconds')

                time.sleep(timing)
                speak('Your time has been finished sir')


            elif "Bye" in query:
                speak("thanks for using me sir, have a good day.")
                sys.exit()


            # to set an alarm

            # to find a joke
            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "shut down the system" in query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in query:
                os.system("shutdown /r /t 5")

            elif "sleep the system" in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


            elif 'switch the window' in query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "tell me news" in query:
                speak("please wait sir, feteching the latest news")
                news()


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    # def run(self):
    #     self.TaskExection
    def startTask(self):
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
