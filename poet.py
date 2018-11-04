import bs4 as bs
import requests
import string
import random
import itertools

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
        poem = [*prevkey]
        for i in range(18):
            word = re(chain[prevkey])
            prevkey = (prevkey[1], word)
            poem.append(word)
        return ' '.join(poem)
