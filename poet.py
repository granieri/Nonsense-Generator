import bs4 as bs
import requests
import string
import random
import itertools
import pyphen

class Poet:

    def __init__(self):
        pass

    def target(self, url):
        target_html = requests.get(url).text
        self.soup = bs.BeautifulSoup(target_html, 'html.parser')

    def makechain(self, words):
        chain = {}
        thruples = ((a, b, c) for a, b, c in zip(words, words[1:], words[2:]))
        for t in thruples:
            k, v = (t[0], t[1]), t[2]
            try:
                chain[k].append(v)
            except KeyError:
                chain[k] = [v]
        return chain

    def getpoem(self):
        ps = [p.get_text() for p in self.soup.find_all('p')]
        text = '\n'.join(ps)
        words = text.split()
        words = [word.strip() for word in words if all([c in string.ascii_letters for c in word])]
        chain = self.makechain(words)
        rx = random.randint(0, len(chain.keys())-1)
        prevkey = list(chain.keys())[rx] # root
        re = lambda x: x[random.randint(0,len(x)-1)]# random element
        syls = [5, 7, 5]
        dic = pyphen.Pyphen(lang='en_US')
        poem = []
        line = []
        while syls:
            word = re(chain[prevkey])
            prevkey = (prevkey[1], word)
            sylc = len(dic.inserted(word).split('-'))
            if (syls[0] - sylc) >= 0:
                syls[0] -= sylc
                line.append(word)
            if syls[0] == 0:
                syls.pop(0)
                poem.append(' '.join(line))
                line = []
        return '|'.join(poem)
