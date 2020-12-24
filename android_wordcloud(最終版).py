'''for Andorid 使用'''
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL .Image as image
import numpy as np
import jieba
import datetime as dt

# Notice:字數的list跟其他檔案不太一樣
dateformat = "%Y/%m/%d"
dateFormatter = "%Y/%m/%d %H:%M"
timeformat = "%H:%M"
calltimeformat = "%H:%M:%S"
# input file
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
#############################################
# 建立兩人名字的list
name = []
name.append(lines_for_word[0][3])
for i in range(len(lines_for_word)):
    if lines_for_word[i][3] != name[0]:
        name.append(lines_for_word[i][3])
        break
# print(name)
"""文字雲"""
only_text1 = []
only_text2 = []
for i in range(len(lines_for_word)):
    if lines_for_word[i][4] == '[貼圖]':
        continue
    if lines_for_word[i][4] == '[照片]':
        continue
    if lines_for_word[i][4] == '[影片]':
        continue
    if lines_for_word[i][4] == '[語音訊息]':
        continue
    if lines_for_word[i][4] == '[檔案]':
        continue
    if lines_for_word[i][4] == '未接來電':
        continue
    if lines_for_word[i][4] == '相簿建立成功':
        continue
    if lines_for_word[i][4] == '[聯絡資訊]':
        continue
    if lines_for_word[i][4] == '[位置資訊]':
        continue
    if lines_for_word[i][4][0:4] == '通話時間':
        continue
    if lines_for_word[i][4] == '您已結束通話':
        continue
    if lines_for_word[i][4] == '[禮物]':
        continue
    if lines_for_word[i][4] == '無人接聽':
        continue
    if lines_for_word[i][3] == name[0]:
        only_text1.append(lines_for_word[i][4])
    if lines_for_word[i][3] == name[1]:
        only_text2.append(lines_for_word[i][4])
# print(only_text1)
# print(only_text2)

enter_text1 = ''
enter_text2 = ''
for text1 in only_text1:
    enter_text1 += text1 + '\n'
for text2 in only_text2:
    enter_text2 += text2 + '\n'

font = 'C:\\Users\\j3699\\.matplotlib\\TaipeiSansTCBeta-Regular.ttf'  # 要自己從使用者的電腦放字型檔
word_list1 = jieba.cut(enter_text1)  # 第一個人傳的訊息
result1 = " ".join(word_list1)  # 斷句以空格隔開
mask = np.array(image.open("C:\\Users\\j3699\\OneDrive\\Documents\\circle.jpg"))  # 要自己從使用者的電腦下載文字雲圖形模板
wordcloud1 = WordCloud(mask=mask, font_path=font).generate(result1)
# 這裡會合併兩個圖(所以用到subplot)
plt.figure(figsize=(10, 5))
plt.subplot(1,2,1)
plt. title(str(name[0]) + "常用的字")
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
plt.imshow(wordcloud1)
plt.axis("off")


word_list2 = jieba.cut(enter_text2)  # 第二個人傳的訊息
result2 = " ".join(word_list2)
wordcloud2 = WordCloud(mask=mask, font_path=font).generate(result2)

plt.subplot(1,2,2)
plt. title(str(name[1]) + "常用的字")
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
plt.axis("off")
plt.imshow(wordcloud2)
# 顯示圖形
plt.show()
