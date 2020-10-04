from bs4 import BeautifulSoup
import requests


# first !
# source = requests.get(r'https://www.bnro.ro/Home.aspx/',verify=False).text

# soup = BeautifulSoup(source,'html.parser')

# x=soup.find('table')
# target2 = x.th.find_next().text
# euro = x.th.text
# curs_zi = float(target2)


# def get_trend():
#     if x.find('span',class_ = 'rise') == None:
#         pass
#     if x.find('span',class_ = 'rise'):
#         return (curs_zi - abs(float(x.find('span',class_ = 'rise').text)))
#     if x.find('span',class_ = 'fall') == None:
#         pass
#     if x.find('span',class_ = 'fall'):
#         return (curs_zi + abs(float(x.find('span',class_ = 'fall').text)))


# curs_ieri = get_trend()

# second !

source = requests.get(r'https://bnr.ro/cursul-de-schimb-524.aspx',verify=False).text

soup = BeautifulSoup(source,'html.parser')

x=soup.find('table' ,class_ = 'cursTable')
x2 = x.find_all('tr')[8]


curs_ieri = x2.find_all('td')[5].text
curs_zi = x2.find_all('td')[6].text