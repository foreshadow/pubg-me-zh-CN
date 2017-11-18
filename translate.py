from bs4 import BeautifulSoup as bs
from json import dumps, loads
from re import match
from urllib.request import Request, urlopen

class TranslateMap:

    def __init__(self, path):
        self.path = path
        self.map = {}
        json = '{}'
        try:
            f = open(path, encoding='u8')
            json = f.read()
            f.close()
        except Exception as e:
            print(e)
        self.map = loads(json)

    def _filter(self, key):
        return match('[A-Za-z]', key)

    def _add(self, key):
        if not key in self.map:
            self.map[key] = key

    def tr(self, key):
        if self._filter(key):
            self._add(key)
            return self.map[key]
        else:
            return key

    def dump(self):
        for key in sorted(self.map.keys()):
            print(key)

    def save(self):
        f = open(self.path, 'w', encoding='u8')
        f.write(dumps(self.map, sort_keys=True, indent='  '))
        f.close()

lang = 'zh-CN'

tm = TranslateMap('{}.json'.format(lang))

def translate(html):
    s = bs(html, 'html5lib')
    for item in s.find_all('script'):
        item.decompose()
    for item in s.find_all('link'):
        item.decompose()
    # s.find(attrs={'id': 'header'}).decompose()
    nav = s.find(attrs={'class': 'global-nav'}).find_all('li')
    nav[0].decompose()
    nav[3].decompose()
    s.find('form').decompose()
    s.find(attrs={'class': 'btn-signin'}).parent.parent.decompose()
    s.find(attrs={'id': 'footer'}).decompose()
    s.head.append(s.new_tag('link', href="style.css", rel="stylesheet"))
    for item in s.find_all('div'):
        if item.string:
            item.string = tm.tr(item.string)
    for item in s.find_all('p'):
        if item.string:
            item.string = tm.tr(item.string)
    for item in s.find_all(attrs={'class': 'label'}):
        if item.string:
            item.string = tm.tr(item.string)
    return s.prettify()

for weapon in ['sniper-rifles', 'assault-rifles', 'submachine-guns', 'shotguns',
               'pistols', 'misc', 'melee', 'throwables']:
    url = 'https://pubg.me/weapons/{}'.format(weapon)
    print(url)
    request = Request(url, headers={
        'User-Agent': 'Infinity'
    })
    response = urlopen(request)
    html = translate(response.read())
    open('doc/zh-CN/{}.html'.format(weapon), 'w', encoding='u8').write(html)

tm.save()