import pygame as pg
from PyQt5.QtWidgets import QFileDialog
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import*
import group_function  # 群組的py檔
import individual_android
import individual_ios

pg.init()
android_g = group_function.Android()  # 群組py檔的Android()
ios_g = group_function.Ios()  # 群組py檔的Ios()

android_i = individual_android.Android()
ios_i = individual_ios.Ios()


# 對話紀錄class
class Data:
    path = ''  # 檔案路徑
    system = ''  # 手機系統
    individual_group = ''  # 個人或群組聊天
    # 群組對話圖片
    img = ''  # 現在要呈現的圖片名稱
    surf = ''  # 夯夯和句點王
    surf_d = ''  # 群組一天內圖片
    surf_a = ''  # 群組從古至今圖片
    text_active = ''
    word_sticker1 = ''
    word_sticker2 = ''
    word_time1 = ''
    word_time2 = ''


# 跳視窗匯檔案class
class Window(QtWidgets.QWidget):
    def msg(self):
        # 限定匯入txt檔
        fileName, filetype = QFileDialog.getOpenFileName(self, "選取檔案", "./", "Text Files (*.txt)")

        return fileName


# 設定顏色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 48, 48)
green = (34, 177, 76)
blue = (70, 130, 180)
dark = (170, 170, 170)
light = (100, 100, 100)

# 設定字體大小
small_font = pg.font.SysFont('appleligothicmedium', 18)
med_font = pg.font.SysFont('appleligothicmedium', 30)
large_font = pg.font.SysFont('appleligothicmedium', 50)

# 設定視窗
width, height = 800, 800
screen = pg.display.set_mode((width, height))
pg.display.set_caption('LINE聊天對話分析')

# 建立畫布
bg = pg.Surface(screen.get_size())
bg = bg.convert()
bg.fill(white)


# 文字物件樣式
def text_objects(text, color, size):
    textSurface = ''
    if size == 'small':
        textSurface = small_font.render(text, True, color)
    elif size == 'medium':
        textSurface = med_font.render(text, True, color)
    elif size == 'large':
        textSurface = large_font.render(text, True, color)

    return textSurface, textSurface.get_rect()


# 螢幕上印出文字「置中」
def message_to_screen_center(msg, color, y_displace=0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (width / 2), (height / 2) + y_displace
    screen.blit(textSurf, textRect)  # 顯示


# 螢幕上印出文字「靠左對齊」
def message_to_screen_side(msg, color, x_displace=0, y_displace=0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    screen.blit(textSurf, [x_displace, y_displace])  # 顯示


# 在 button 上的文字
def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth/2)), buttony + (buttonheight/2))
    screen.blit(textSurf, textRect)  # 顯示


# 按鈕組合
def button(text, x, y, width, height, inactive_color, active_color):
    mouse = pg.mouse.get_pos()  # 儲存滑鼠游標 (x,y) 位置

    # 若滑鼠在 button 上方就變顏色
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        button_rect = pg.draw.rect(screen, active_color, (x, y, width, height))
    else:
        button_rect = pg.draw.rect(screen, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)
    return button_rect


# 匯入資料
def import_data():
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        myshow = Window()
        Data.path = myshow.msg()


# 依據手機系統分別執行功能
def ios_android_function(system, function):
    if system == 'iOS':  # 手機系統選ios，執行ios的群組功能
        if function == '誰是夯夯':
            surf, text = ios_g.hot_function()
            return surf, text
        elif function == '誰是句點王':
            surf, text = ios_g.dot_function()
            return surf, text
        elif function == '活躍時間':
            surf_d = ios_g.day_function()
            surf_a, text = ios_g.active_function()
            return surf_d, surf_a, text

    elif system == 'Android':
        if function == '誰是夯夯':
            surf, text = android_g.hot_function()
            return surf, text
        elif function == '誰是句點王':
            surf, text = android_g.dot_function()
            return surf, text
        elif function == '活躍時間':
            surf_d = android_g.day_function()
            surf_a, text = android_g.active_function()
            return surf_d, surf_a, text


def ios_android_function_i(system, function):
    if system == 'Android':  # 手機系統選Android，執行Android的個人功能
        if function == '字數':
            android_i.inputfile(Data.path)
            surf_a, surf_d = android_i.words()
            return surf_a, surf_d
        elif function == '句數':
            android_i.inputfile2(Data.path)
            surf, surf_a, surf_d = android_i.sentences()
            return surf, surf_a, surf_d
        elif function == '通話':
            android_i.inputfile2(Data.path)
            surf, surf_a, surf_d, time1, time2 = android_i.calls()
            return surf, surf_a, surf_d, time1, time2
        elif function == '常用的字':
            surf = pg.image.load('/Users/yashan/Desktop/GitHub/android_wordcloud.png')
            return surf
        elif function == '關係成分':
            android_i.inputfile(Data.path)
            surf = android_i.relationships()
            return surf
        elif function == '其他':
            android_i.inputfile2(Data.path)
            surf_a, surf_d, sticker1, sticker2, time1, time2 = android_i.others()
            return surf_a, surf_d, sticker1, sticker2, time1, time2

    elif system == 'iOS':
        if function == '字數':
            ios_i.inputfile(Data.path)
            surf_a, surf_d = ios_i.words()
            return surf_a, surf_d
        elif function == '句數':
            ios_i.inputfile2(Data.path)
            surf, surf_a, surf_d = ios_i.sentences()
            return surf, surf_a, surf_d
        elif function == '通話':
            ios_i.inputfile2(Data.path)
            surf, surf_a, surf_d, time1, time2 = ios_i.calls()
            return surf, surf_a, surf_d, time1, time2
        elif function == '常用的字':
            surf = pg.image.load('/Users/yashan/Desktop/GitHub/ios_wordcloud.png')
            return surf
        elif function == '關係成分':
            ios_i.inputfile(Data.path)
            surf = ios_i.relationships()
            return surf
        elif function == '其他':
            ios_i.inputfile2(Data.path)
            surf_a, surf_d, sticker1, sticker2, time1, time2 = ios_i.others()
            return surf_a, surf_d, sticker1, sticker2, time1, time2


# 個人頁面
def individual():

    back = False
    while not back:
        screen.fill(white)
        message_to_screen_side("個人聊天分析結果", black, 50, 50, 'medium')
        if Data.img == '其他':
            message_to_screen_center(Data.word_sticker1+'     '+Data.word_time1, black, 320)
            message_to_screen_center(Data.word_sticker2 + '     ' + Data.word_time2, blue, 355)
        elif Data.img == '通話':
            message_to_screen_side(Data.word_time1, black, 445, 270)
            message_to_screen_side(Data.word_time2, black, 445, 320)

        button_word = button("字數", 50, 100, 100, 50, dark, light)
        button_sentence = button("句數", 150, 100, 100, 50, dark, light)
        button_call = button("通話", 250, 100, 100, 50, dark, light)
        button_often = button("常用的字", 350, 100, 100, 50, dark, light)
        button_relation = button("關係成分", 450, 100, 100, 50, dark, light)
        button_other = button("其他", 550, 100, 100, 50, dark, light)
        button_back = button("回首頁", 650, 100, 100, 50, dark, light)

        if Data.img == '字數':
            screen.blit(Data.surf_a, (-5, 280))    # 圖片擺放位置
            screen.blit(Data.surf_d, (305, 200))
            pg.display.flip()

        elif Data.img == '句數' or Data.img == "通話":
            screen.blit(Data.surf, (30, 170))
            screen.blit(Data.surf_a, (30, 450))  # 圖片擺放位置
            screen.blit(Data.surf_d, (400, 450))
            pg.display.flip()

        elif Data.img == "關係成分":
            screen.blit(Data.surf, (20, 170))  # 圖片擺放位置
            pg.display.flip()

        elif Data.img == "常用的字":
            screen.blit(Data.surf, (-110, 170))  # 圖片擺放位置
            pg.display.flip()

        elif Data.img == '其他':
            screen.blit(Data.surf_a, (-5, 280))  # 圖片擺放位置和!!!結論字串!!!
            screen.blit(Data.surf_d, (305, 200))
            pg.display.flip()

        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_word.collidepoint(ev.pos):
                    Data.surf_a, Data.surf_d = ios_android_function_i(Data.system, '字數')
                    Data.img = "字數"

                elif button_sentence.collidepoint(ev.pos):
                    Data.surf, Data.surf_a, Data.surf_d = ios_android_function_i(Data.system, "句數")
                    Data.img = "句數"

                elif button_call.collidepoint(ev.pos):
                    Data.surf, Data.surf_a, Data.surf_d, Data.word_time1, Data.word_time2 = ios_android_function_i(Data.system, "通話")
                    Data.img = "通話"

                elif button_often.collidepoint(ev.pos):
                    Data.surf = ios_android_function_i(Data.system, "常用的字")
                    Data.img = "常用的字"

                elif button_relation.collidepoint(ev.pos):
                    Data.surf = ios_android_function_i(Data.system, '關係成分')
                    Data.img = "關係成分"

                elif button_other.collidepoint(ev.pos):
                    Data.surf_a, Data.surf_d, Data.word_sticker1, Data.word_sticker2,\
                        Data.word_time1, Data.word_time2 = ios_android_function_i(Data.system, '其他')
                    Data.img = "其他"

                elif button_back.collidepoint(ev.pos):
                    game_intro()


# 群組頁面
def group():
    Data.path = ''  # 路徑清空

    back = False
    # myphone = group_function.Android
    while not back:
        screen.fill(white)
        message_to_screen_side("群組聊天分析結果", black, 50, 50, 'medium')
        if Data.img == '活躍時間':
            message_to_screen_center(Data.text_active, blue, 300)
        elif Data.img == '誰是夯夯':
            message_to_screen_center(Data.word_time1 + ' 是夯夯！', blue, 300)
        elif Data.img == '誰是句點王':
            message_to_screen_center(Data.word_time1 + ' 是句點王。', blue, 300)

        button_hot = button("誰是夯夯", 50, 120, 100, 50, dark, light)
        button_dot = button("誰是句點王", 250, 120, 100, 50, dark, light)
        button_active = button("活躍時間", 450, 120, 100, 50, dark, light)
        button_back = button("回首頁", 650, 120, 100, 50, dark, light)

        if Data.img == '誰是夯夯' or Data.img == '誰是句點王':
            screen.blit(Data.surf, (25, 220))  # 圖片擺放位置
            pg.display.flip()
        elif Data.img == '活躍時間':
            screen.blit(Data.surf_d, (30, 250))
            screen.blit(Data.surf_a, (400, 250))
            pg.display.flip()


        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_hot.collidepoint(ev.pos):
                    Data.surf, Data.word_time1 = ios_android_function(Data.system, '誰是夯夯')  # 要呈現的圖片
                    Data.img = '誰是夯夯'

                elif button_dot.collidepoint(ev.pos):
                    Data.surf, Data.word_time1 = ios_android_function(Data.system, '誰是句點王')
                    Data.img = '誰是句點王'

                elif button_active.collidepoint(ev.pos):
                    Data.surf_d, Data.surf_a, Data.text_active = ios_android_function(Data.system, '活躍時間')
                    Data.img = '活躍時間'

                elif button_back.collidepoint(ev.pos):
                    game_intro()


# 基本設定（選擇手機系統、個人群組頁面）
def choice():
    back = False
    while not back:
        screen.fill(white)
        background = pg.image.load('/Users/yashan/Downloads/choice_bg.png')
        screen.blit(background, (-5, -5))
        # message_to_screen_center("基本設定", black, -220, 'medium')
        # message_to_screen_side('您手機的系統為：', black, 250, 400, 'medium')
        # message_to_screen_side('輸入的對話紀錄為：', black, 250, 600, 'medium')
        android_img = pg.image.load('/Users/yashan/Downloads/icons8-android-os-48.png')
        ios_img = pg.image.load('/Users/yashan/Downloads/icons8-ios-logo-50.png')
        indi_img = pg.image.load('/Users/yashan/Downloads/icons8-toddler-50.png')
        group_img = pg.image.load('/Users/yashan/Downloads/icons8-crowd-50.png')

        screen.blit(android_img, (204, 655))
        screen.blit(ios_img, (306, 655))
        screen.blit(indi_img, (444, 655))
        screen.blit(group_img, (545, 655))

        if Data.system != '':
            message_to_screen_side(Data.system, black, 630, 341, 'medium')
        if Data.individual_group != '':
            message_to_screen_side(Data.individual_group, black, 630, 550, 'medium')

        button_android = button("Android", 179, 710, 100, 50, (176, 196, 222), (240, 255, 240))
        button_ios = button("iOS", 281, 710, 100, 50, (176, 196, 222), (240, 255, 240))
        button_individual = button("個人聊天", 419, 710, 100, 50, (176, 196, 222), (240, 255, 240))
        button_group = button("群組聊天", 521, 710, 100, 50, (176, 196, 222), (240, 255, 240))
        button_back = button("回首頁", 40, 710, 100, 50, (135, 206, 250), (255, 246, 143))
        button_start = button("開始分析", 660, 710, 100, 50, (135, 206, 250), (255, 246, 143))

        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_ios.collidepoint(ev.pos):  # 按下ios
                    Data.system = 'iOS'

                elif button_android.collidepoint(ev.pos):  # 按下android
                    Data.system = 'Android'

                elif button_individual.collidepoint(ev.pos):  # 按下個人聊天
                    Data.individual_group = '個人聊天'

                elif button_group.collidepoint(ev.pos):  # 按下群組聊天
                    Data.individual_group = '群組聊天'

                elif button_back.collidepoint(ev.pos):  # 按下回首頁
                    game_intro()

                elif button_start.collidepoint(ev.pos):  # 開始分析
                    if Data.individual_group != '' and Data.system != '':
                        if Data.individual_group == '個人聊天':
                            individual()
                        elif Data.individual_group == '群組聊天':

                            # 依照手機系統處理資料
                            if Data.system == 'iOS':
                                ios_g.input_file(Data.path)
                            elif Data.system == 'Android':
                                android_g.input_file(Data.path)

                            group()  # 群組頁面


# 遊戲首頁
def game_intro():
    intro = True
    Data.path = ''  # 路徑清空
    while intro:

        Data.img = ''  # 現在要呈現的圖片名稱清空
        Data.individual_group = ''  # 群組或個人選擇清空
        Data.system = ''  # 系統選擇清空

        screen.fill(white)
        background = pg.image.load('/Users/yashan/Downloads/menu.png')
        screen.blit(background, (-5, -5))

        message_to_screen_center("歡迎來到遊戲", black, -160, 'medium')
        message_to_screen_center("請先確認您的手機為「24小時制」且為「中文版本」", white, -120)
        message_to_screen_center("再由「手機的line」匯出對話紀錄 txt.檔並儲存至您的電腦", black, -80)
        message_to_screen_center("點選「匯入資料」匯入您的對話紀錄，並根據手機系統點選「Android」或「iOS」", black, -40)
        message_to_screen_center("依據您的對話紀錄點選「個人聊天」或是「群組聊天」", black, 0)
        message_to_screen_center("就會進入對話紀錄分析的頁面囉！", black, 40)
        if Data.path == '':
            message_to_screen_center('*** 請匯入資料 ***', white, 180)
        else:
            message_to_screen_center('資料路徑：' + Data.path, white, 180)

        button_import = button("匯入資料", 350, 500, 100, 50, (135, 206, 250), (255, 246, 143))
        button_quit = button("離開", 200, 700, 100, 50, (176, 196, 222), (240, 255, 240))
        button_next = button("下一頁", 500, 700, 100, 50, (176, 196, 222), (240, 255, 240))

        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_import .collidepoint(ev.pos):
                    import_data()  # 匯入資料
                    print(Data.path)  # 檔案路徑 Data.path

                elif button_next.collidepoint(ev.pos):
                    if Data.path != '':  # 有路徑才能按下一頁
                        choice()

                elif button_quit.collidepoint(ev.pos):
                    pg.quit()
                    quit()


game_intro()

# 關閉
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:  # 使用者按右上角的關閉鈕
            running = False

pg.quit()  # 關閉繪圖視窗
quit()
