import requests
import bs4
import pandas as pd

TEMP_URL = "http://notelections.online/region/region/st-petersburg?action=show&root=1&tvd=27820001217417&vrn=27820001217413&region=78&global=&sub_region=78&prver=0&pronetvd=null&vibid=27820001217417&type=222"

response = requests.get(url=TEMP_URL)
soup = bs4.BeautifulSoup(response.text, 'html.parser')
find_tik = soup.find_all("a")
table = soup.find('table', attrs={'style': "width:100%;border-color:#000000"})
column = table.contents[1].contents[1].contents[1]
items = soup.find_all('a', attrs={'style': "text-decoration: none"})

fields = []

for i in range(2, len(column.contents)):
    if i % 2 != 0:
        fields += [column.contents[i].contents[2].contents[0].get_text()]

fields.remove('\xa0')
fields.insert(0, 'tic')
fields.insert(1, 'uik')

tik = []

for i in find_tik[8:-4]:
    tik += [i.contents[0]]

href = []

for elem in items:
    href += ["http://notelections.online" + str(elem['href'])]

d = []


def add_table():
    for i in range(30):
        response = requests.get(url=href[i])
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        find_uik = soup.find_all("a")
        find_val = soup.find_all("b")

        uik = []

        for find in find_uik[9:-3]:
            uik += [find.contents[0]]

        val = []

        for find in find_val[19:]:
            val += [find.contents[0]]

        for j in range(0, len(uik)):
            dict_ = {"Tik": tik[i], 'Uik': uik[j]}
            for k in range(2, len(fields)):
                dict_[fields[k]] = (val[j + len(uik) * (k - 2)])
            d.append(dict_)


add_table()

elect_table = pd.DataFrame(d)
elect_table.to_csv("el_table.csv")
