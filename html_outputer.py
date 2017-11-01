import re
import jieba

import numpy
import pandas as pd

import matplotlib.pyplot as plt

import matplotlib
import pylab

#matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from PIL import Image
from os import path
from wordcloud import WordCloud

class HtmlOutputer(object):

    def __init__(self):
        self.datas = ''

    def collect_data(self, new_data):
        if new_data is None:
            return

        for k in range(len(new_data)):
            self.datas += (str(new_data[k])).strip()

    def output_html(self):

        #清理数据，清除符号
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        filterdata = re.findall(pattern, self.datas)
        cleaned_comments = ''.join(filterdata)

        #结巴分词
        segment = jieba.lcut(cleaned_comments, cut_all=False)
        words_df = pd.DataFrame({'segment': segment})

        stopwords = pd.read_csv("stopwords.txt", index_col=False, quoting=3, sep="\t", names=['stopword'], encoding='utf-8')
        words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

        #词频统计
        words_stat = words_df.groupby(by=['segment'])['segment'].agg({"count":numpy.size})
        words_stat = words_stat.reset_index().sort_values(by=["count"], ascending=False)
        print(words_stat.head())

        #背景图片
        mask = numpy.array(Image.open("man.jpg"))

        wordcloud = WordCloud(font_path = "msyh.ttf",background_color = "black", max_words=1000 ,random_state=1 ,mask=mask)

        word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
        word_frequence_list = []

        for key in word_frequence:
            temp = (key, word_frequence[key])
            word_frequence_list.append(temp)

        wordcloud = wordcloud.fit_words(dict(word_frequence_list))

        plt.imshow(wordcloud)
        plt.axis("off")
        plt.figure()
        #pylab.show()
        plt.imshow(mask)
        plt.axis("off")
        plt.show()

        # fout = open('output.html', 'w', encoding='utf-8')
        #
        # fout.write("<html>")
        # fout.write("<body>")
        # fout.write("<div>")
        # fout.write(words_df.head())
        # fout.write("</div>")
        # fout.write("</body>")
        # fout.write("</html>")
        #
        # fout.close()