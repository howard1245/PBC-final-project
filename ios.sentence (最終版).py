from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
dateformat = "%Y/%m/%d"
dateFormatter = "%Y/%m/%d %H:%M"
timeformat = "%H:%M"
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

# input file
path = input()
with open(file=path, mode="r", encoding="utf-8", errors='ignore') as f:
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
            date = lines[i + 1][0][:-3]

            # 要再檢查日期是不是符合格式 因為有智障一則訊息裡包含空行
            datetime.strptime(date, dateformat)

            # 把空行和日期行位置append到indexes list中，等等加完日期就可以刪掉
            # 空行
            indexes.append(i)
            # 日期行
            indexes.append(i + 1)

            k = i + 2

            # 判斷其後數行是否為空行 否則持續迴圈 加上日期元素
            while lines[k] != ['']:
                if k + 1 > len(lines):
                    break

                lines[k].insert(0, date) # date

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
# print(lines)  # ['2018/10/02', '18:21', '昀真', '你去球場了嗎']

# 日期和時間兩元素合併 然後轉格式
delete_indexes = list()
for i in range(len(lines)):
    datetimestr = lines[i][0] + " " + lines[i][1]
    dtformat = datetime.strptime(datetimestr, dateFormatter)
    lines[i].insert(0, dtformat)

# 刪掉一次多則訊息的剩下訊息
for index in sorted(delete_indexes, reverse=True):
    del lines[index]
# print(lines) #  [datetime.datetime(2018, 10, 2, 18, 21), '2018/10/02', '18:21', '昀真', '你去球場了嗎']


def sentence(list_message):
    member = dict()
    for i in range(len(list_message)):
        name = list_message[i][3]

        if name in member:
            member[name] += 1
        else:
            member[name] = 1

    sorted_items = sorted(member.items(), key=lambda x: x[1], reverse=True)

    # 只取前8名 到時候介面可以呈現大的第一名第二名第三名 其他五名用列表小字

    return sorted_items


sent = sentence(lines)
for key, value in sent:
    print(str(key) + "回覆則數: " + str(value))

# 畫雙方回覆則數圓餅圖
fig_word = plt.figure()
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
labels = [sent[0][0], sent[1][0]]
sentences = [sent[0][1], sent[1][1]]
explode = [0, 0]  # 0則不突凸出，值越大 則凸出越大
plt.pie(sentences, explode=explode, labels=labels, autopct="%3.1f%%")
plt.title('雙方回覆則數比例')  # 設定圖形標題

plt.legend(loc="best")
plt.show()

'''近30日雙方總回應則數折線圖'''


def total_msg(list_message):
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

    # 分別抓兩個人的第一則訊息絕對日期
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

    # dict 天數:[每日訊息則數, 日期]
    day_1 = dict()
    for i in interval_1:
        day_1[i] = [0, str(datetime.date(member_1_msglist[0][0] + dt.timedelta(days=i - 1)))]

    day_2 = dict()
    for i in interval_2:
        day_2[i] = [0, str(datetime.date(member_2_msglist[0][0] + dt.timedelta(days=i - 1)))]

    # 加總每天有多少則訊息
    for i in range(len(member_1_msglist)):
        if member_1_msglist[i][3] == name[0]:
            d1 = (member_1_msglist[i][0] - datetime.strptime(str(origin_1), "%Y-%m-%d")).days
            day_1[d1 + 1][0] += 1

    for i in range(len(member_2_msglist)):
        if member_1_msglist[i][3] == name[1]:
            d2 = (member_2_msglist[i][0] - datetime.strptime(str(origin_2), "%Y-%m-%d")).days
            day_2[d2 + 1][0] += 1

    # 取近30日的句數訊息
    month_1 = list(day_1.values())[-30:]  # 第一個人的近30日的總句數訊息
    month_2 = list(day_2.values())[-30:]  # 第二個人的近30日的總句數訊息

    member_date_1 = []
    member_sent_1 = []
    for i in range(len(month_1)):
        # 第一人的日期
        member_date_1.append(month_1[i][1])
        # 第一人句數訊息
        member_sent_1.append(month_1[i][0])

    member_date_2 = []
    member_sent_2 = []
    for i in range(len(month_2)):
        # 第二人的日期
        member_date_2.append(month_2[i][1])
        # 第二人句數訊息
        member_sent_2.append(month_2[i][0])
    return [member_date_1, member_sent_1, member_date_2, member_sent_2, name]


temp = total_msg(lines)
# print(temp)
# 折線圖
fig, ax = plt.subplots()
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
plt.xticks(fontsize=7)
plt.yticks(fontsize=7)
plt.title('近30日雙方總回覆則數折線圖')  # 設定圖形標題
plt.xlabel("日期")  # 設定x軸標題
plt.ylabel("回覆則數")  # 設定y軸標題
plt.plot(temp[0], temp[1], label=str(temp[4][0]) + "的回覆則數")
plt.plot(temp[2], temp[3], label=str(temp[4][1]) + "的回覆則數")
plt.xticks(rotation=45, ha='right')
# 顯示圖例
plt.legend(loc='best', fontsize=10)
# 顯示圖形
plt.show()
########################################################
'''24小時平均訊息數長條圖'''


def avghour_msg(list_message):
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


# 畫長條圖
avghour = avghour_msg(lines)
x_labels = np.array(avghour[1])  # 每個小時
height = np.array(avghour[0])  # 總回應則數
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

plt.title('24小時平均訊息數長條圖')  # 設定圖形標題
plt.bar(x_labels, height, width=0.5)
plt.xlabel("時間(24小時制)")  # 設定y軸標題
plt.ylabel("總回應則數")  # 設定x軸標題
plt.xlim((-0.5, 24))
plt.show()
