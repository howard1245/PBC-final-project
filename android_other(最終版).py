'''for Andorid 使用'''
import numpy as np
import matplotlib.pyplot as plt   # 資料視覺化套件
import matplotlib.font_manager
##################################################
# 資料處理 -> 資料長這樣[python日期時間, str日期, str時間, 人名, 內容]
from datetime import datetime
import datetime as dt
dateformat = "%Y/%m/%d"
dateFormatter = "%Y/%m/%d %H:%M"
timeformat = "%H:%M"

# imput file
path = input()
with open(file=path, mode="r", encoding="utf-8") as f:
    lines = f.readlines()

# 去除前2列沒用的資訊
lines = lines[2:]

for i in range(len(lines)):
    # get rid of "\n"
    lines[i] = lines[i].strip("\n")
    # 將每則訊息的元素分開變成list中的元素 一則訊息為一小list
    lines[i] = lines[i].split(sep="\t")

# 刪除空行和日期行
indexes = list()

# 在每則訊息前加上日期
for i in range(len(lines)):

    # 若找到空行 則在其後數行都加上日期元素
    if lines[i] == ['']:
        try:
            # date 把後面沒用的星期幾刪掉
            date = lines[i + 1][0][:-4]

            # 要再檢查日期是不是符合格式 因為有智障一則訊息裡包含空行
            datetime.strptime(date, dateformat)

            # 把空行和日期行位置append到indexes list中，等等加完日期就可以刪掉
            # 空行
            indexes.append(i)
            # 日期行
            indexes.append(i + 1)

            k = i + 2

            # 因為android版退群會是空行 所以要加個判斷 避免最後一則訊息是空行然後超出list長度
            if k + 1 <= len(lines):
                # 判斷其後數行是否為空行 否則持續迴圈 加上日期元素
                while lines[k] != ['']:
                    if k + 1 > len(lines):
                        break

                    lines[k].insert(0, date)  # date

                    if k + 1 == len(lines):
                        break

                    k += 1

        except ValueError:
            indexes.append(i)
            continue

# delete space and date elements
for index in sorted(indexes, reverse=True):
    del lines[index]

# 若錯誤代表有人一次傳很多行訊息(而且裡面可能還有空行)
# 直接刪掉就好 因為群組訊息我不需要做內容相關的功能 則數就夠了

# 長度4: 正常
# 此時訊息長度1(內容): 一則訊息內有數行 前一行是空行
# 此時訊息長度2(日期,內容): 一則訊息內有數行
# 此時訊息長度3(時間,人名,內容): 前面訊息有智障一次傳數行內有空行 所以沒讀到日期 等等解決
# 長度3(日期,時間,內容): 有人退群/有人收回訊息 直接刪除

# 加日期到沒日期的訊息
for i in range(len(lines)):
    try:
        datetemp = lines[i][0]
        datetime.strptime(datetemp, dateformat)
    except:
        lines[i].insert(0, date)  # date
    date = lines[i][0]

delete = list()
for i in range(len(lines)):
    if len(lines[i]) == 2 or len(lines[i]) == 3:
        delete.append(i)

# delete space and date elements
for index in sorted(delete, reverse=True):
    del lines[index]


# 日期和時間兩元素合併 然後轉格式
delete_indexes = list()
for i in range(len(lines)):
    datetimestr = lines[i][0] + " " + lines[i][1]
    dtformat = datetime.strptime(datetimestr, dateFormatter)
    lines[i].insert(0, dtformat)

# 刪掉一次多則訊息的剩下訊息
for index in sorted(delete_indexes, reverse=True):
    del lines[index]


##################################################

'''雙方貼圖次數圓餅圖'''
# 建立兩人名字的list
name = []
name.append(lines[0][3])
for i in range(len(lines)):
    if lines[i][3] != name[0]:
        name.append(lines[i][3])
        break
sticker_1 = 0
sticker_2 = 0
for i in range(len(lines)):
    if lines[i][3] == name[0]:  # 如果名字與第一人相同
        if lines[i][4] != "[貼圖]":  # 跳過不是貼圖的對話
            pass
        else:
            sticker_1 += 1  # 計算第一人字數
    if lines[i][3] == name[1]:  # 如果名字與第二人相同
        if lines[i][4] != "[貼圖]":  # 跳過不是貼圖的對話
            pass
        else:
            sticker_2 += 1  # 計算第二人字數
print(str(name[0]) + "貼圖數: " + str(sticker_1))
print(str(name[1]) + "貼圖數: " + str(sticker_2))
# 畫雙方貼圖數圓餅圖

plt.figure(figsize=(10, 6))  # 設定圖形大小
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

labels = [name[0], name[1]]  # 名字
sticker = [sticker_1, sticker_2]  # 貼圖數
plt.pie(sticker, labels=labels, autopct="%3.1f%%")
plt.title('從古至今雙方貼圖次數圓餅圖')  # 設定圖形標題
plt.legend(loc="best")
plt.show()

'''等待對方回覆的平均時間'''


def replytime(list_message):
    # dict item存list: [他人回話間隔時間(分鐘),別人有回過他的他的訊息次數,平均間隔時間(分鐘)]
    member = dict()
    for i in range(len(list_message)):
        # 除去最後一則訊息i+1超出index的情況
        if i + 1 < len(list_message):
            # 若下一個訊息是別人回話(但如果很久沒有聊天突然聊天的話的話就會讓回覆時間)
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

    return sorted_items


# 長條圖
reply_time = replytime(lines)
reply_timelist_1 = [name[0]]
reply_timelist_2 = [name[1]]
# print(reply_time[0][1][2])
for i in range(len(reply_time)):
    if reply_time[i][0] == name[0]:  # 第一人的名字
        reply_timelist_1.append(reply_time[i][1][2])
    if reply_time[i][0] == name[1]:  # 第二人的名字
        reply_timelist_2.append(reply_time[i][1][2])
print(str(name[0]) + "等待回覆的平均時間: " + str(round(reply_timelist_1[1], 2)))
print(str(name[1]) + "等待回覆的平均時間: " + str(round(reply_timelist_2[1], 2)))
# print(reply_timelist_1, reply_timelist_2)
# 匯入x y 字型資料
x_labels = np.array([reply_timelist_1[0], reply_timelist_2[0]])  # 名字
height = np.array([reply_timelist_1[1], reply_timelist_2[1]])  # 回覆時間
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
# 顯示圖例
plt.figure(figsize=(10, 6))  # 設定圖形大小
plt.bar(x_labels, height, width=0.3)
plt.title('等待對方回覆的平均時間')  # 設定圖形標題

plt.ylabel("平均回覆時間(分鐘)")  # 設定x軸標題
plt.show()
