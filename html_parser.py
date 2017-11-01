from bs4 import BeautifulSoup
import re
import urllib.parse

class HtmlParser(object):

    def parse(self, html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')

        new_data = self._get_new_data(soup)
        return  new_data


    def _get_new_data(self, soup):

        eachCommentList = []

        comment_div_lits = soup.find_all('div', class_='comment')

        if comment_div_lits is None:
            return

        for item in comment_div_lits:
            if item.find('p').get_text() is not None:
                eachCommentList.append(item.find('p').get_text())

        return  eachCommentList

