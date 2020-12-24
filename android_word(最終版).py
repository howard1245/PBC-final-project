'''for Andorid 使用'''
from datetime import datetime
import matplotlib as mpl
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager

'''Notice:字數的list跟其他檔案不太一樣'''
dateformat = "%Y/%m/%d"
dateFormatter = "%Y/%m/%d %H:%M"
timeformat = "%H:%M"
calltimeformat = "%H:%M:%S"
# input file
# C:\Users\j3699\OneDrive\桌面\Chat history with 姍姐.txt
path = input()
with open(file=path, mode="r", encoding="utf-8") as f:
    lines_for_word = f.readlines()
# print(lines_for_word)

# 去除前2列沒用的資訊
lines_for_word = lines_for_word[2:]
for i in range(len(lines_for_word)):
    # get rid of "\n"
    lines_for_word[i] = lines_for_word[i].strip("\n")
    # 將每則訊息的元素分開變成list中的元素 一則訊息為一小list
    lines_for_word[i] = lines_for_word[i].split(sep="\t")
# print(lines_for_word)
# 刪除空行和日期行
indexes = list()

# 在每則訊息前加上日期
for i in range(len(lines_for_word)):

    # 若找到空行 則在其後數行都加上日期元素
    if lines_for_word[i] == ['']:
        try:
            # date 把後面沒用的星期幾刪掉
            date = lines_for_word[i + 1][0][:-4]

            # 要再檢查日期是不是符合格式 因為有智障一則訊息裡包含空行
            datetime.strptime(date, dateformat)

            # 把空行和日期行位置append到indexes list中，等等加完日期就可以刪掉
            # 空行
            indexes.append(i)
            # 日期行
            indexes.append(i + 1)

            k = i + 2
            # 因為android版退群會是空行 所以要加個判斷 避免最後一則訊息是空行然後超出list長度
            if k + 1 <= len(lines_for_word):
                # 判斷其後數行是否為空行 否則持續迴圈 加上日期元素
                while lines_for_word[k] != ['']:
                    if k + 1 > len(lines_for_word):
                        break

                    lines_for_word[k].insert(0, date)  # date

                    if k + 1 == len(lines_for_word):
                        break

                    k += 1

        except ValueError:
            indexes.append(i)
            continue

# delete space and date elements
for index in sorted(indexes, reverse=True):
    del lines_for_word[index]

# 若錯誤代表有人一次傳很多行訊息(而且裡面可能還有空行)
# 直接刪掉就好 因為群組訊息我不需要做內容相關的功能 則數就夠了

# 長度4: 正常
# 此時訊息長度1(內容): 一則訊息內有數行 前一行是空行
# 此時訊息長度2(日期,內容): 一則訊息內有數行
# 此時訊息長度3(時間,人名,內容): 前面訊息有智障一次傳數行內有空行 所以沒讀到日期 等等解決
# 長度3(日期,時間,內容): 有人退群/有人收回訊息 直接刪除

# 加日期到沒日期的訊息
for i in range(len(lines_for_word)):
    try:
        datetemp = lines_for_word[i][0]
        datetime.strptime(datetemp, dateformat)
    except:
        lines_for_word[i].insert(0, date)  # date
    date = lines_for_word[i][0]
# print(lines_for_word)
delete = list()
for i in range(len(lines_for_word)):
    if len(lines_for_word[i]) == 2:  # 補回用換行的文字內容
        lines_for_word[i].insert(1, lines_for_word[i-1][1])
        lines_for_word[i].insert(2, lines_for_word[i-1][2])
    if len(lines_for_word[i]) == 3:
        lines_for_word[i][1] = lines_for_word[i-1][1]
        lines_for_word[i].insert(2, lines_for_word[i-1][2])

# delete space and date elements
for index in sorted(delete, reverse=True):
    del lines_for_word[index]


# 日期和時間兩元素合併 然後轉格式
delete_indexes = list()
for i in range(len(lines_for_word)):
    datetimestr = lines_for_word[i][0] + " " + lines_for_word[i][1]
    dtformat = datetime.strptime(datetimestr, dateFormatter)
    lines_for_word[i].insert(0, dtformat)

# 刪掉一次多則訊息的剩下訊息
for index in sorted(delete_indexes, reverse=True):
    del lines_for_word[index]
# print(len(lines_for_word))
# print(lines_for_word)
########################################
'''雙方各別總字數圓餅圖'''


def pie_words(list_message):
    # 建立兩人名字的list
    name = []
    name.append(list_message[0][3])
    for i in range(len(list_message)):
        if list_message[i][3] != name[0]:
            name.append(list_message[i][3])
            break

    word_1 = 0  # 第一人的字數
    word_2 = 0  # 第二人的字數
    for i in range(len(list_message)):
        if list_message[i][3] == name[0]:  # 如果名字與第一人相同
            if list_message[i][4] == "[貼圖]"\
               or list_message[i][4] == "[照片]"\
               or list_message[i][4] == "[影片]"\
               or list_message[i][4] == "[語音訊息]"\
               or list_message[i][4] == "[檔案]"\
               or list_message[i][4] == "未接來電"\
               or list_message[i][4] == "相簿建立成功"\
               or list_message[i][4] == "[聯絡資訊]"\
               or list_message[i][4] == "[位置資訊]"\
               or list_message[i][4][0:4] == "通話時間"\
               or list_message[i][4] == "您已結束通話"\
               or list_message[i][4] == "[禮物]"\
               or list_message[i][4] == "無人接聽":
                pass
            else:
                word_1 += len(list_message[i][4])  # 計算第一人字數
        if list_message[i][3] == name[1]:  # 如果名字與第二人相同
            if list_message[i][4] == "[貼圖]"\
               or list_message[i][4] == "[照片]"\
               or list_message[i][4] == "[影片]"\
               or list_message[i][4] == "[語音訊息]"\
               or list_message[i][4] == "[檔案]"\
               or list_message[i][4] == "未接來電"\
               or list_message[i][4] == "相簿建立成功"\
               or list_message[i][4] == "[聯絡資訊]"\
               or list_message[i][4] == "[位置資訊]"\
               or list_message[i][4][0:4] == "通話時間"\
               or list_message[i][4] == "您已結束通話"\
               or list_message[i][4] == "[禮物]"\
               or list_message[i][4] == "無人接聽":
                pass
            else:
                word_2 += len(list_message[i][4])  # 計算第二人字數

    return [word_1, word_2, name]


totalwords = pie_words(lines_for_word)
# print(totalwords)[7493, 11004, ['映權姑姑', '昀真']]
# 畫雙方字數圓餅圖
plt.figure(figsize=(10, 6))  # 設定圖形大小
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']  # 匯入中文字型
labels = [totalwords[2][0], totalwords[2][1]]  # 名字list
word = [totalwords[0], totalwords[1]]  # 字數list
plt.pie(word, labels=labels, autopct="%3.1f%%")
plt.title('從古至今雙方總字數圓餅圖')  # 設定圖形標題
plt.legend(loc="best")
plt.show()

'''近30日雙方總字數折線圖'''


def linechart_words(list_message):

    name = []
    name.append(list_message[0][3])
    for i in range(len(list_message)):
        if list_message[i][3] != name[0]:
            name.append(list_message[i][3])
            break
    member_1_msglist = []
    member_2_msglist = []
    for i in range(len(list_message)):
        if list_message[i][3] == name[0]:
            member_1_msglist.append(list_message[i])
        else:
            member_1_msglist.append(list_message[i])
    for i in range(len(list_message)):
        if list_message[i][3] == name[1]:
            member_2_msglist.append(list_message[i])
        else:
            member_2_msglist.append(list_message[i])

    # 第一則訊息絕對日期
    origin_1 = datetime.date(member_1_msglist[0][0])
    last_1 = datetime.date(member_1_msglist[- 1][0])
    passday_1 = (last_1 - origin_1).days + 1

    origin_2 = datetime.date(member_2_msglist[0][0])
    last_2 = datetime.date(member_2_msglist[- 1][0])
    passday_2 = (last_2 - origin_2).days + 1
    # 做每天天數的list
    interval_1 = []
    interval_2 = []
    for i in range(passday_1):
        interval_1.append(i + 1)

    for i in range(passday_2):
        interval_2.append(i + 1)

    # dict 天數:[每日字數, 日期]
    day_1 = dict()
    for i in interval_1:
        day_1[i] = [0, str(datetime.date(member_1_msglist[0][0] + dt.timedelta(days=i-1)))]

    day_2 = dict()
    for i in interval_2:
        day_2[i] = [0, str(datetime.date(member_2_msglist[0][0] + dt.timedelta(days=i-1)))]

    # 加總每天有多少字數
    for i in range(len(member_1_msglist)):
        if member_1_msglist[i][3] == name[0]:
            if list_message[i][4] == "[貼圖]"\
               or list_message[i][4] == "[照片]"\
               or list_message[i][4] == "[影片]"\
               or list_message[i][4] == "[語音訊息]"\
               or list_message[i][4] == "[檔案]"\
               or list_message[i][4] == "未接來電"\
               or list_message[i][4] == "相簿建立成功"\
               or list_message[i][4] == "[聯絡資訊]"\
               or list_message[i][4] == "[位置資訊]"\
               or list_message[i][4][0:4] == "通話時間"\
               or list_message[i][4] == "您已結束通話"\
               or list_message[i][4] == "[禮物]"\
               or list_message[i][4] == "無人接聽":
                pass
            else:
                d1 = (member_1_msglist[i][0] - datetime.strptime(str(origin_1), "%Y-%m-%d")).days
                day_1[d1 + 1][0] += len(member_1_msglist[i][4])

    for i in range(len(member_2_msglist)):
        if member_1_msglist[i][3] == name[1]:
            if list_message[i][4] == "[貼圖]"\
               or list_message[i][4] == "[照片]"\
               or list_message[i][4] == "[影片]"\
               or list_message[i][4] == "[語音訊息]"\
               or list_message[i][4] == "[檔案]"\
               or list_message[i][4] == "未接來電"\
               or list_message[i][4] == "相簿建立成功"\
               or list_message[i][4] == "[聯絡資訊]"\
               or list_message[i][4] == "[位置資訊]"\
               or list_message[i][4][0:4] == "通話時間"\
               or list_message[i][4] == "您已結束通話"\
               or list_message[i][4] == "[禮物]"\
               or list_message[i][4] == "無人接聽":
                pass
            else:
                d2 = (member_2_msglist[i][0] - datetime.strptime(str(origin_2), "%Y-%m-%d")).days
                day_2[d2 + 1][0] += len(member_1_msglist[i][4])

    # 取近30日的字數
    month_1 = list(day_1.values())[-30:]  # 第一個人的近30日的總字數
    month_2 = list(day_2.values())[-30:]  # 第二個人的近30日的總字數

    member_date_1 = []
    member_word_1 = []
    for i in range(len(month_1)):
        # 第一人的日期
        member_date_1.append(month_1[i][1])
        # 第一人總字數訊息
        member_word_1.append(month_1[i][0])

    member_date_2 = []
    member_word_2 = []
    for i in range(len(month_2)):
        # 第二人的日期
        member_date_2.append(month_2[i][1])
        # 第二人總字數訊息
        member_word_2.append(month_2[i][0])
    return [member_date_1, member_word_1, member_date_2, member_word_2, name]


both_totalwords = linechart_words(lines_for_word)
# print(both_totalwords)
# 折線圖
plt.figure(figsize=(12, 6))  # 設定圖形大小
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']  # 匯入中文字型
plt.xticks(fontsize=8)  # x軸刻度大小
plt.yticks(fontsize=8)  # y軸刻度大小
plt.plot(both_totalwords[0], both_totalwords[1], marker='o', ms=5, label=str(both_totalwords[4][0]) + "的近30日總字數")
plt.plot(both_totalwords[2], both_totalwords[3], marker='s', ms=5, label=str(both_totalwords[4][1]) + "的近30日總字數")
plt.xticks(rotation=45,  ha='right')
# 顯示圖例
plt.legend(loc='best', fontsize=10)
plt.title('近30日雙方總字數折線圖')  # 設定圖形標題
plt.ylabel("字數", fontsize=10)  # 設定y軸標題
# 顯示圖形
plt.show()
