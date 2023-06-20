from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd 
import time

# opsi = webdriver.ChromeOptions()
# opsi.add_argument('--headless')

driver = webdriver.Chrome()

#menampung data
list_posisi,list_company,list_location =[],[],[]
list_date,list_url,list_deskripsi=[],[],[]

start_values = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,]

# Nilai awal dan akhir
start_awal = 0
start_akhir = 400
# Membuat daftar start_values dengan pola kelipatan 10
start_values = list(range(start_awal, start_akhir + 1, 10))

for start in start_values:
    #driver membuka url
    driver.get(f"https://id.indeed.com/jobs?q=data+analyst&start={start}")
    time.sleep(1.5)
    #auto scroll dengan rentang 500px 
    rentang =500
    for i in range(1,10):
        akhir = rentang * i
        perintah = "window.scrollTo((0),"+str(akhir)+")"
        driver.execute_script(perintah)
        time.sleep(2.5)

    # time.sleep(5)
    # driver.save_screenshot("home.png")
    # content = driver.page_source
    # driver.quit()

    # lihattampilan
    content = driver.page_source

    base_url = 'https://id.indeed.com'
    data = BeautifulSoup(content, 'html.parser')
    # print(data.encode("utf-8"))

    # #menampung data
    # list_posisi,list_company,list_location =[],[],[]
    # list_date,list_url,list_deskripsi=[],[],[]
    datainpage = 1
    for item in data.find_all('div', class_='job_seen_beacon'):
        posisi = item.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').text
        company = item.find('span', class_='companyName').text
        location = item.find('div', class_= 'companyLocation').text
        posting = item.find('span',class_="date").text
        url = base_url + item.find('a',class_='jcs-JobTitle')['href']
        deskripsi = item.find('div', class_='job-snippet').text

        list_posisi.append(posisi)
        list_company.append(company)
        list_location.append(location)
        list_date.append(posting)
        list_url.append(url)
        list_deskripsi.append(deskripsi)

df = pd.DataFrame({'posisi':list_posisi,'company':list_company,'lokasi':list_location,'date_posting':list_date,'link':list_url,'deskripsi':list_deskripsi})

df.to_excel('data_analyst_indeed_19062023.xlsx', index=False)
driver.quit()