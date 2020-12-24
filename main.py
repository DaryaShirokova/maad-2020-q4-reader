# -*- coding: utf-8 -*-
# -*- coding: cp1251 -*-

#Пока храним данные так - на каждую главу отдельная папка.
#В этой папке файлы:
#1."sound.mp3" - аудио всей книги
#
#2."text.txt" - текст всей книги
#
#3."timepoints.txt" - таймпоинты. Каждый таймпоинт связывает координаты текста и звука.
#  Он состоит из двух целых чисел. Первое - координата текста.
#  Второе время в секундах, когда этот рассказчик читает близко к координате текста.

import os.path

import pygame
import pygame.mixer_music as speaker

import codecs

from kivy.config import Config
Config.set('graphics', 'resizable', False)
window_width = 1440
window_height = 1000
Config.set('graphics', 'width', window_width)
Config.set('graphics', 'height', window_height)

FTT = ''

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.clock import Clock

from kivy.graphics import (Rectangle)

from kivy.core.window import Window
Window.clearcolor = (125.0/255, 100.0/255, 50.0/255, 1)

class PageClass:
    first_symbol_coord = 0
    last_symbol_coord = 0
    first_line_coord = 0
    last_line_coord = 0
class PaperClass(TextInput):
    def set_lines(self, first_line_coord, last_line_coord):
        self.text = ''
        for s in self.full_lines[first_line_coord:last_line_coord+1]:
            self.text += s + '\n'

    def init(self, text_adress, pg_num=0):
        self.font_name = 'fonts/paper_font.ttf'
        self.font_size = 30

        self.selection_color = (0,0,0,0)

        self.readonly = True
        self.width = window_width * self.size_hint_x
        self.height = window_height * self.size_hint_y

        f = codecs.open(text_adress, 'r', 'utf_8_sig')
        self.full_text = f.read()
        f.close()
        self.full_text = self.full_text.replace("\n", "0\n")

        self.text = self.full_text
        self.full_lines = []
        for line in self._lines:
            self.full_lines.append(str(line))

        new_first_symbol_coord = 0
        new_last_symbol_coord = -1
        self.pages = []
        number_of_lines_in_page = int(self.height) // int(self.line_height) - 3
        t = 0
        i = 0
        new_first_line_coord = 0
        new_last_line_coord = -1
        for line in self.full_lines:                #Прошу не бейте ногами
            t += 1
            new_last_symbol_coord += len(line)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            new_last_line_coord += 1
            self.full_lines[i] = self.full_lines[i].replace("0", "")
            i += 1

            if t == number_of_lines_in_page:
                new_page = PageClass()
                new_page.first_symbol_coord = new_first_symbol_coord
                new_page.last_symbol_coord = new_last_symbol_coord
                new_page.first_line_coord = new_first_line_coord
                new_page.last_line_coord = new_last_line_coord
                self.pages.append(new_page)

                new_first_line_coord = new_last_line_coord + 1
                new_first_symbol_coord = new_last_symbol_coord + 1
                t = 0
        new_page = PageClass()
        new_page.first_symbol_coord = new_first_symbol_coord
        new_page.last_symbol_coord = new_last_symbol_coord
        new_page.first_line_coord = new_first_line_coord
        new_page.last_line_coord = new_last_line_coord
        self.pages.append(new_page)

        self.full_text = self.full_text.replace("0\n", "\n")

        self.num_pages = len(self.pages)
        self.set_page_num(pg_num)

    def set_page_num(self, pg_num):
        self.set_lines(self.pages[pg_num].first_line_coord, self.pages[pg_num].last_line_coord)
        self.cur_page_num = pg_num
    def get_page_num(self):
        return self.cur_page_num

    def flip_right(self):
        if self.cur_page_num < self.num_pages - 1:
            self.set_page_num(self.cur_page_num + 1)
    def flip_left(self):
        if self.cur_page_num > 0:
            self.set_page_num(self.cur_page_num - 1)

    def set_page_near_text_coord(self, txt_crd):
        new_pg_num = -1
        for pg in self.pages:
            if pg.first_symbol_coord <= txt_crd:
                new_pg_num += 1
        self.set_page_num(new_pg_num)
    def set_page_near_line_coord(self, ln_crd):
        new_pg_num = -1
        for pg in self.pages:
            if pg.first_line_coord <= ln_crd:
                new_pg_num += 1
        self.set_page_num(new_pg_num)
    def get_page_near_text_coord(self, txt_crd):
        res_pg_num = -1
        for pg in self.pages:
            if pg.first_symbol_coord <= txt_crd:
                res_pg_num += 1
        return res_pg_num
    def get_page_near_line_coord(self, ln_crd):
        res_pg_num = -1
        for pg in self.pages:
            if pg.first_line_coord <= ln_crd:
                res_pg_num += 1
        self.set_page_num(res_pg_num)
class ScreenClass(FloatLayout):
    def page_show(self):
        self.children[0].clear_widgets()

        if self.left_paper.cur_page_num == 0:
            left_button = Button(background_normal = 'images/zero.png', background_down = 'images/zero.png')
        else:
            left_button = Button(background_normal = 'images/left_button.png', background_down = 'images/left_button_pressed.png', on_release=self.left_interact)
        left_button.size_hint = (40/1440, 160/1000)
        left_button.pos_hint = {'x': 5/1440, 'y': 415/1000}#(0, 340)

        left_page_text = Label()
        left_page_text.font_name = 'fonts/paper_font.ttf'
        left_page_text.font_size = 30
        left_page_text.color = (0, 0, 0, 1)
        left_page_text.text = str(self.left_paper.cur_page_num + 1)
        left_page_text.halign = 'center'
        left_page_text.multiline = False
        left_page_text.on_text_validate = self.set_page_num_ti
        left_page_text.pos_hint = {'x':280/1440, 'y':30/1000}
        left_page_text.size_hint = (150/1440, 50/1000)
        right_page_text = Label()
        right_page_text.font_name = 'fonts/paper_font.ttf'
        right_page_text.font_size = 30
        right_page_text.color = (0,0,0,1)
        right_page_text.text = str(self.left_paper.cur_page_num + 2)
        right_page_text.halign = 'center'
        right_page_text.multiline = False
        right_page_text.on_text_validate = self.set_page_num_ti
        right_page_text.size_hint = (150/1440, 50/1000)
        right_page_text.pos_hint = {'x': 1010/1400, 'y': 30/1000}
        #down_text = Label(text='/' + str(self.paper.num_pages))
        #page_wid = BoxLayout(orientation='vertical')
        #page_wid.size_hint = (.1, 1)
        #page_wid.add_widget(up_text)
        #page_wid.add_widget(down_text)

        if (self.left_paper.cur_page_num == self.left_paper.num_pages - 2) or (self.left_paper.cur_page_num == self.left_paper.num_pages - 1):
            right_button = Button(background_normal = 'images/zero.png', background_down = 'images/zero.png')
        else:
            right_button = Button(background_normal = 'images/right_button.png', background_down = 'images/right_button_pressed.png', on_release=self.right_interact)
        right_button.size_hint = (40/1440, 160/1000)# = (60, 320)
        #right_button.pos = (1385, 340)
        right_button.pos_hint = {'x': 1400 / 1440, 'y': 415 / 1000}

        #space_wid = Widget()
        #space_wid.size_hint = (.5, 1)

        restart_page_button = Button()
        restart_page_button.on_release = self.restart_page_interact
        restart_page_button.size_hint = (75/1440, 75/1000)
        restart_page_button.background_normal = 'images/restart_button.png'
        restart_page_button.background_down = 'images/restart_button_pressed.png'
        restart_page_button.background_disabled_normal = 'images/zero.png'
        restart_page_button.pos_hint = {'x':1330/1440, 'y':905/1000}

        play_pause_button = Button()
        play_pause_button.on_release = self.play_pause_interact
        if self.mode == 'reading':
            play_pause_button.background_normal = 'images/play_button.png'
            play_pause_button.background_down = 'images/play_button_pressed.png'
        elif self.mode == 'listening':
            play_pause_button.background_normal = 'images/pause_button.png'
            play_pause_button.background_down = 'images/pause_button_pressed.png'
        play_pause_button.size_hint = (75/1440, 75/1000)
        play_pause_button.pos_hint = {'x': 1240 / 1440, 'y': 905 / 1000}

        #buttons_layout = FloatLayout()
        #buttons_layout.size = (1440, 1000)
        #buttons_layout.pos = (0, 0)
        #buttons_panel.size_hint = (1, .1)

        self.children[0].add_widget(left_button)
        self.children[0].add_widget(left_page_text)
        self.children[0].add_widget(right_button)
        self.children[0].add_widget(right_page_text)
        self.children[0].add_widget(restart_page_button)
        self.children[0].add_widget(play_pause_button)

    def left_interact(self, *args):
        if self.left_paper.cur_page_num != self.left_paper.num_pages - 1:
            self.left_paper.flip_left()
            self.left_paper.flip_left()
            self.right_paper.flip_left()
            self.right_paper.flip_left()
        else:
            self.left_paper.flip_left()
            self.left_paper.flip_left()
            self.right_paper.foreground_color = (0, 0, 0, 1)
        self.page_show()
        self.events.append('left')
    def right_interact(self, *args):
        if self.left_paper.cur_page_num != self.left_paper.num_pages - 3:
            self.left_paper.flip_right()
            self.left_paper.flip_right()
            self.right_paper.flip_right()
            self.right_paper.flip_right()
        else:
            self.left_paper.flip_right()
            self.left_paper.flip_right()
            self.right_paper.foreground_color = (0,0,0,0)
        self.page_show()
        self.events.append('right')
    def restart_page_interact(self, *args):
        self.set_page_num(self.left_paper.cur_page_num)
    def play_pause_interact(self, *args):
        self.events.append('play_pause')
        if self.mode =='reading':
            self.mode = 'listening'
        elif self.mode == 'listening':
            self.mode = 'reading'
        self.page_show()

    def set_page_num(self, pg_num):
        if (pg_num >= 0) and (pg_num < self.left_paper.num_pages):
            self.left_paper.set_page_num(pg_num)
            self.page_show()
            self.events.append('set_page_num')


    def set_page_num_ti(self):
        page_num_str = self.children[0].children[4].children[1].text
        self.children[0].children[4].children[1].text = ''
        if (page_num_str.isdigit()):
            self.set_page_num(int(page_num_str) - 1)

    def reading_mode_init(self, book_name, page=0):
        self.clear_widgets()

        self.left_paper = PaperClass()
        self.left_paper.background_normal = 'images/zero.png'
        self.left_paper.background_active = 'images/zero.png'
        self.left_paper.background_disabled_normal = 'images/zero.png'
        self.left_paper.size_hint = (600/1440, 870/1000)
        self.left_paper.pos_hint = {'x':50/1440, 'y':20/1000}

        self.left_paper.init('source/' + book_name + '/text.txt', page)

        self.right_paper = PaperClass()
        self.right_paper.background_normal = 'images/zero.png'
        self.right_paper.background_active = 'images/zero.png'
        self.right_paper.background_disabled_normal = 'images/zero.png'
        self.right_paper.size_hint = (600 / 1440, 870 / 1000)
        self.right_paper.pos_hint = {'x': 770 / 1440, 'y': 20 / 1000}

        self.right_paper.init('source/' + book_name + '/text.txt', page + 1)


        buttons_layout = FloatLayout()
        buttons_layout.size_hint = (1.0, 1.0)
        buttons_layout.pos_hint = {'x':0, 'y':0}
        #self.orientation = 'vertical'

        self.fone_widget = Widget()
        self.fone_widget.pos_hint = {'x':0, 'y':0}
        self.fone_widget.size_hint = (1.0, 1.0)
        self.fone_widget.canvas.add(Rectangle(source = 'images/fone.png', pos = (0,0), size = (window_width, window_height)))

        self.add_widget(self.fone_widget)   # четвёртый потомок - фон
        self.add_widget(self.right_paper)  # третий его потомок - left_paper (виджет типа TextInput)
        self.add_widget(self.left_paper)  # второй его потомок - left_paper (виджет типа TextInput)
        self.add_widget(buttons_layout)  # первый - панель кнопок
        # да, добавляются в стек детей в обратном порядке

        #if self.paper.cur_page_num == 0:
        #    self.leftmost_page_show()
        #elif self.paper.cur_page_num == self.paper.num_pages:
        #    self.rightmost_page_show()
        #else:
        #    self.internal_page_show()
        self.mode = 'reading'
        self.page_show()

        self.play_on = False
        self.events = []

    def book_overview_init(self, book_name):
        pass

class TimepointClass:
    text_coord = 0
    sound_coord = 0
class SoundtrackClass:
    def init(self, book_name, cur_tmpt_num = 0):
        f = codecs.open('source/' + book_name + '/timepoints.txt', 'r', 'utf_8_sig')
        tmpts_text = f.read()
        f.close()
        coord_text = tmpts_text.split('\n')

        self.timepoints = []
        for cor in coord_text:
            add_timepoint = TimepointClass()
            cor = cor.split('\t')
            add_timepoint.text_coord = int(cor[0])
            add_timepoint.sound_coord = int(cor[1])
            self.timepoints.append(add_timepoint)
        self.cur_timepoint_num = cur_tmpt_num
        self.sound_position = 0

        speaker.load('source/' + book_name + '/sound.mp3')
        speaker.play()
        speaker.pause()

        self.paused = True

    def set_timepoint_num(self, timept_num):
        self.cur_timepoint_num = timept_num

        speaker.stop()
        speaker.play()
        speaker.set_pos(self.timepoints[self.cur_timepoint_num].sound_coord)
        speaker.pause()

        if not self.paused:
            speaker.unpause()

    def get_timepoint_num(self):
        return self.cur_timepoint_num

    def set_timepoint_num_near_text_coord(self, txt_crd):
        new_tmp_num = -1
        for tmp in self.timepoints:
            if tmp.text_coord <= txt_crd:
                new_tmp_num += 1
        self.set_timepoint_num(new_tmp_num)
    def set_timepoint_num_near_sound_coord(self, snd_crd):
        new_tmp_num = -1
        for tmp in self.timepoints:
            if tmp.sound_coord <= snd_crd:
                new_tmp_num += 1
        self.set_timepoint_num(new_tmp_num)

    def get_timepoint_num_near_text_coord(self, txt_crd):
        res_tmp_num = -1
        for tmp in self.timepoints:
            if tmp.text_coord <= txt_crd:
                res_tmp_num += 1
        return res_tmp_num
    def get_timepoint_num_near_sound_coord(self, snd_crd):
        res_tmp_num = -1
        for tmp in self.timepoints:
            if tmp.sound_coord <= snd_crd:
                res_tmp_num += 1
        return res_tmp_num

    def play(self):
        speaker.play()
    def pause(self):
        speaker.pause()
    def unpause(self):
        speaker.unpause()
    def stop(self):
        speaker.stop()

    def get_busy(self):
        return speaker.get_busy()

    def update(self):
        self.sound_position = self.timepoints[self.cur_timepoint_num].sound_coord + speaker.get_pos() / 1000.0
        #print (self.sound_position)

        if self.cur_timepoint_num < len(self.timepoints) - 1:
            if self.sound_position > self.timepoints[self.cur_timepoint_num + 1].sound_coord:
                self.set_timepoint_num(self.cur_timepoint_num + 1)

class CommunicatorClass:
    def handle_screen_events(self, screen, soundtrack):
        for event in screen.events:
            if event == 'left' or event == 'right' or event == 'set_page_num':
                #print(screen.left_paper.cur_page_num)
                fst_sym_crd = screen.left_paper.pages[screen.left_paper.cur_page_num].first_symbol_coord
                #lst_sym_crd = screen.left_paper.pages[screen.left_paper.cur_page_num].last_symbol_coord
                #print (str(fst_sym_crd) + ' ' + str(lst_sym_crd))
                soundtrack.set_timepoint_num_near_text_coord(fst_sym_crd)
                #print (soundtrack.timepoints[soundtrack.cur_timepoint_num].sound_coord)
                #print(screen.left_paper.full_text[fst_sym_crd:lst_sym_crd])
            if event == 'play_pause':
                if soundtrack.paused:
                    soundtrack.unpause()
                    soundtrack.paused = False
                else:
                    soundtrack.pause()
                    soundtrack.paused = True
            screen.events.remove(event)
    def put_the_desired_page(self, screen, soundtrack):
        c_tmp = soundtrack.timepoints[soundtrack.get_timepoint_num()]
        c_pg = screen.right_paper.pages[screen.left_paper.get_page_num()]

        if c_tmp.text_coord > c_pg.last_symbol_coord:
            screen.right_interact()
            screen.events.remove('right')

    def update(self, screen, soundtrack):
        self.handle_screen_events(screen, soundtrack)
        self.put_the_desired_page(screen, soundtrack)

class BookBlabberApp(App):
    def build(self):
        self.screen = ScreenClass()
        self.screen.reading_mode_init('Eugene Onegin')

        self.soundtrack = SoundtrackClass()
        self.soundtrack.init('Eugene Onegin')

        self.communicator = CommunicatorClass()

        return self.screen
    def update(self, dt):
        self.soundtrack.update()
        self.communicator.update(self.screen, self.soundtrack)

if __name__ == "__main__":
    title = "Sync Book"

    pygame.init()

    bb = BookBlabberApp()
    #bb.book_name = 'Eugene Onegin'
    #bb.chapter_name = 'chapter 1'

    Clock.schedule_interval(bb.update, 1/30)
    bb.run()

    pygame.quit()

'''
    class BookBlabberApp(App):
        def play_pause_interact(self, *args):
            if self.current_regime == 'read_regime':
                self.current_regime = 'headphones_regime'
                pygame.mixer.music.unpause()
            elif self.current_regime == 'headphones_regime':
                self.current_regime = 'read_regime'
                pygame.mixer.music.pause()

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

                self.root_widget.children[1].text = text_source
                self.root_widget.children[0].children[4].text = str(self.page_number)

                if self.page_number == 0:
                    self.root_widget.children[0].clear_widgets()

                    left_button = Widget()
                    left_button.size_hint = (.0001, 1)
                    page_label = Label(text=str(self.page_number))
                    page_label.size_hint = (.1, 1)
                    right_button = Button(text='RIGHT', on_release=self.right_interact)
                    right_button.size_hint = (.1, 1)
                    space_wid = Widget()
                    space_wid.size_hint = (.6999, 1)
                    play_pause_button = Button(text="PLAY/\nPAUSE",
                                               on_release=self.play_pause_interact)
                    play_pause_button.size_hint = (.1, 1)

                    self.root_widget.children[0].add_widget(left_button)
                    self.root_widget.children[0].add_widget(page_label)
                    self.root_widget.children[0].add_widget(right_button)
                    self.root_widget.children[0].add_widget(space_wid)
                    self.root_widget.children[0].add_widget(play_pause_button)
                else:
                    self.root_widget.children[0].clear_widgets()

                    left_button = Button(text='LEFT', on_release=self.left_interact)
                    left_button.size_hint = (.1, 1)
                    page_label = Label(text=str(self.page_number))
                    page_label.size_hint = (.1, 1)
                    right_button = Button(text='RIGHT', on_release=self.right_interact)
                    right_button.size_hint = (.1, 1)
                    space_wid = Widget()
                    space_wid.size_hint = (.6, 1)
                    play_pause_button = Button(text='PLAY/\nPAUSE',
                                               on_release=self.play_pause_interact)
                    play_pause_button.size_hint = (.1, 1)

                    self.root_widget.children[0].add_widget(left_button)
                    self.root_widget.children[0].add_widget(page_label)
                    self.root_widget.children[0].add_widget(right_button)
                    self.root_widget.children[0].add_widget(space_wid)
                    self.root_widget.children[0].add_widget(play_pause_button)



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

                self.root_widget.children[1].text = text_source
                self.root_widget.children[0].children[4].text = str(self.page_number)

                if self.page_number == len(os.listdir('source/' + self.book_name +
                                           '/' + self.chapter_name + '/sheets/')) - 1:
                    self.root_widget.children[0].clear_widgets()

                    left_button = Button(text='LEFT', on_release=self.left_interact)
                    left_button.size_hint = (.1, 1)
                    page_label = Label(text=str(self.page_number))
                    page_label.size_hint = (.1, 1)
                    right_button = Widget() #Button(text="RIGHT", on_release=self.right_interact)
                    right_button.size_hint = (.0001, 1)
                    space_wid = Widget()
                    space_wid.size_hint = (.6999, 1)
                    play_pause_button = Button(text="PLAY/\nPAUSE",
                                               on_release=self.play_pause_interact)
                    play_pause_button.size_hint = (.1, 1)

                    self.root_widget.children[0].add_widget(left_button)
                    self.root_widget.children[0].add_widget(page_label)
                    self.root_widget.children[0].add_widget(right_button)
                    self.root_widget.children[0].add_widget(space_wid)
                    self.root_widget.children[0].add_widget(play_pause_button)
                else:
                    self.root_widget.children[0].clear_widgets()

                    left_button = Button(text='LEFT', on_release=self.left_interact)
                    left_button.size_hint = (.1, 1)
                    page_label = Label(text=str(self.page_number))
                    page_label.size_hint = (.1, 1)
                    right_button = Button(text='RIGHT', on_release=self.right_interact)
                    right_button.size_hint = (.1, 1)
                    space_wid = Widget()
                    space_wid.size_hint = (.6, 1)
                    play_pause_button = Button(text='PLAY/\nPAUSE',
                                               on_release=self.play_pause_interact)
                    play_pause_button.size_hint = (.1, 1)

                    self.root_widget.children[0].add_widget(left_button)
                    self.root_widget.children[0].add_widget(page_label)
                    self.root_widget.children[0].add_widget(right_button)
                    self.root_widget.children[0].add_widget(space_wid)
                    self.root_widget.children[0].add_widget(play_pause_button)

        def build(self):
            self.page_number = 0
            self.current_regime = 'read_regime'

            f = open('source/' + self.book_name + '/' + self.chapter_name + '/sheets/' +
            str(self.page_number) + '.txt', 'rb')
            text_source = f.read()
            f.close()

            f = open('source/' + self.book_name + '/' + self.chapter_name
                     + '/timepoints.txt')
            timepoints_data = str(f.read())
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

            left_button = Widget()
            left_button.size_hint = (.0001, 1)
            page_label = Label(text = str(self.page_number))
            page_label.size_hint = (.1, 1)
            right_button = Button(text="RIGHT", on_release=self.right_interact)
            right_button.size_hint = (.1, 1)
            space_wid = Widget()
            space_wid.size_hint = (.6999, 1)
            play_pause_button = Button(text="PLAY/\nPAUSE",
                                       on_release=self.play_pause_interact)
            play_pause_button.size_hint = (.1, 1)

            buttons_panel = BoxLayout(orientation="horizontal")
            buttons_panel.size_hint = (1, .1)

            buttons_panel.add_widget(left_button)
            buttons_panel.add_widget(page_label)
            buttons_panel.add_widget(right_button)
            buttons_panel.add_widget(space_wid)
            buttons_panel.add_widget(play_pause_button)


            self.root_widget = BoxLayout(orientation="vertical")                        #корневой виджет
            self.root_widget.add_widget(paper)                                          #второй его потомок - paper (виджет типа TextInput)
            self.root_widget.add_widget(buttons_panel)                                  #первый - панель кнопок
                                                                                        #да, добавляются в стек детей в обратном порядке

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
    '''
