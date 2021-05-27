import re
import json
from os import path
from random import choice


def main(w=0):
    current_path = path.dirname(__file__)
    content = open(current_path+'/temp/EnglishAnswer.html',
                   encoding='utf-8').read()
    result = re.findall(r"(.+答案：</span>(.*?)</li>.+)", content)
    questions = re.findall('question_', content)
    if w:
        # 1 系数是保证你每次都上80，但偶尔会上90。改成1.2不会上90，经常上不了80
        w = int(len(questions) * (100-w) / 100 * 1)
    print('随机选择 '+str(w)+' 道题的答案')

    ans_list = []
    for x in result:
        if '、' in x[1]:
            xlist = x[1].split('、')
            for y in xlist:
                if w != 0:
                    ans_list.append(
                        choice(['this', 'it', 'kind', 'so', 'and']))  # 随机从垃圾词汇中挑选一个
                    w -= 1
                else:
                    ans_list.append(y)
        else:
            random = choice(['A', 'B'])   # 只选两个是因为可以同时兼容双选和多选
            ans = x[1]
            if w != 0:
                ans = random
                w -= 1
            # GET THE FUCKING ID!!!!
            id_list = re.findall('<label for="(.*?)">', x[0])
            if id_list:
                letters = ["A", "B", "C", "D"]
                for y in range(0, 4):
                    if ans == letters[y]:
                        ans_list.append(id_list[y])
            else:
                ans_list.append(ans)
    return ans_list


def callback(w):
    ans = main(w)
    return ans


if __name__ == '__main__':
    print(main(80))
