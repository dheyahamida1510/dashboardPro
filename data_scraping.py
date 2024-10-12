# deklarasi library yang akan digunakan
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import json
from random import randint
import re

# untuk password akun LinkedIn
with open("D:\\Dokumen\\account.txt") as f:
    acc = f.readline()

# membuat instance webdriver
# headless Chrome browser
# (web driver didownload di : https://googlechromelabs.github.io/chrome-for-testing/#stable )
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("D:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

# membuka halaman login LinkedIn
driver.get("https://linkedin.com/uas/login")
 
# tunggu loading halaman
sleep(randint(5, 7))

# Mengisi username/alamat email
# cari field untuk mengisi username (email)
username = driver.find_element(By.ID, "username")
# mengisi alamat email
username.send_keys("dheyahamida@upi.edu")  
 
# Mengisi password
password = driver.find_element(By.ID, "password")
password.send_keys(acc)
 
# Format XPATH ---> //tagname[@attribute='value']
driver.find_element(By.XPATH, "//button[@type='submit']").click()
# tunggu loading halaman
sleep(randint(5, 6))

# check code
#print(driver.page_source)

# placeholder data
link_list = [
#    "https://www.linkedin.com/in/saiku1/",
#    "https://www.linkedin.com/in/tarandeep-singh-947135104/",
#    "https://www.linkedin.com/in/sylvester-kwame-inkoom-phd-6357b560/",
#    "https://www.linkedin.com/in/mdcochran/",
#    "https://www.linkedin.com/in/ameya-kabre/",
#    "https://www.linkedin.com/in/maddyrandle/",
#    "https://www.linkedin.com/in/kevincendana/",
#    "https://www.linkedin.com/in/shubhada-bagal/",
    "https://www.linkedin.com/in/zaretta-hammond-2b122ba/",
    "https://www.linkedin.com/in/ojo-audu-azure-certified/",
    "https://www.linkedin.com/in/victor-akoko-b85a2221a/",
]

with open("D:\\Dokumen\\dashboardPro\\people_data.json", "r+") as pd:
    people_data = json.load(pd)

for dsnt_link in link_list:

    driver.get(dsnt_link)
    sleep(randint(5, 7))
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    if(soup.find("div", class_= "mt2 relative")):

        # Mendapatkan bagian introduction dari profil
        # (name, work, location)
        intro = soup.find("div", class_= "mt2 relative")

        # check code
        # print(intro)

        name = intro.find("h1", class_="text-heading-xlarge inline t-24 v-align-middle break-words").text.strip()
        work = intro.find("div", class_="text-body-medium break-words").text.strip()
        loc = intro.find("span", class_="text-body-small inline t-black--light break-words").text.strip()

        # check code
        # print("Nama     : " + name + "\nProfesi     : " + work + "\nLokasi    : " + loc)


        # Mengambil data Experience

        experience = []

        # Jika ada element "navigation-index-see-all-experiences"
        if(soup.find("a", attrs={"id" : "navigation-index-see-all-experiences"})):
            driver.find_element(By.XPATH, "//*[@id='navigation-index-see-all-experiences']").click()
            sleep(randint(3, 5))
            experien = driver.page_source
            soup = BeautifulSoup(experien, "html.parser")

            exp = soup.find_all("div", attrs={"data-view-name" : "profile-component-entity"})

            for e in exp:
                exprn = e.find("div", class_="display-flex flex-row justify-space-between")

                if(exprn.find("div", class_="display-flex align-items-center mr1 t-bold")):
                    n = exprn.find("div", class_="display-flex align-items-center mr1 t-bold")
                    exp_name = n.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                    exp_loc = ""
                    if(exprn.find("span", class_="t-14 t-normal")):
                        l = exprn.find("span", class_="t-14 t-normal")
                        exp_loc = l.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                    exp_tm = ""
                    if(exprn.find("span", class_="t-14 t-normal t-black--light")):
                        t = exprn.find("span", class_="t-14 t-normal t-black--light")
                        exp_tm = t.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                    exp_dict = {"name" : exp_name, "location" : exp_loc, "time" : exp_tm}
                    experience.append(exp_dict)

                    # check code
                    # print(exp_name + "\nLocation :\n" + exp_loc + "\nTime :\n" + exp_tm + "\n")
                    # print("\n")
                    
        # Jika tidak ada
        else:
            experien = driver.page_source
            soup = BeautifulSoup(experien, "html.parser")
            expcl = soup.find_all("section", attrs={"data-view-name" : "profile-card"})

            for i in expcl:
                if(i.find("h2", class_="pvs-header__title text-heading-large")):
                    head = i.find("h2", class_="pvs-header__title text-heading-large")
                    if(head.find("span", attrs={"aria-hidden" : "true"}).text.strip() == "Experience"):
                        exp = i.find_all("div", attrs={"data-view-name" : "profile-component-entity"})

                        for e in exp:
                            exprn = e.find("div", class_="display-flex flex-row justify-space-between")

                            if(exprn.find("div", class_="display-flex align-items-center mr1 t-bold")):
                                n = exprn.find("div", class_="display-flex align-items-center mr1 t-bold")
                                exp_name = n.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                                exp_loc = ""
                                if(exprn.find("span", class_="t-14 t-normal")):
                                    l = exprn.find("span", class_="t-14 t-normal")
                                    exp_loc = l.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                                exp_tm = ""
                                if(exprn.find("span", class_="t-14 t-normal t-black--light")):
                                    t = exprn.find("span", class_="t-14 t-normal t-black--light")
                                    exp_tm = t.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                                exp_dict = {"name" : exp_name, "location" : exp_loc, "time" : exp_tm}
                                experience.append(exp_dict)

                                # check code
                                # print(exp_name + "\nLocation :\n" + exp_loc + "\nTime :\n" + exp_tm + "\n")
                                # print("\n")

        profile_dict = {
            "name" : name,
            "work" : work,
            "location" : loc,
            "link" : dsnt_link,
            "experiences" : experience
        }

        # Memeriksa jika data dengan user yang sama sudah ada pada database
        if len(people_data) != 0:
            i = 0
            match_found = False
            while i < len(people_data):
                if profile_dict["name"] == people_data[i]["name"] or profile_dict["link"] == people_data[i]["link"]:
                    people_data[i] = profile_dict
                    match_found = True
                    i = len(people_data)
                i += 1
            if match_found == False:
                people_data.append(profile_dict)
        else:
            people_data.append(profile_dict)

        sleep(randint(2, 3))

# Menuliskan database yang sudah terupdate pada file json database
json_data = json.dumps(people_data, indent=3)
with open("D:\\Dokumen\\dashboardPro\\people_data.json", "r+") as pd:
    pd.seek(0)
    pd.write(json_data)
    pd.truncate()

# Menutup selenium webdriver
driver.close()