'''for ios 使用'''
# C:\Users\irene\Downloads\[LINE] 與張喜程的聊天.txt
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL .Image as image
import jieba
import datetime as dt

dateformat = "%Y/%m/%d"
dateFormatter = "%Y/%m/%d %H:%M"
timeformat = "%H:%M"
calltimeformat = "%H:%M:%S"
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

# input file
path = input()
with open(file=path, mode="r", encoding="utf-8", errors='ignore') as f:
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
            date = lines_for_word[i + 1][0][:-3]

            # 要再檢查日期是不是符合格式 因為有智障一則訊息裡包含空行
            datetime.strptime(date, dateformat)

            # 把空行和日期行位置append到indexes list中，等等加完日期就可以刪掉
            # 空行
            indexes.append(i)
            # 日期行
            indexes.append(i + 1)

            k = i + 2

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
        lines_for_word[i].insert(2, lines_for_word[i - 1][2])

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

#############################################
# 建立兩人名字的list
name = []
name.append(lines_for_word[0][3])
for i in range(len(lines_for_word)):
    if lines_for_word[i][3] != name[0]:
        name.append(lines_for_word[i][3])
        break


def relationship(list_message):
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
            if list_message[i][4] == "[貼圖]" or list_message[i][4] == "[照片]" \
                    or list_message[i][4] == "[影片]" or list_message[i][4] == "[語音訊息]" \
                    or list_message[i][4] == "[檔案]" or list_message[i][4][2:6] == "未接來電" \
                    or list_message[i][4] == "相簿建立成功" or list_message[i][4] == "[聯絡資訊]" \
                    or list_message[i][4] == "[位置資訊]" or list_message[i][4][2:6] == "通話時間 " \
                    or list_message[i][4][2:8] == "您已取消通話" or list_message[i][4] == "[禮物]" \
                    or lines_for_word[i][4][2:6] == "無人接聽" or lines_for_word[i][4][-4:] == "收回訊息":
                pass
            else:
                word_1 += len(list_message[i][4])  # 計算第一人字數
        if list_message[i][3] == name[1]:  # 如果名字與第二人相同
            if list_message[i][4] == "[貼圖]" or list_message[i][4] == "[照片]" \
                    or list_message[i][4] == "[影片]" or list_message[i][4] == "[語音訊息]" \
                    or list_message[i][4] == "[檔案]" or list_message[i][4][2:6] == "未接來電" \
                    or list_message[i][4] == "相簿建立成功" or list_message[i][4] == "[聯絡資訊]" \
                    or list_message[i][4] == "[位置資訊]" or list_message[i][4][2:6] == "通話時間 " \
                    or list_message[i][4][2:8] == "您已取消通話" or list_message[i][4] == "[禮物]" \
                    or lines_for_word[i][4][2:6] == "無人接聽" or lines_for_word[i][4][-4:] == "收回訊息":
                pass
            else:
                word_2 += len(list_message[i][4])  # 計算第一人字數
    total_word = word_1 + word_2
    return total_word


# 只看訊息
only_text1 = []
only_text2 = []
for i in range(len(lines_for_word)):
    if lines_for_word[i][3] == name[0]:  # 如果名字與第一人相同
        if lines_for_word[i][4] == "[貼圖]" or lines_for_word[i][4] == "[照片]" \
                or lines_for_word[i][4] == "[影片]" or lines_for_word[i][4] == "[語音訊息]" \
                or lines_for_word[i][4] == "[檔案]" or lines_for_word[i][4][2:6] == "未接來電" \
                or lines_for_word[i][4] == "相簿建立成功" or lines_for_word[i][4] == "[聯絡資訊]" \
                or lines_for_word[i][4] == "[位置資訊]" or lines_for_word[i][4][2:6] == "通話時間 " \
                or lines_for_word[i][4][2:8] == "您已取消通話" or lines_for_word[i][4] == "[禮物]" \
                or lines_for_word[i][4][2:6] == "無人接聽" or lines_for_word[i][4][-4:] == "收回訊息":
            pass
        else:
            only_text1.append(lines_for_word[i][4])
    if lines_for_word[i][3] == name[1]:  # 如果名字與第二人相同
        if lines_for_word[i][4] == "[貼圖]" or lines_for_word[i][4] == "[照片]" \
                or lines_for_word[i][4] == "[影片]" or lines_for_word[i][4] == "[語音訊息]" \
                or lines_for_word[i][4] == "[檔案]" or lines_for_word[i][4][2:6] == "未接來電" \
                or lines_for_word[i][4] == "相簿建立成功" or lines_for_word[i][4] == "[聯絡資訊]" \
                or lines_for_word[i][4] == "[位置資訊]" or lines_for_word[i][4][2:6] == "通話時間 " \
                or lines_for_word[i][4][2:8] == "您已取消通話" or lines_for_word[i][4] == "[禮物]" \
                or lines_for_word[i][4][2:6] == "無人接聽" or lines_for_word[i][4][-4:] == "收回訊息":
            pass
        else:
            only_text2.append(lines_for_word[i][4])


keyword_eat = ['吃', '早餐', '午餐', '晚餐', '宵夜', '好料', '甜點', '餐廳', '點心', '口味', 'ㄔ', '飯', '喝', '飲料']
eat1 = 0
eat2 = 0
for text in only_text1:
    for i in range(len(keyword_eat)):
        if text.find(keyword_eat[i]) != -1:
            eat1 += 1
for text in only_text2:
    for i in range(len(keyword_eat)):
        if text.find(keyword_eat[i]) != -1:
            eat2 += 1
eat = eat1 + eat2
eat_relationship = round(eat / relationship(lines_for_word) * 10000, 2)
if eat_relationship > 99.99:
    eat_relationship = 99.99

keyword_study = ['作業', 'hw', 'Hw', 'HW', '寫', '算', '教', '學', '報告']
study1 = 0
study2 = 0
for text in only_text1:
    for i in range(len(keyword_study)):
        if text.find(keyword_study[i]) != -1:
            study1 += 1
for text in only_text2:
    for i in range(len(keyword_study)):
        if text.find(keyword_study[i]) != -1:
            study2 += 1
study = study1 + study2
study_relationship = round(study / relationship(lines_for_word) * 10000, 2)
if study_relationship > 99.99:
    eat_relationship = 99.99

keyword_dirty = ['幹', '乾', '靠', '操', '媽的', '他媽', 'shit', 'fuck']
dirty1 = 0
dirty2 = 0
for text in only_text1:
    for i in range(len(keyword_dirty)):
        if text.find(keyword_dirty[i]) != -1:
            dirty1 += 1
for text in only_text2:
    for i in range(len(keyword_dirty)):
        if text.find(keyword_dirty[i]) != -1:
            dirty2 += 1
dirty = dirty1 + dirty2
dirty_relationship = round(dirty / relationship(lines_for_word) * 10000, 2)
if dirty_relationship > 99.99:
    dirty_relationship = 99.99

keyword_ha = ['哈']
ha1 = 0
ha2 = 0
for text in only_text1:
    for i in range(len(keyword_ha)):
        if text.find(keyword_ha[i]) != -1:
            ha1 += 1
for text in only_text2:
    for i in range(len(keyword_ha)):
        if text.find(keyword_ha[i]) != -1:
            ha2 += 1
ha = ha1 + ha2
ha_relationship = round(ha / relationship(lines_for_word) * 10000, 2)
if ha_relationship > 99.99:
    ha_relationship = 99.99

keyword_sex = ['變態', '色', '奶', '女', '男', '帥', '漂亮', '抓', '可愛', '妹', '寫真', '暈', '裸', '噁', '壞壞']
sex1 = 0
sex2 = 0
for text in only_text1:
    for i in range(len(keyword_sex)):
        if text.find(keyword_sex[i]) != -1:
            sex1 += 1
for text in only_text2:
    for i in range(len(keyword_sex)):
        if text.find(keyword_sex[i]) != -1:
            sex2 += 1
sex = sex1 + sex2
sex_relationship = round(sex / relationship(lines_for_word) * 10000, 2)
if sex_relationship > 99.99:
    sex_relationship = 99.99

keyword_number = [ha_relationship, sex_relationship, dirty_relationship, study_relationship, eat_relationship]
keyword_level = []
for i in keyword_number:
    if i == 0:
        keyword_level.append(0)
    if 0 < i < 20:
        keyword_level.append(1)
    if 20 <= i < 40:
        keyword_level.append(2)
    if 40 <= i < 60:
        keyword_level.append(3)
    if 60 <= i < 80:
        keyword_level.append(4)
    if 80 <= i:
        keyword_level.append(5)

keyword_type = ['「哈」的使用頻率', '變態程度', '髒話使用', '學術討論', '關於「吃」']
y = np.arange(len(keyword_type))  # 產生 Y 軸座標序列
x = np.arange(0, 6, 1)  # 產生 X 軸座標序列
plt.figure(figsize=(12, 6))  # 設定圖形大小
plt.barh(y, keyword_level)  # 繪製長條圖
plt.yticks(y, keyword_type)  # 設定 Y 軸刻度標籤
x_ticks = np.arange(0, 6, 1)  # X 軸刻度陣列
plt.xticks(x, x_ticks)  # 設定 X 軸刻度標籤
plt.title(name[0] + " & " + name[1] + '\n' + "聊天紀錄等級分析")  # 設定圖形標題
plt.xlabel('等級')   # 設定 X 軸標籤
plt.show()
