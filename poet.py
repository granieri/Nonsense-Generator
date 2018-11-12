import bs4 as bs
import requests
import string
import random
import itertools
from nltk.corpus import cmudict

class Poet:

    commonbaddies = [
    'and',
    'of',
    'the',
    'as',
    'for'
    'a',
    'to',
    'like',
    'in'
    ]

    def __init__(self):
        pass

    def target(self, url):
        target_html = requests.get(url).text
        self.soup = bs.BeautifulSoup(target_html, 'html.parser')

    def countsyl(self, words):
        ct = 0
        d = cmudict.dict()
        for word in words:
            if(word.lower() in d):
                ct += [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
        return ct

    def makechain(self, words, syl):
        rx = random.randint(0, len(words)-1)
        line = []
        while(self.countsyl(line) != syl or line[-1] in self.commonbaddies):
            line.append(words[rx].lower())
            if(self.countsyl(line) > 5):
                line = line[1:]
            rx+=1
            print(line)
        return line

    def getpoem(self):
        ps = [p.get_text() for p in self.soup.find_all('p')]
        text = '\n'.join(ps)
        words = text.split()
        words = [word.strip() for word in words if all([c in string.ascii_letters for c in word])]
        line_1 = self.makechain(words, 5)
        line_2 = self.makechain(words, 7)
        line_3 = self.makechain(words, 5)

        poem = ' '.join(line_1 + ['|'] + line_2 + ['|'] + line_3)
        return poem
