import pygame as pg
from datetime import datetime
import matplotlib
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager
import matplotlib.backends.backend_agg as agg


dateformat = "%Y/%m/%d"
dateFormatter = "%Y/%m/%d %H:%M"
timeformat = "%H:%M"


# ios系統的群組功能
class Ios:
    lines = ''

    # 匯入檔案
    def input_file(self, path):
        with open(file=path, mode="r", encoding="utf-8") as f:
            Ios.lines = f.readlines()
        # 去除前2列沒用的資訊
        Ios.lines = Ios.lines[2:]
        # print(lines)

        for i in range(len(Ios.lines)):
            # get rid of "\n"
            Ios.lines[i] = Ios.lines[i].strip("\n")
            # 將每則訊息的元素分開變成list中的元素 一則訊息為一小list
            Ios.lines[i] = Ios.lines[i].split(sep="\t")
        # print(lines)

        # 刪除空行和日期行
        indexes = list()

        # 在每則訊息前加上日期
        for i in range(len(Ios.lines)):

            # 若找到空行 則在其後數行都加上日期元素
            if Ios.lines[i] == ['']:
                try:
                    # date 把後面沒用的星期幾刪掉
                    date = Ios.lines[i + 1][0][:-3]

                    # 要再檢查日期是不是符合格式 因為有智障一則訊息裡包含空行
                    datetime.strptime(date, dateformat)

                    # 把空行和日期行位置append到indexes list中，等等加完日期就可以刪掉
                    # 空行
                    indexes.append(i)
                    # 日期行
                    indexes.append(i + 1)

                    k = i + 2

                    # 判斷其後數行是否為空行 否則持續迴圈 加上日期元素
                    while Ios.lines[k] != ['']:
                        if k + 1 > len(Ios.lines):
                            break

                        Ios.lines[k].insert(0, date)  # date

                        if k + 1 == len(Ios.lines):
                            break

                        k += 1

                except ValueError:
                    indexes.append(i)
                    continue

        # delete space and date elements
        for index in sorted(indexes, reverse=True):
            del Ios.lines[index]

        # 若錯誤代表有人一次傳很多行訊息(而且裡面可能還有空行)
        # 直接刪掉就好 因為群組訊息我不需要做內容相關的功能 則數就夠了

        # 長度4: 正常
        # 此時訊息長度1(內容): 一則訊息內有數行 前一行是空行
        # 此時訊息長度2(日期,內容): 一則訊息內有數行
        # 此時訊息長度3(時間,人名,內容): 前面訊息有智障一次傳數行內有空行 所以沒讀到日期 等等解決
        # 長度3(日期,時間,內容): 有人退群/有人收回訊息 直接刪除

        # 加日期到沒日期的訊息
        for i in range(len(Ios.lines)):
            try:
                datetemp = Ios.lines[i][0]
                datetime.strptime(datetemp, dateformat)
            except:
                Ios.lines[i].insert(0, date)  # date
            date = Ios.lines[i][0]

        delete = list()
        for i in range(len(Ios.lines)):
            if len(Ios.lines[i]) == 2 or len(Ios.lines[i]) == 3:
                delete.append(i)

        # delete space and date elements
        for index in sorted(delete, reverse=True):
            del Ios.lines[index]

        # 日期和時間兩元素合併 然後轉格式
        delete_indexes = list()
        for i in range(len(Ios.lines)):
            datetimestr = Ios.lines[i][0] + " " + Ios.lines[i][1]
            dtformat = datetime.strptime(datetimestr, dateFormatter)
            Ios.lines[i].insert(0, dtformat)

        # 刪掉一次多則訊息的剩下訊息
        for index in sorted(delete_indexes, reverse=True):
            del Ios.lines[index]

    '''誰是夯夯(訊息則數) -> 資料長這樣 list裡有tuple = [("人名", 訊息則數), ("人名", 訊息則數)...]
        # [4]名字 [5]內容'''
    def hot_function(self):
        def hot(list_message):
            member = dict()
            for i in range(len(list_message)):
                name = list_message[i][3]

                if name in member:
                    member[name] += 1
                else:
                    member[name] = 1

            sorted_items = sorted(member.items(), key=lambda x: x[1], reverse=True)

            # 只取前8名 到時候介面可以呈現大的第一名第二名第三名 其他五名用列表小字
            sorted_items = sorted_items[0:8]
            return sorted_items

        # 畫圖
        hot = hot(Ios.lines)
        hot_name = []  # 前八名姓名
        hot_times = []  # 前八名的訊息數
        for i in range(len(hot)):
            hot_name.append(hot[i][0])
            hot_times.append(hot[i][1])

        fig_hot = plt.figure(figsize=(7.5, 4.5))  # 設定圖片大小
        x_labels = np.array(hot_name)  # 人名
        height = np.array(hot_times)  # 總回應數
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        plt.title('誰是夯夯')  # 設定圖形標題
        plt.bar(x_labels, height, width=0.5, color=['coral', 'orange', 'gold', 'lightgreen', 'turquoise', 'lightblue',
                                                    'lavender', 'plum'])

        plt.ylabel("總回應則數")  # 設定y軸標題
        canvas = agg.FigureCanvasAgg(fig_hot)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")
        text = hot_name[0]
        return surf, text

        # plt.show()
        # print(hot_name, hot_times)
        # print(hot(lines))

    '''誰是句點王（個人發言後，平均別人回話時間間隔最長者'''
    def dot_function(self):
        def dot(list_message):
            # dict item存list: [他人回話間隔時間(分鐘),別人有回過他的他的訊息次數,平均間隔時間(分鐘)]
            member = dict()
            for i in range(len(list_message)):
                # 除去最後一則訊息i+1超出index的情況
                if i + 1 < len(list_message):
                    # 若下一個訊息是別人回話
                    if list_message[i + 1][3] != list_message[i][3]:
                        name = list_message[i][3]

                        if name in member:
                            time = (list_message[i + 1][0] - list_message[i][0]).seconds / 60
                            member[name][1] += 1
                            member[name][0] += time
                        else:
                            time = (list_message[i + 1][0] - list_message[i][0]).seconds / 60
                            member[name] = [time, 1, 0]

            for i in member:
                member[i][2] = (member[i][0] / member[i][1])

            sorted_items = sorted(member.items(), key=lambda x: x[1][2], reverse=True)

            # 也可以反過來取大家回覆速度最快的人 -> 誰是夯夯
            # 只取前8名 到時候介面可以呈現大的第一名第二名第三名 其他五名用列表小字
            sorted_items = sorted_items[0:8]
            return sorted_items

        dot = dot(Ios.lines)
        # print(dot(lines))
        dot_name = []
        dot_time = []
        for i in range(len(dot)):
            dot_name.append(dot[i][0])
            dot_time.append(round(dot[i][1][2], 2))  # 四捨五入取到小數點後兩位
        # print(dot_name, dot_time)
        x_labels = np.array(dot_name)  # 人名
        height = np.array(dot_time)  # 每日平均被回話時間
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        # 設定圖片大小標題
        fig_dot = plt.figure(figsize=(7.5, 4.5))  # 設定圖片大小
        plt.title('誰是句點王')  # 設定圖形標題
        plt.bar(x_labels, height, width=0.5, color=['coral', 'orange', 'gold', 'lightgreen', 'turquoise', 'lightblue',
                                                    'lavender', 'plum'])
        plt.ylabel("每日平均被回話時間(分鐘)")  # 設定y軸標題
        canvas = agg.FigureCanvasAgg(fig_dot)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")
        text = dot_name[0]
        return surf, text
        # plt.show()

    ##################################################
    '''# 單日24小時，各時段平均訊息數（折線圖）'''
    def day_function(self):
        def day(list_message):
            origin = datetime.date(list_message[0][0])
            last = datetime.date(list_message[- 1][0])
            passday = (last - origin).days + 1

            time = dict()
            for i in range(24):
                time[i] = 0
            # 做每個小時的絕對時間的list
            interval = list()
            for i in range(24):
                hh = str()
                if i < 10:
                    hh = "0" + str(i)
                else:
                    hh = str(i)
                interval.append(datetime.strptime(hh + ":00", timeformat))

            # 加總每小時有多少則訊息
            for i in range(len(list_message)):
                for j in interval:
                    if (list_message[i][0] - j).seconds / 60 / 60 < 1:
                        hour = (j - datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).seconds / 60 / 60
                        time[hour] += 1
            msg_perhour = []
            perhour = []
            for i in range(len(time)):
                msg_perhour.append(time[i] / passday)
            for i in range(24):
                perhour.append(i)
            return [msg_perhour, perhour]

        # print(day(lines))
        # 畫長條圖
        day = day(Ios.lines)
        x_labels = np.array(day[1])  # 每個小時
        height = np.array(day[0])  # 總回應則數
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        fig_day = plt.figure(figsize=(4, 4))  # 設定圖片大小
        plt.title('24小時平均訊息數長條圖')  # 設定圖形標題
        plt.bar(x_labels, height, width=0.5)

        plt.ylabel("訊息數")  # 設定x軸標題
        plt.xlim((-0.5, 24))
        canvas = agg.FigureCanvasAgg(fig_day)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")
        # plt.show()
        return surf

    '''# 從古至今聊天訊息數'''
    def active_function(self):
        def past(list_message):
            # 第一則訊息絕對日期
            origin = datetime.date(list_message[0][0])
            last = datetime.date(list_message[- 1][0])
            passday = (last - origin).days + 1

            # 做每天天數的list
            interval = list()
            for i in range(passday):
                interval.append(i + 1)

            # dict 天數:[每日訊息則數, 日期]
            day = dict()
            for i in interval:
                day[i] = [0, str(datetime.date(list_message[0][0] + dt.timedelta(days=i - 1)))]

            # 加總每天有多少則訊息
            for i in range(len(list_message)):
                d = (list_message[i][0] - datetime.strptime(str(origin), "%Y-%m-%d")).days
                day[d + 1][0] += 1

            day_value = list(day.values())

            date = []
            msg = []
            for i in range(len(day)):
                date.append(day_value[i][1])  # 日期list
                msg.append(day_value[i][0])  # 訊息數list

            # 荒廢群組(大於指定時間未回訊息次數或近30天每日訊息量(訊息間隔))
            text = str()
            total = 0
            for i in list(day.values())[-30:]:
                if i[0] == 0:
                    total += 1
                if total == 30:
                    text = "群組有點荒廢了喔QQ"

            sorted_items = sorted(day.items(), key=lambda x: x[1][0], reverse=True)
            sorted_items_most = sorted_items[0:5]

            return [date, msg, text, sorted_items_most]

        past_msg = past(Ios.lines)
        # print(past_msg[3][0][0])
        # print(past_msg)
        if past_msg[2] != "":  # 荒廢文字
            print(str(past_msg[2]))

        # 畫長條圖
        fig_active = plt.figure(figsize=(4, 4))  # 設定圖片大小
        x_labels = np.array(past_msg[0])  # 過去到現在的時間

        height = np.array(past_msg[1])  # 訊息數
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        plt.title('從古至今聊天訊息數')  # 設定圖形標題
        plt.bar(x_labels, height, width=1, color='CornflowerBlue')

        plt.ylabel("訊息數")  # 設定y軸標題
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        # plt.show()
        '''想要顯示日期 但如果特別高峰的前五名太集中日期會擠在一起
        my_xticks = ax.get_xticks() 
        tmp = []
        for i in range(5):
            tmp.append(my_xticks[past_msg[3][i][0]])
        plt.xticks(tmp, visible=True) 
        plt.xticks(rotation=45,  ha='right', fontsize=5)'''
        canvas = agg.FigureCanvasAgg(fig_active)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")
        return surf, past_msg[2]


# android系統的群組功能
class Android:
    lines = ''

    # 匯入及處理檔案
    def input_file(self, path):
        with open(file=path, mode="r", encoding="utf-8") as f:
            Android.lines = f.readlines()

        # 去除前2列沒用的資訊
        Android.lines = Android.lines[2:]
        # print(lines)

        for i in range(len(Android.lines)):
            # get rid of "\n"
            Android.lines[i] = Android.lines[i].strip("\n")
            # 將每則訊息的元素分開變成list中的元素 一則訊息為一小list
            Android.lines[i] = Android.lines[i].split(sep="\t")
        # print(lines)

        # 刪除空行和日期行
        indexes = list()

        # 在每則訊息前加上日期
        for i in range(len(Android.lines)):

            # 若找到空行 則在其後數行都加上日期元素
            if Android.lines[i] == ['']:
                try:
                    # date 把後面沒用的星期幾刪掉
                    date = Android.lines[i + 1][0][:-4]

                    # 要再檢查日期是不是符合格式 因為有智障一則訊息裡包含空行
                    datetime.strptime(date, dateformat)

                    # 把空行和日期行位置append到indexes list中，等等加完日期就可以刪掉
                    # 空行
                    indexes.append(i)
                    # 日期行
                    indexes.append(i + 1)

                    k = i + 2

                    # 因為android版退群會是空行 所以要加個判斷 避免最後一則訊息是空行然後超出list長度
                    if k + 1 <= len(Android.lines):

                        # 判斷其後數行是否為空行 否則持續迴圈 加上日期元素
                        while Android.lines[k] != ['']:

                            if k + 1 > len(Android.lines):
                                break

                            Android.lines[k].insert(0, date)  # date

                            if k + 1 == len(Android.lines):
                                break

                            k += 1

                except ValueError:
                    indexes.append(i)
                    continue

        # delete space and date elements
        for index in sorted(indexes, reverse=True):
            del Android.lines[index]

        # 若錯誤代表有人一次傳很多行訊息(而且裡面可能還有空行)
        # 直接刪掉就好 因為群組訊息我不需要做內容相關的功能 則數就夠了

        # 長度4: 正常
        # 此時訊息長度1(內容): 一則訊息內有數行 前一行是空行
        # 此時訊息長度2(日期,內容): 一則訊息內有數行
        # 此時訊息長度3(時間,人名,內容): 前面訊息有智障一次傳數行內有空行 所以沒讀到日期 等等解決
        # 長度3(日期,時間,內容): 有人退群/有人收回訊息 直接刪除

        # 加日期到沒日期的訊息
        for i in range(len(Android.lines)):
            try:
                datetemp = Android.lines[i][0]
                datetime.strptime(datetemp, dateformat)
            except:
                Android.lines[i].insert(0, date)  # date
            date = Android.lines[i][0]

        delete = list()
        for i in range(len(Android.lines)):
            if len(Android.lines[i]) == 2 or len(Android.lines[i]) == 3:
                delete.append(i)

        # delete space and date elements
        for index in sorted(delete, reverse=True):
            del Android.lines[index]

        # 日期和時間兩元素合併 然後轉格式
        delete_indexes = list()
        for i in range(len(Android.lines)):
            datetimestr = Android.lines[i][0] + " " + Android.lines[i][1]
            dtformat = datetime.strptime(datetimestr, dateFormatter)
            Android.lines[i].insert(0, dtformat)

        # 刪掉一次多則訊息的剩下訊息
        for index in sorted(delete_indexes, reverse=True):
            del Android.lines[index]

    '''誰是夯夯(訊息則數) -> 資料長這樣 list裡有tuple = [("人名", 訊息則數), ("人名", 訊息則數)...]
    # [4]名字 [5]內容'''
    def hot_function(self):
        def hot(list_message):
            member = dict()
            for i in range(len(list_message)):
                name = list_message[i][3]

                if name in member:
                    member[name] += 1
                else:
                    member[name] = 1

            sorted_items = sorted(member.items(), key=lambda x: x[1], reverse=True)

            # 只取前8名 到時候介面可以呈現大的第一名第二名第三名 其他五名用列表小字
            sorted_items = sorted_items[0:8]
            return sorted_items

        # 畫圖
        hot = hot(Android.lines)
        hot_name = []  # 前八名姓名
        hot_times = []  # 前八名的訊息數
        for i in range(len(hot)):
            hot_name.append(hot[i][0])
            hot_times.append(hot[i][1])

        fig_hot = plt.figure(figsize=(7.5, 4.5))  # 設定圖片大小
        x_labels = np.array(hot_name)  # 人名
        height = np.array(hot_times)  # 總回應數
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        plt.title('誰是夯夯')  # 設定圖形標題
        plt.bar(x_labels, height, width=0.5, color=['coral', 'orange', 'gold', 'lightgreen', 'turquoise', 'lightblue',
                                                    'lavender', 'plum'])

        plt.ylabel("總回應則數")  # 設定y軸標題
        canvas = agg.FigureCanvasAgg(fig_hot)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")
        text = hot_name[0]
        return surf, text
        # plt.show()
        # print(hot_name, hot_times)
        # print(hot(lines))

    '''誰是句點王（個人發言後，平均別人回話時間間隔最長者'''
    def dot_function(self):
        # 資料長這樣 -> [('Alyssa 盈慧', [868.0, 1, 868.0]), ('Sophia Meow', [2584.0, 5, 516.8])...]
        # (人名, [總回話間隔(分鐘), 總訊息則數, 平均回話間隔(分鐘)]

        def dot(list_message):
            # dict item存list: [他人回話間隔時間(分鐘),別人有回過他的他的訊息次數,平均間隔時間(分鐘)]
            member = dict()
            for i in range(len(list_message)):
                # 除去最後一則訊息i+1超出index的情況
                if i + 1 < len(list_message):
                    # 若下一個訊息是別人回話
                    if list_message[i + 1][3] != list_message[i][3]:
                        name = list_message[i][3]

                        if name in member:
                            time = (list_message[i + 1][0] - list_message[i][0]).seconds / 60
                            member[name][1] += 1
                            member[name][0] += time
                        else:
                            time = (list_message[i + 1][0] - list_message[i][0]).seconds / 60
                            member[name] = [time, 1, 0]

            for i in member:
                member[i][2] = (member[i][0] / member[i][1])

            sorted_items = sorted(member.items(), key=lambda x: x[1][2], reverse=True)

            # 也可以反過來取大家回覆速度最快的人 -> 誰是夯夯
            # 只取前8名 到時候介面可以呈現大的第一名第二名第三名 其他五名用列表小字
            sorted_items = sorted_items[0:8]
            return sorted_items

        dot = dot(Android.lines)
        # print(dot(lines))
        dot_name = []
        dot_time = []
        for i in range(len(dot)):
            dot_name.append(dot[i][0])
            dot_time.append(round(dot[i][1][2], 2))  # 四捨五入取到小數點後兩位
        # print(dot_name, dot_time)
        x_labels = np.array(dot_name)  # 人名
        height = np.array(dot_time)  # 每日平均被回話時間
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        # 設定圖片大小標題
        fig_dot = plt.figure(figsize=(7.5, 4.5))  # 設定圖片大小
        plt.title('誰是句點王')  # 設定圖形標題
        plt.bar(x_labels, height, width=0.5, color=['coral', 'orange', 'gold', 'lightgreen', 'turquoise', 'lightblue',
                                                    'lavender', 'plum'])
        plt.ylabel("每日平均被回話時間(分鐘)")  # 設定y軸標題
        canvas = agg.FigureCanvasAgg(fig_dot)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")
        text = dot_name[0]
        return surf, text
        # plt.show()

    ##################################################
    '''# 單日24小時，各時段平均訊息數（折線圖）'''
    def day_function(self):
        def day(list_message):
            origin = datetime.date(list_message[0][0])
            last = datetime.date(list_message[- 1][0])
            passday = (last - origin).days + 1

            time = dict()
            for i in range(24):
                time[i] = 0
            # 做每個小時的絕對時間的list
            interval = list()
            for i in range(24):
                hh = str()
                if i < 10:
                    hh = "0" + str(i)
                else:
                    hh = str(i)
                interval.append(datetime.strptime(hh + ":00", timeformat))

            # 加總每小時有多少則訊息
            for i in range(len(list_message)):
                for j in interval:
                    if (list_message[i][0] - j).seconds / 60 / 60 < 1:
                        hour = (j - datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).seconds / 60 / 60
                        time[hour] += 1
            msg_perhour = []
            perhour = []
            for i in range(len(time)):
                msg_perhour.append(time[i] / passday)
            for i in range(24):
                perhour.append(i)
            return [msg_perhour, perhour]

        # print(day(lines))
        # 畫長條圖
        day = day(Android.lines)
        x_labels = np.array(day[1])  # 每個小時
        height = np.array(day[0])  # 總回應則數
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        fig_day = plt.figure(figsize=(4, 3))  # 設定圖片大小
        plt.title('24小時平均訊息數長條圖')  # 設定圖形標題
        plt.bar(x_labels, height, width=0.5, color='CornflowerBlue')

        plt.ylabel("訊息數")  # 設定x軸標題
        plt.xlim((-0.5, 24))
        canvas = agg.FigureCanvasAgg(fig_day)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")
        return surf
        # plt.show()

    '''# 從古至今聊天訊息數'''
    def active_function(self):
        # dict資料長這樣 (從第一天至今第幾天:[幾則訊息, 日期].....) 848: [0, '2020-11-22'], 849: [4, '2020-11-23'], 850: [1, '2020-11-24']}

        def past(list_message):
            # 第一則訊息絕對日期
            origin = datetime.date(list_message[0][0])
            last = datetime.date(list_message[- 1][0])
            passday = (last - origin).days + 1

            # 做每天天數的list
            interval = list()
            for i in range(passday):
                interval.append(i + 1)

            # dict 天數:[每日訊息則數, 日期]
            day = dict()
            for i in interval:
                day[i] = [0, str(datetime.date(list_message[0][0] + dt.timedelta(days=i - 1)))]

            # 加總每天有多少則訊息
            for i in range(len(list_message)):
                d = (list_message[i][0] - datetime.strptime(str(origin), "%Y-%m-%d")).days
                day[d + 1][0] += 1

            day_value = list(day.values())

            date = []
            msg = []
            for i in range(len(day)):
                date.append(day_value[i][1])  # 日期list
                msg.append(day_value[i][0])  # 訊息數list

            # 荒廢群組(大於指定時間未回訊息次數或近30天每日訊息量(訊息間隔))
            text = str()
            total = 0
            for i in list(day.values())[-30:]:
                if i[0] == 0:
                    total += 1
                if total == 30:
                    text = "群組有點荒廢了喔QQ"

            sorted_items = sorted(day.items(), key=lambda x: x[1][0], reverse=True)
            sorted_items_most = sorted_items[0:5]

            return [date, msg, text, sorted_items_most]

        past_msg = past(Android.lines)
        # print(past_msg[3][0][0])
        # print(past_msg)
        if past_msg[2] != "":
            print(str(past_msg[2]))

        # 畫長條圖
        fig_active = plt.figure(figsize=(4, 3))  # 設定圖片大小
        x_labels = np.array(past_msg[0])  # 過去到現在的時間

        height = np.array(past_msg[1])  # 訊息數
        plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

        plt.title('從古至今聊天訊息數')  # 設定圖形標題
        plt.bar(x_labels, height, width=1, color='CornflowerBlue')

        plt.ylabel("訊息數")  # 設定y軸標題
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        canvas = agg.FigureCanvasAgg(fig_active)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pg.image.fromstring(raw_data, size, "RGB")

        '''想要顯示日期 但如果特別高峰的前五名太集中日期會擠在一起
        my_xticks = ax.get_xticks() 
        tmp = []
        for i in range(5):
            tmp.append(my_xticks[past_msg[3][i][0]])
        plt.xticks(tmp, visible=True) 
        plt.xticks(rotation=45,  ha='right', fontsize=5)'''
        # plt.show()
        return surf, past_msg[2]


# myphone = Android()
# myphone.input_file()
# myphone.hot_function()
# myphone.dot_function()
# myphone.day_function()
# myphone.active_function()


