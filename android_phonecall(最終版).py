'''for Andorid 使用'''
from datetime import datetime
import matplotlib as mpl
import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager
dateformat = "%Y/%m/%d"
dateFormatter = "%Y/%m/%d %H:%M"
timeformat = "%H:%M"
calltimeformat = "%H:%M:%S"
# input file
# C:\Users\j3699\OneDrive\桌面\Chat history with 姍姐.txt
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
# print(lines)
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


# print(lines)
# print(lines[-1][1:6])  # ['2020/12/18', '20:19', '昀真', '通話時間 2:41']
#########################################################################
'''雙方通話時間圓餅圖'''


def call_time(list_message):
    # 先建立兩人名字的list，方便後面分層
    name = []
    name.append(list_message[0][3])
    for i in range(len(list_message)):
        if list_message[i][3] != name[0]:
            name.append(list_message[i][3])
            break
    # 先分開兩人的通話時間[通話時間]
    call_temp_1 = []
    call_temp_2 = []
    for i in range(len(list_message)):
        if list_message[i][3] == name[0] and list_message[i][4][0:4] == "通話時間":
            call_temp_1.append(list_message[i][4][5:])

        if list_message[i][3] == name[1] and list_message[i][4][0:4] == "通話時間":
            call_temp_2.append(list_message[i][4][5:])
    # 轉換成時間格式
    call_1 = []
    call_2 = []
    for i in call_temp_1:
        if len(i) == 7:  # 通話是大於一個小時但小於十個小時(7個字元)
            call_1.append(datetime.strptime("0" + i, calltimeformat))
        if len(i) == 8:  # 通話是大於十個小時(8個字元)
            call_1.append(datetime.strptime(i, calltimeformat))
        if len(i) == 4:  # 通話小於一個小時且小於十分鐘(4個字元)
            call_1.append(datetime.strptime("00:0" + i, calltimeformat))
        if len(i) == 5:  # 通話小於一個小時且大於十分鐘(5個字元)
            call_1.append(datetime.strptime("00:" + i, calltimeformat))
        else:
            pass
    for i in call_temp_2:
        if len(i) == 7:  # 通話是大於一個小時但小於十個小時(7個字元)
            call_2.append(datetime.strptime("0" + i, calltimeformat))
        if len(i) == 8:  # 通話是大於十個小時(8個字元)
            call_2.append(datetime.strptime(i, calltimeformat))
        if len(i) == 4:  # 通話小於一個小時且小於十分鐘(4個字元)
            call_2.append(datetime.strptime("00:0" + i, calltimeformat))
        if len(i) == 5:  # 通話小於一個小時且大於十分鐘(5個字元)
            call_2.append(datetime.strptime("00:" + i, calltimeformat))
        else:
            pass
    # 加總雙方各別通話時間
    time_1 = float()
    time_2 = float()
    for i in call_1:
        hour_1 = (i - datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).seconds / 60
        time_1 += hour_1
    for i in call_2:
        hour_2 = (i - datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).seconds / 60
        time_2 += hour_2

    return [[name[0], round(time_1, 2)], [name[1], round(time_2, 2)]]


calltime = call_time(lines)
# print(calltime)

# 畫雙方通話時間圓餅圖
if calltime[0][1] != 0 and calltime[1][1] != 0:
    print(str(calltime[0][0]) + "打給對方的通話時間(分鐘): " + str(calltime[0][1]))
    print(str(calltime[1][0]) + "打給對方的通話時間(分鐘): " + str(calltime[1][1]))
    plt.figure(figsize=(10, 6))  # 設定圖形大小
    labels = [calltime[0][0], calltime[1][0]]  # 是名字
    calltime_pie = [calltime[0][1], calltime[1][1]]  # 是通話時間
    # 顯示圖例
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    plt.pie(calltime_pie, labels=labels, autopct="%3.1f%%")
    plt.title('從古至今雙方通話時間圓餅圖')  # 設定圖形標題
    plt.legend(loc="best")
    plt.show()

    '''只有一人有打過電話'''
if calltime[0][1] == 0 and calltime[1][1] != 0:  # 只有第一人有打過電話
    print(str(calltime[0][0]) + "打給對方的通話時間(分鐘): " + str(calltime[0][1]))
    print(str(calltime[1][0]) + "打給對方的通話時間(分鐘): " + str(calltime[1][1]))
    plt.figure(figsize=(10, 6))  # 設定圖形大小
    labels = [calltime[1][0]]  # 是名字
    calltime_pie = [1]  # 是通話時間
    # 顯示圖例
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    plt.pie(calltime_pie, labels=labels, autopct="%3.1f%%")
    plt.title('從古至今雙方通話時間圓餅圖')  # 設定圖形標題
    plt.legend(loc="best")
    plt.show()
if calltime[0][1] != 0 and calltime[1][1] == 0:  # 只有第二人有打過電話
    print(str(calltime[0][0]) + "打給對方的通話時間(分鐘): " + str(calltime[0][1]))
    print(str(calltime[1][0]) + "打給對方的通話時間(分鐘): " + str(calltime[1][1]))
    plt.figure(figsize=(10, 6))  # 設定圖形大小
    labels = [calltime[0][0]]  # 是名字
    calltime_pie = [1]  # 是通話時間
    # 顯示圖例
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    plt.pie(calltime_pie, labels=labels, autopct="%3.1f%%")
    plt.title('從古至今雙方通話時間圓餅圖')  # 設定圖形標題
    plt.legend(loc="best")
    plt.show()
if calltime[0][1] == 0 and calltime[1][1] == 0:
    print("你們還沒有通話過喔")
###############################################################################
'''近30日雙方通話次數折線圖'''


def phonecall_times(list_message):
    # 抓兩人第一則的訊息
    name = []
    name.append(list_message[0][3])
    for i in range(len(list_message)):
        if list_message[i][3] != name[0]:
            name.append(list_message[i][3])
            break
    member_1_calltimes = []  # 把有通話的放到list中[日期, 名字, 次數]
    member_2_calltimes = []
    for i in range(len(list_message)):
        if list_message[i][3] == name[0] and list_message[i][4][0:4] == "通話時間":
            member_1_calltimes.append([list_message[i][0], list_message[i][3], 1])
        if list_message[i][3] == name[0] and list_message[i][4][0:4] != "通話時間":
            member_1_calltimes.append([list_message[i][0], list_message[i][3], 0])
    for i in range(len(list_message)):
        if list_message[i][3] == name[1] and list_message[i][4][0:4] == "通話時間":
            member_2_calltimes.append([list_message[i][0], list_message[i][3], 1])
        if list_message[i][3] == name[1] and list_message[i][4][0:4] != "通話時間":
            member_2_calltimes.append([list_message[i][0], list_message[i][3], 0])
    # 第一則訊息絕對日期
    origin_1 = datetime.date(member_1_calltimes[0][0])
    last_1 = datetime.date(member_1_calltimes[- 1][0])
    passday_1 = (last_1 - origin_1).days + 1

    origin_2 = datetime.date(member_2_calltimes[0][0])
    last_2 = datetime.date(member_2_calltimes[- 1][0])
    passday_2 = (last_2 - origin_2).days + 1
    # 做每天天數的list
    interval_1 = []
    interval_2 = []
    for i in range(passday_1):
        interval_1.append(i + 1)

    for i in range(passday_2):
        interval_2.append(i + 1)

    # dict 天數:[每日通話數, 日期]
    day_1 = dict()
    for i in interval_1:
        day_1[i] = [0, str(datetime.date(member_1_calltimes[0][0] + dt.timedelta(days=i-1)))]

    day_2 = dict()
    for i in interval_2:
        day_2[i] = [0, str(datetime.date(member_2_calltimes[0][0] + dt.timedelta(days=i-1)))]

    # 加總每天有多少通電話
    for i in range(len(member_1_calltimes)):
        if member_1_calltimes[i][1] == name[0]:
            d1 = (member_1_calltimes[i][0] - datetime.strptime(str(origin_1), "%Y-%m-%d")).days
            day_1[d1 + 1][0] += member_1_calltimes[i][2]

    for i in range(len(member_2_calltimes)):
        if member_2_calltimes[i][1] == name[1]:
            d2 = (member_2_calltimes[i][0] - datetime.strptime(str(origin_2), "%Y-%m-%d")).days
            day_2[d2 + 1][0] += member_2_calltimes[i][2]

    # 取近30日的句數訊息
    month_1 = list(day_1.values())[-30:]  # 第一個人的近30日的通話數
    month_2 = list(day_2.values())[-30:]  # 第二個人的近30日的通話數

    member_date_1 = []
    member_times_1 = []
    for i in range(len(month_1)):
        # 第一人的日期
        member_date_1.append(month_1[i][1])
        # 第一人的通話數
        member_times_1.append(month_1[i][0])

    member_date_2 = []
    member_times_2 = []
    for i in range(len(month_2)):
        # 第二人的日期
        member_date_2.append(month_2[i][1])
        # 第二人的通話數
        member_times_2.append(month_2[i][0])
    return [member_date_1, member_times_1, member_date_2, member_times_2, name]


calltimes_temp = phonecall_times(lines)
# print(calltimes_temp)
# 近30日通話次數折線圖

plt.figure(figsize=(10, 6))  # 設定圖形大小
plt.plot(calltimes_temp[0], calltimes_temp[1], marker='o', ms=5, linestyle="--", label=str(calltimes_temp[4][0]) + "打給" + str(calltimes_temp[4][1]) + "的次數")
plt.plot(calltimes_temp[0], calltimes_temp[3], marker='s', ms=5, label=str(calltimes_temp[4][1]) + "打給" + str(calltimes_temp[4][0]) + "的次數")
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
# 顯示圖例
plt.xticks(fontsize=7)  # x刻度
plt.ylabel("通話次數")  # 設定y軸標題
plt.title('近30日雙方通話次數折線圖')  # 設定圖形標題
plt.xticks(rotation=45,  ha='right')
plt.legend(loc='best', fontsize=10)
# 顯示圖形
plt.show()
##################################################################################
'''近30日雙方通話時間折線圖'''
# dict資料長這樣 (從第一天至今第幾天:[幾則訊息, 日期].....) 848: [0, '2020-11-22'], 849: [4, '2020-11-23'], 850: [1, '2020-11-24']}


def day_calltime(list_message):
    name = []
    name.append(list_message[0][3])
    for i in range(len(list_message)):
        if list_message[i][3] != name[0]:
            name.append(list_message[i][3])
            break
    # 先分開兩人的通話時間[日期, 名字, 通話時間][datetime.datetime(2020, 12, 18, 20, 19), '昀真', '2:41']
    call_temp_1 = []
    call_temp_2 = []
    for i in range(len(list_message)):
        if list_message[i][3] == name[0] and list_message[i][4][0:4] == "通話時間":
            call_temp_1.append([list_message[i][0], list_message[i][3], list_message[i][4][5:]])
        else:
            call_temp_1.append([list_message[i][0], list_message[i][3], "0"])
    for i in range(len(list_message)):
        if list_message[i][3] == name[1] and list_message[i][4][0:4] == "通話時間":
            call_temp_2.append([list_message[i][0], list_message[i][3], list_message[i][4][5:]])
        else:
            call_temp_2.append([list_message[i][0], list_message[i][3], "0"])
    # 轉換成時間格式
    call_1 = []
    call_2 = []
    for i in range(len(call_temp_1)):
        if len(call_temp_1[i][2]) == 1:
            call_1.append([call_temp_1[i][0], call_temp_1[i][1], datetime.strptime("00:00:00", calltimeformat)])
        if len(call_temp_1[i][2]) == 7:  # 通話是大於一個小時但小於十個小時(7個字元)
            call_1.append([call_temp_1[i][0], call_temp_1[i][1], datetime.strptime("0" + call_temp_1[i][2], calltimeformat)])
        if len(call_temp_1[i][2]) == 8:  # 通話是大於十個小時(8個字元)
            call_1.append([call_temp_1[i][0], call_temp_1[i][1],  datetime.strptime(call_temp_1[i][2], calltimeformat)])
        if len(call_temp_1[i][2]) == 4:  # 通話小於一個小時且小於十分鐘(4個字元)
            call_1.append([call_temp_1[i][0], call_temp_1[i][1], datetime.strptime("00:0" + call_temp_1[i][2], calltimeformat)])
        if len(call_temp_1[i][2]) == 5:  # 通話小於一個小時且大於十分鐘(5個字元)
            call_1.append([call_temp_1[i][0], call_temp_1[i][1], datetime.strptime("00:" + call_temp_1[i][2], calltimeformat)])

    for i in range(len(call_temp_2)):
        if len(call_temp_2[i][2]) == 1:
            call_2.append([call_temp_2[i][0], call_temp_2[i][1], datetime.strptime("00:00:00", calltimeformat)])
        if len(call_temp_2[i][2]) == 7:  # 通話是大於一個小時但小於十個小時(7個字元)
            call_2.append([call_temp_2[i][0], call_temp_2[i][1], datetime.strptime("0" + call_temp_2[i][2], calltimeformat)])
        if len(call_temp_2[i][2]) == 8:  # 通話是大於十個小時(8個字元)
            call_2.append([call_temp_2[i][0], call_temp_2[i][1], datetime.strptime(call_temp_2[i][2], calltimeformat)])
        if len(call_temp_2[i][2]) == 4:  # 通話小於一個小時且小於十分鐘(4個字元)
            call_2.append([call_temp_2[i][0], call_temp_2[i][1], datetime.strptime("00:0" + call_temp_2[i][2], calltimeformat)])
        if len(call_temp_2[i][2]) == 5:  # 通話小於一個小時且大於十分鐘(5個字元)
            call_2.append([call_temp_2[i][0], call_temp_2[i][1], datetime.strptime("00:" + call_temp_2[i][2], calltimeformat)])

    # 第一則訊息絕對日期
    origin_1 = datetime.date(call_1[0][0])
    last_1 = datetime.date(call_1[- 1][0])
    passday_1 = (last_1 - origin_1).days + 1

    origin_2 = datetime.date(call_2[0][0])
    last_2 = datetime.date(call_2[- 1][0])
    passday_2 = (last_2 - origin_2).days + 1
    # 做每天天數的list
    interval_1 = []
    interval_2 = []
    for i in range(passday_1):
        interval_1.append(i + 1)

    for i in range(passday_2):
        interval_2.append(i + 1)

    # dict 天數:[每日通話時間, 日期]
    day_1 = dict()
    for i in interval_1:
        day_1[i] = [0, str(datetime.date(call_1[0][0] + dt.timedelta(days=i-1)))]

    day_2 = dict()
    for i in interval_2:
        day_2[i] = [0, str(datetime.date(call_2[0][0] + dt.timedelta(days=i-1)))]

    # 加總雙方各別通話時間
    hour_1 = float()
    hour_2 = float()
    for i in range(len(call_1)):
        d1 = (call_1[i][0] - datetime.strptime(str(origin_1), "%Y-%m-%d")).days
        hour_1 = (call_1[i][2] - datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).seconds / 60
        day_1[d1 + 1][0] += hour_1

    for i in range(len(call_2)):
        d2 = (call_2[i][0] - datetime.strptime(str(origin_2), "%Y-%m-%d")).days
        hour_2 = (call_2[i][2] - datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).seconds / 60
        day_2[d2 + 1][0] += hour_2

    # 取近30日的通話時間
    month_1 = list(day_1.values())[-30:]  # 第一個人的近30日的通話時間
    month_2 = list(day_2.values())[-30:]  # 第二個人的近30日的通話時間

    member_date_1 = []
    member_time_1 = []
    time_1 = float()
    time_2 = float()
    for i in range(len(month_1)):
        # 第一人的日期
        member_date_1.append(month_1[i][1])
        # 第一人通話時間
        time_1 = round(month_1[i][0], 4)
        member_time_1.append(time_1)

    member_date_2 = []
    member_time_2 = []
    for i in range(len(month_2)):
        # 第一人的日期
        member_date_2.append(month_2[i][1])
        # 第一人通話時間
        time_2 = round(month_2[i][0], 4)
        member_time_2.append(time_2)

    return [member_date_1, member_time_1, member_date_2, member_time_2, name]


calltime = day_calltime(lines)
# print(calltime)

plt.figure(figsize=(10, 6))  # 設定圖形大小
plt.plot(calltime[0], calltime[1], marker='o', ms=5, linestyle="--", label=str(calltime[4][0]) + "打給" + str(calltime[4][1]) + "的通話時間(分鐘)")
plt.plot(calltime[0], calltime[3], marker='s', ms=5, label=str(calltime[4][1]) + "打給" + str(calltime[4][0]) + "的通話時間(分鐘)")
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
# 顯示圖例
plt.yticks(fontsize=7)
plt.xticks(rotation=45,  ha='right', fontsize=7)
plt.title("近30日雙方通話時間折線圖")
plt.ylabel("通話時間(分鐘)")  # 設定y軸標題
# 顯示圖例
plt.legend(loc='best', fontsize=10)
# 顯示圖形
plt.show()
