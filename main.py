# -*- coding: utf-8 -*-
# -*- coding: cp1251 -*-

#Пока храним данные так - на каждую главу отдельная папка. В этой папке файлы "n.txt" и "n.mp3", где n - номер страницы. То есть там хранятся тексты страниц и их аудио.

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

class BookBlabberApp(App):
    def play_pause_interact(self, instance):                                        #эта функция вызывается при нажатии кнопки "PLAY/PAUSE"
        if self.current_regime == 'read_regime':
            self.current_regime = 'headphones_regime'
            pygame.mixer.music.unpause()                                            #если в момент нажатия аудио не воспроизводится, то оно включается с момента паузы
        elif self.current_regime == 'headphones_regime':
            self.current_regime = 'read_regime'
            pygame.mixer.music.pause()                                              #а если воспроизводится, то оно ставится на паузу


    def restart_interact(self, instance):                                           #эта функция вызывается при нажатии кнопки "RESTART"
        pygame.mixer.music.stop()
        pygame.mixer.music.play(loops=-1)                                           #останавливаем аудио, запускаем заново и переходим в режим прослушивания
        self.current_regime = 'headphones_regime'                                   #loops = -1 означает, что аудио будет воспроизводится циклично


    def left_interact(self, instance):                                              #эта функция вызывается при нажатии кнопки "LEFT"
        if self.page_number != 0:                                                   #Если мы на нулевой странице, то ничего не происходит
            self.page_number -= 1

            if self.current_regime == 'headphones_regime':
                pygame.mixer.music.stop()
                pygame.mixer.music.load('source/' + self.book_name + '/' + self.chapter_name + '/' + str(self.page_number) + '.mp3')
                pygame.mixer.music.play(loops=-1)                                   #остановили старое аудио и загрузили новое

            f = open('source/' + self.book_name + '/' + self.chapter_name + '/' + str(self.page_number) + '.txt', 'rb')
            text_source = f.read()
            f.close()                                                               #записали текст новой страницы в переменную text_source

            self.root_widget.children[0].text = text_source                         #передали его в виджет TextInput


    def right_interact(self, instance):                                             #эта функция вызывается при нажатии кнопки "RIGHT" и работает аналогично
        if self.page_number < len(os.listdir('source/' + self.book_name + '/' + self.chapter_name + '/'))/2 - 1:
            self.page_number += 1

            if self.current_regime == 'headphones_regime':
                pygame.mixer.music.stop()
                pygame.mixer.music.load('source/' + self.book_name + '/' + self.chapter_name + '/' + str(self.page_number) + '.mp3')
                pygame.mixer.music.play(loops=-1)

            f = open('source/' + self.book_name + '/' + self.chapter_name + '/' + str(self.page_number) + '.txt', 'rb')
            text_source = f.read()
            f.close()

            self.root_widget.children[0].text = text_source


    def build(self):
        BookBlabberApp.page_number = 0                                              #изначально у нас 0 страница и режим чтения
        self.current_regime = 'read_regime'

        f = open('source/' + self.book_name + '/' + self.chapter_name + '/' + str(self.page_number) + '.txt', 'rb')
        text_source = f.read()
        f.close()                                                                   #записали текст нулевой страницы в переменную text_source

        pygame.mixer.music.load('source/' + self.book_name + '/' + self.chapter_name + '/' + str(self.page_number) + '.mp3')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.pause()                                                  #загрузили аудио нулевой страницы и поставили на цикл

        paper = TextInput(readonly=True, text=text_source)                          #создали виджет TextInput и загрузили в него текст, а также запретили редактировать

        play_pause_button = Button(text="PLAY/\nPAUSE", on_release=self.play_pause_interact)
        play_pause_button.size_hint = (1, .2)
        restart_button = Button(text="RESTART", on_release=self.restart_interact)
        restart_button.size_hint = (1, .2)
        space_wid = Widget()
        left_button = Button(text="LEFT", on_release=self.left_interact)
        left_button.size_hint = (1, .2)
        right_button = Button(text="RIGHT", on_release=self.right_interact)
        right_button.size_hint = (1, .2)                                            #создаём кнопки и пропуск между ними - пустой виджет space_wid

        buttons_panel = BoxLayout(orientation="vertical")
        buttons_panel.size_hint = (.1, 1)
        buttons_panel.add_widget(play_pause_button)
        buttons_panel.add_widget(restart_button)
        buttons_panel.add_widget(space_wid)
        buttons_panel.add_widget(left_button)
        buttons_panel.add_widget(right_button)                                      #это панель всех наших кнопок

        self.root_widget = BoxLayout(orientation="horizontal")                      #корневой виджет
        self.root_widget.add_widget(buttons_panel)                                  #второй его потомок - панель кнопок
        self.root_widget.add_widget(paper)                                          #первый - paper (виджет типа TextInput)
                                                                                    #да, добавляются в стек детей в обратном порядке

        return self.root_widget

if __name__ == "__main__":
    title = 'Book blabber'

    BookBlabberApp.book_name = 'Eugene Onegin'
    BookBlabberApp.chapter_name = 'chapter 1'
    pygame.init()

    BookBlabberApp().run()

    pygame.quit()