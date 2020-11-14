# -*- coding: utf-8 -*-
# -*- coding: cp1251 -*-

#Пока храним данные так - на каждую главу отдельная папка.
#В этой папке файлы:
#1."sound.mp3" - аудио всей главы
#
#2."sheets" - подфайл состоящий  только
#  из файлов "n.txt", где n - номер страницы.
#
#3."timepoints.txt" - таймпоинты. Каждый таймпоинт соответствует абзацу
#  и состоит из двух целых чисел. Первое - номер страница абзаца.
#  Второе время в секундах, когда этот абзац начинает читаться.

import os.path

import pygame

from kivy.config import Config
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '720')
Config.set('graphics', 'height', '500')

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput

from kivy.uix.boxlayout import BoxLayout

from kivy.clock import Clock


class timepoint_class:
    page = 0
    start_time = 0

class BookBlabberApp(App):
    def play_pause_interact(self, *args):
        if self.current_regime == 'read_regime':
            self.current_regime = 'headphones_regime'
            pygame.mixer.music.unpause()
        elif self.current_regime == 'headphones_regime':
            self.current_regime = 'read_regime'
            pygame.mixer.music.pause()


    #def restart_interact(self, *args):
    #    pygame.mixer.music.stop()
    #    pygame.mixer.music.play()
    #    self.current_regime = 'headphones_regime'


    def left_interact(self, *args):
        if self.page_number != 0:
            self.page_number -= 1

            f = open('source/' + self.book_name + '/' + self.chapter_name
                     + '/sheets/' + str(self.page_number) + '.txt', 'rb')
            text_source = f.read()
            f.close()


            want_num = 0
            for timepoint in self.timepoints:
                if timepoint.page < self.page_number:
                    want_num += 1
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            pygame.mixer.music.set_pos(self.timepoints[want_num].start_time)
            self.sound_position = self.timepoints[want_num].start_time
            if self.current_regime == 'read_regime':
                pygame.mixer.music.pause()

            self.root_widget.children[0].text = text_source


    def right_interact(self, *args):
        if self.page_number < len(os.listdir('source/' + self.book_name +
                                             '/' + self.chapter_name + '/sheets/')) - 1:
            self.page_number += 1

            f = open('source/' + self.book_name + '/' + self.chapter_name + '/sheets/' +
                     str(self.page_number) + '.txt', 'rb')
            text_source = f.read()
            f.close()

            want_num = 0
            for timepoint in self.timepoints:
                if timepoint.page < self.page_number:
                    want_num += 1
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            pygame.mixer.music.set_pos(self.timepoints[want_num].start_time)
            self.sound_position = self.timepoints[want_num].start_time
            if self.current_regime == 'read_regime':
                pygame.mixer.music.pause()

            self.root_widget.children[0].text = text_source

    def build(self):
        BookBlabberApp.page_number = 0
        self.current_regime = 'read_regime'

        f = open('source/' + self.book_name + '/' + self.chapter_name + '/sheets/' +
        str(self.page_number) + '.txt', 'rb')
        text_source = f.read()
        f.close()

        f = open('source/' + self.book_name + '/' + self.chapter_name
                 + '/timepoints.txt')
        timepoints_data = str(f.read())
        #print(timepoints_data[0])
        timepoints_data = timepoints_data.splitlines()
        f.close()

        self.timepoints = []

        for cur_str in timepoints_data:
            add_timepoint = timepoint_class()
            cur_str = cur_str.split('\t')
            add_timepoint.page = int(cur_str[0])
            add_timepoint.start_time = int(cur_str[1])
            self.timepoints.append(add_timepoint)

        pygame.mixer.music.load('source/' + self.book_name + '/' + self.chapter_name +
                                '/sound.mp3')
        pygame.mixer.music.play()
        pygame.mixer.music.pause()
        self.sound_position = 0

        paper = TextInput(readonly=True, text=text_source)

        play_pause_button = Button(text="PLAY/\nPAUSE",
                                   on_release=self.play_pause_interact)
        play_pause_button.size_hint = (1, .2)
        #restart_button = Button(text="RESTART", on_release=self.restart_interact)
        #restart_button.size_hint = (1, .2)
        space_wid = Widget()
        left_button = Button(text="LEFT", on_release=self.left_interact)
        left_button.size_hint = (1, .2)
        right_button = Button(text="RIGHT", on_release=self.right_interact)
        right_button.size_hint = (1, .2)

        buttons_panel = BoxLayout(orientation="vertical")
        buttons_panel.size_hint = (.1, 1)
        buttons_panel.add_widget(play_pause_button)
        #buttons_panel.add_widget(restart_button)
        buttons_panel.add_widget(space_wid)
        buttons_panel.add_widget(left_button)
        buttons_panel.add_widget(right_button)

        self.root_widget = BoxLayout(orientation="horizontal")                      #корневой виджет
        self.root_widget.add_widget(buttons_panel)                                  #второй его потомок - панель кнопок
        self.root_widget.add_widget(paper)                                          #первый - paper (виджет типа TextInput)
                                                                                    #да, добавляются в стек детей в обратном порядке

        self.my_widget = Widget()
        self.my_widget.create_property('custom')
        self.my_widget.custom = True
        print(self.my_widget.custom)

        return self.root_widget

bb = BookBlabberApp()

def sound_treatment(dt):
    cur_timepoint = timepoint_class()
    for timepoint in bb.timepoints:
        if timepoint.start_time <= bb.sound_position:
            cur_timepoint.page = timepoint.page
            cur_timepoint.start_time = timepoint.start_time
    bb.sound_position = pygame.mixer.music.get_pos()/1000 + cur_timepoint.start_time
    if cur_timepoint.page > bb.page_number:
        bb.right_interact()
Clock.schedule_interval(sound_treatment, 1 / 30.)

if __name__ == "__main__":
    title = 'Book blabber'

    pygame.init()
    
    bb.book_name = 'Eugene Onegin'
    bb.chapter_name = 'chapter 1'

    bb.run()

    pygame.quit()