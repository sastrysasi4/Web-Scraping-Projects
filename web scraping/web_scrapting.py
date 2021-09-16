from bs4 import BeautifulSoup
import requests
import pandas as pd

data=[]
html_text= requests.get("https://hmfw.ap.gov.in/covid_dashboard.aspx",verify=False).text
soup = BeautifulSoup(html_text,"lxml")
table = soup.find("table",class_= "table table-bordered table-striped")

table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.findAll('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) 