import pygame as pg
from PyQt5.QtWidgets import QFileDialog
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import*
import group_function  # 群組的py檔

pg.init()
android_g = group_function.Android()  # 群組py檔的Android()
ios_g = group_function.Ios()  # 群組py檔的Ios()


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
blue = (30, 144, 255)
dark = (170, 170, 170)
light = (100, 100, 100)

# 設定字體大小
small_font = pg.font.SysFont('appleligothicmedium', 18)
med_font = pg.font.SysFont('appleligothicmedium', 30)
large_font = pg.font.SysFont('appleligothicmedium', 50)

# 設定視窗
width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption('聊天資料分析')

# 建立畫布
bg = pg.Surface(screen.get_size())
bg = bg.convert()
bg.fill(white)


# 文字物件樣式
def text_objects(text, color, size):
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
    if system == 'ios':  # 手機系統選ios，執行ios的群組功能
        if function == '誰是夯夯':
            surf = ios_g.hot_function()
            return surf
        elif function == '誰是句點王':
            surf = ios_g.dot_function()
            return surf
        elif function == '活躍時間':
            surf_d = ios_g.day_function()
            surf_a = ios_g.active_function()
            return surf_d, surf_a

    elif system == 'android':
        if function == '誰是夯夯':
            surf = android_g.hot_function()
            return surf
        elif function == '誰是句點王':
            surf = android_g.dot_function()
            return surf
        elif function == '活躍時間':
            surf_d = android_g.day_function()
            surf_a = android_g.active_function()
            return surf_d, surf_a


# 個人頁面
def individual():
    back = False
    while not back:
        screen.fill(white)
        message_to_screen_side("個人頁面", green, 50, 50, 'medium')

        button_word = button("字數", 50, 100, 100, 50, dark, light)
        button_sentence = button("句數", 200, 100, 100, 50, dark, light)
        button_call = button("通話", 350, 100, 100, 50, dark, light)
        button_often = button("常用的字", 500, 100, 100, 50, dark, light)
        button_back = button("回首頁", 650, 100, 100, 50, dark, light)

        pg.display.update()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_word .collidepoint(ev.pos):
                    pass
                elif button_sentence .collidepoint(ev.pos):
                    pass
                elif button_call .collidepoint(ev.pos):
                    pass
                elif button_often .collidepoint(ev.pos):
                    pass
                elif button_back .collidepoint(ev.pos):
                    game_intro()


# 群組頁面
def group():
    Data.path = ''  # 路徑清空

    back = False
    # myphone = group_function.Android
    while not back:
        screen.fill(white)
        message_to_screen_side("群組頁面", green, 50, 50, 'medium')

        button_hot = button("誰是夯夯", 50, 100, 100, 50, dark, light)
        button_dot = button("誰是句點王", 250, 100, 100, 50, dark, light)
        button_active = button("活躍時間", 450, 100, 100, 50, dark, light)
        button_back = button("回首頁", 650, 100, 100, 50, dark, light)

        if Data.img == '誰是夯夯' or Data.img == '誰是句點王':
            screen.blit(Data.surf, (50, 175))  # 圖片擺放位置
            pg.display.flip()
        elif Data.img == '活躍時間':
            screen.blit(Data.surf_d, (30, 210))
            screen.blit(Data.surf_a, (400, 210))
            pg.display.flip()


        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_hot.collidepoint(ev.pos):
                    Data.surf = ios_android_function(Data.system, '誰是夯夯')  # 要呈現的圖片
                    Data.img = '誰是夯夯'

                elif button_dot.collidepoint(ev.pos):
                    Data.surf = ios_android_function(Data.system, '誰是句點王')
                    Data.img = '誰是句點王'

                elif button_active.collidepoint(ev.pos):
                    Data.surf_d, Data.surf_a = ios_android_function(Data.system, '活躍時間')
                    Data.img = '活躍時間'

                elif button_back.collidepoint(ev.pos):
                    game_intro()


# 基本設定（選擇手機系統、個人群組頁面）
def choice():
    back = False
    while not back:
        screen.fill(white)
        message_to_screen_center("基本設定", black, -220, 'medium')
        message_to_screen_side('您手機的系統為：', black, 250, 150)
        message_to_screen_side('輸入的對話紀錄為：', black, 250, 350)
        if Data.system != '':
            message_to_screen_side(Data.system, blue, 450, 150)
        if Data.individual_group != '':
            message_to_screen_side(Data.individual_group, blue, 450, 350)

        button_android = button("android", 250, 200, 100, 50, dark, light)
        button_ios = button("ios", 450, 200, 100, 50, dark, light)
        button_individual = button("個人聊天", 250, 400, 100, 50, dark, light)
        button_group = button("群組聊天", 450, 400, 100, 50, dark, light)
        button_back = button("回首頁", 50, 500, 100, 50, dark, light)
        button_start = button("開始分析", 650, 500, 100, 50, dark, light)

        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_ios.collidepoint(ev.pos):  # 按下ios
                    Data.system = 'ios'

                elif button_android.collidepoint(ev.pos):  # 按下android
                    Data.system = 'android'

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
                            if Data.system == 'ios':
                                ios_g.input_file(Data.path)
                            elif Data.system == 'android':
                                android_g.input_file(Data.path)

                            group()  # 群組頁面


# 遊戲首頁
def game_intro():
    intro = True
    while intro:

        Data.img = ''  # 現在要呈現的圖片名稱清空
        Data.individual_group = ''  # 群組或個人選擇清空
        Data.system = ''  # 系統選擇清空

        screen.fill(white)
        message_to_screen_center("歡迎來到遊戲", blue, -220, 'large')
        message_to_screen_center("使用說明", black, -130, 'medium')
        message_to_screen_center("請先確認您的手機為「24小時制」且為「中文版本」", red, -90)
        message_to_screen_center("再由「手機的line」匯出對話紀錄 txt.檔並儲存至您的電腦", black, -60)
        message_to_screen_center("點選「匯入資料」匯入您的對話紀錄，並根據手機系統點選「android」或「ios」", black, -30)
        message_to_screen_center("依據您的對話紀錄點選「個人聊天」或是「群組聊天」", black, 0)
        message_to_screen_center("就會進入對話紀錄分析的頁面囉！", black, 30)
        if Data.path == '':
            message_to_screen_center('*** 請匯入資料 ***', green, 150)
        else:
            message_to_screen_center('資料路徑：' + Data.path, light, 150)

        button_import = button("匯入資料", 350, 365, 100, 50, dark, light)
        button_quit = button("離開", 200, 500, 100, 50, dark, light)
        button_next = button("下一頁", 500, 500, 100, 50, dark, light)

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
