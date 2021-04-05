
from flask import Flask, render_template
import sys
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import webbrowser
import threading



#app.config()
URL = 'http://127.0.0.1:5000/'
stats_URL = 'https://leagueoflegends.fandom.com/wiki/List_of_champions/Base_statistics'
stats_page = requests.get(stats_URL)
stats_soup = BeautifulSoup(stats_page.content, "html.parser")
#results = soup.find(id='mw-content-text')
#class_results = stats_soup.find("div", {"class":"mw-parser-output"})
stats_results = stats_soup.find(
    "table", {"class": "sortable wikitable sticky-header"})
stats_contents = stats_results.contents
table_1 = []
table_2 = []
table_3 = []
headers = []
first_time = True

top = []
top_table = []
jungle = []
jungle_table = []
mid = []
mid_table = []
adc = []
adc_table = []
supp = []
supp_table = []

position_URL = 'https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position'
position_page = requests.get(position_URL)
position_soup = BeautifulSoup(position_page.content, "html.parser")
position_class = position_soup.find("div", {"class": "mw-parser-output"})
position_contents = position_class.contents[7].contents[1]
for row in range(2, len(position_contents), 2):
    name = position_contents.contents[row].contents
    nome = name[1].text.replace("\n", "").replace(" ", "")
    if ('data-sort-value' in name[3].attrs):
        top.append(nome)
    if ('data-sort-value' in name[5].attrs):
        jungle.append(nome)
    if ('data-sort-value' in name[7].attrs):
        mid.append(nome)
    if ('data-sort-value' in name[9].attrs):
        adc.append(nome)
    if ('data-sort-value' in name[11].attrs):
        supp.append(nome)


for row in stats_contents[1]:
    line = []
    count = 0
    for stat in row:
        if not ((count == 3) or (count == 4) or (count == 7) or (count == 8)):
            if hasattr(stat, 'text'):
                line.append(stat.text.replace(" ", ""))
        count += 1
    if line:
        if first_time:
            headers = line
            first_time = False
        else:
            if line[0] in top:
                top_table.append(line)
            if line[0] in jungle:
                jungle_table.append(line)
            if line[0] in mid:
                mid_table.append(line)
            if line[0] in adc:
                adc_table.append(line)
            if line[0] in supp:
                supp_table.append(line)
            if len(table_1)<(len(stats_contents[1].contents)/6):
                table_1.append(line)
            elif len(table_2)<len(table_1):
                table_2.append(line)
            else:
                table_3.append(line)


#print("table_1 size: " + str(len(table_1)))
#print("table_2 size: " + str(len(table_2)))
#print("table_3 size: " + str(len(table_3)))
#print(table)
#print("\n")
#print(top_table)
#print(tabulate(table, headers))
#print("\n")
#print(tabulate(top_table,headers))

@app.route("/")
def table():
    return render_template("table.html", headings=headers, top_data=top_table, jungle_data = jungle_table, 
                        mid_data = mid_table, adc_data=adc_table, supp_data=supp_table, all_data_1=table_1, all_data_2=table_2, all_data_3=table_3)

threading.Timer(1.25, lambda: webbrowser.open_new_tab(URL) ).start()

app.run(host='0.0.0.0')

