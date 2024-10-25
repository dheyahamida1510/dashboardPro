# deklarasi library yang akan digunakan
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import json
from random import randint
import re
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
sleep(randint(4, 5))

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
w = 0
while w < 3:
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "global-nav")))
    w += 1
sleep(randint(3, 5))

# check code
#print(driver.page_source)

# membuka halaman LinkedIn IKA UPI
driver.get("https://www.linkedin.com/in/ikatan-alumni-universitas-pendidikan-indonesia-209702297/")
WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//a[@class='ember-view']")))

sleep(randint(3, 4))
source = driver.page_source
soup = BeautifulSoup(source, "html.parser")

# mencari dan menekan tombol connections
connections_button = None
buttons = driver.find_elements(By.XPATH, "//a[@class='ember-view']")

for b in buttons:
    b_text = b.text
    if " connection" in b_text:
        connections_button = b

connections_button.click()
WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='mb1']")))
sleep(randint(1, 3))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//button[@type='button' and @aria-label='Next']")))
next_button = driver.find_element(By.XPATH, "//button[@type='button' and @aria-label='Next']")
driver.execute_script("arguments[0].scrollIntoView();", next_button)
sleep(randint(1, 3))

# Mendapatkan list profile yang akan di-scrape
link_list = []  # list untuk menampung link dari profile yang akan di-scrape

i = 0   # hitungan jumlah data yang akan di-scrape
limit = 20   # batasan jumlah data yang akan di-scrape
#last_page_reached = False # kondisi jika telah mencapai halaman terakhir atau tidak

while i < limit:

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    # mendapatkan container dari setiap profile
    containers = soup.find_all("div", class_="mb1")

    profiles = []   # list untuk menampung data nama dan link dari list containers

    # mengumpulkan nama dan link dari list container
    for p in containers:

        if(p.find("div", class_="t-roman t-sans")):

            # mendapatkan nama user
            n1 = p.find("div", class_="t-roman t-sans")
            n2 = n1.find("span", attrs={"dir" : "ltr"})
            name = n2.find("span", attrs={"aria-hidden" : "true"}).text.strip()

            # mendapatkan keterangan/status karir user (work)
            work = ""
            if(p.find("div", class_="entity-result__primary-subtitle t-14 t-black t-normal")):
                work = p.find("div", class_="entity-result__primary-subtitle t-14 t-black t-normal").text.strip()

            # mendapatkan link profile
            l1 = p.find("span", class_="entity-result__title-text t-16")
            link = l1.find("a", class_="app-aware-link").get("href")

            # memasukkan nama dan link dalam list
            data = {"name" : name, "work" : work, "link" : link}
            profiles.append(data)

    # mengumpulkan link dari profile yang akan di-scrape
    for l in profiles:
        # jika belum mencapai limit data
        if i < limit:
            # membuka database profile user
            with open("D:\\Dokumen\\dashboardPro\\people_data.json", "r") as pd:
                people_data = json.load(pd)
            # jika database tidak kosong  
            if len(people_data) != 0:
                p = 0
                match_found = False # memeriksa jika ditemukan match data user
                # menelusuri jika data user telah terekam dalam database profile user
                while p < len(people_data):
                    # jika data user telah terekam
                    #   bersihkan link untuk dibandingkan dengan link pada database profile user
                    clean_link = l["link"].split("?")
                    modified_link = clean_link[0] + "/"
                    # mencari match antar nama atau link
                    if l["name"] == people_data[p]["name"] or modified_link == people_data[p]["link"]:
                        match_found = True # match ditemukan
                        # jika ada pada list dan database match/sama
                        if l["name"] == people_data[p]["name"] and l["work"] == people_data[p]["work"]:
                            p = len(people_data) # menghentikan iterasi
                        # jika ada data yang berbeda antar list dan database
                        else:
                            link_list.append(l["link"]) # tambah link profile ke list
                            i += 1
                            p = len(people_data) # menghentikan iterasi
                    p += 1
                # jika tidak ditemukan match data
                if match_found == False:
                     # menambahkan link pada list link
                    link_list.append(l["link"])
                    i += 1
            # jika database kosong
            else:
                link_list.append(l["link"])
                i += 1

    # jika jumlah data belum mencapai limit
    if i < limit:
        next_button = driver.find_element(By.XPATH, "//button[@type='button' and @aria-label='Next']")
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        # jika terdapat tombol "Next"
        if next_button.is_enabled() == True:
            # klik tombol "Next"
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @aria-label='Next']")))
            next_button.click()
            WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@class='mb1']")))
            sleep(randint(1, 3))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//button[@type='button' and @aria-label='Next']")))
            next_button = driver.find_element(By.XPATH, "//button[@type='button' and @aria-label='Next']")
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            sleep(randint(1, 3))
        # jika tidak terdapat tombol "Next"
        else:
            # sudah mencapai halaman akhir
            i = limit

# Proses scraping profile LinkedIn alumni
with open("D:\\Dokumen\\dashboardPro\\people_data.json", "r+") as pd:
    people_data = json.load(pd)

if len(link_list) != 0:

    for dsnt_link in link_list:

        driver.get(dsnt_link)
        sleep(randint(3, 5))
        
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

            link = driver.current_url

            # Mengambil data Experience

            experience = []

            # Jika ada element "navigation-index-see-all-experiences"
            if(soup.find("a", attrs={"id" : "navigation-index-see-all-experiences"})):

                # Navigasi ke halaman experience
                navigation_button = driver.find_element(By.XPATH, "//*[@id='navigation-index-see-all-experiences']")
                driver.execute_script("arguments[0].scrollIntoView();", navigation_button)

                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navigation-index-see-all-experiences']")))
                driver.execute_script("arguments[0].click();", navigation_button)
                sleep(randint(3, 5))

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@data-view-name='profile-component-entity']")))
                sleep(randint(1, 3))
                
                experien = driver.page_source
                soup = BeautifulSoup(experien, "html.parser")

                # Ekstraksi data experience
                exp = soup.find_all("div", attrs={"data-view-name" : "profile-component-entity"})

                for e in exp:
                    exprn = e.find("div", class_="display-flex flex-row justify-space-between")

                    # Jika data experience bukan uraian
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

                    # Jika data experience adalah uraian
                    else:
                        if(exprn.find("span", class_="t-14 t-normal")):

                            # Mencari lokasi bekerja
                            exp_loc = ""

                            cpy = exprn.find("div", class_="display-flex align-items-center mr1 hoverable-link-text t-bold")
                            company = cpy.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                            job_type = ""
                            if(exprn.find("span", class_="t-14 t-normal")):
                                tp = exprn.find("span", class_="t-14 t-normal")
                                job_and_time = tp.find("span", attrs={"aria-hidden" : "true"}).text.strip()
                                job_type = job_and_time.split("\u00b7")[0].strip()

                            # lokasi bekerja + tipe pekerjaan
                            if job_type:
                                exp_loc = company + " \u00b7 " + job_type
                            else:
                                exp_loc = company

                            # Menampung container experience
                            if(e.find("div", class_="pvs-list__container")):
                                exp_container = e.find("div", class_="pvs-list__container")
                                extd_exp = exp_container.find_all("div", attrs={"data-view-name" : "profile-component-entity"})

                                for ep in extd_exp:

                                    data_container = ep.find("div", class_="display-flex flex-row justify-space-between")

                                    if(data_container.find("div", class_="display-flex align-items-center mr1 hoverable-link-text t-bold")):
                                        n = data_container.find("div", class_="display-flex align-items-center mr1 hoverable-link-text t-bold")
                                        exp_name = n.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                                        exp_tm = ""
                                        if(data_container.find_all("span", class_="t-14 t-normal t-black--light")):
                                            grey_text = data_container.find_all("span", class_="t-14 t-normal t-black--light")
                                            for t in grey_text:
                                                if(t.find("span", class_="pvs-entity__caption-wrapper")):
                                                    exp_tm = t.find("span", class_="pvs-entity__caption-wrapper").text.strip()

                                        exp_dict = {"name" : exp_name, "location" : exp_loc, "time" : exp_tm}
                                        experience.append(exp_dict)
                        
            # Jika tidak ada element "navigation-index-see-all-experiences"
            else:

                # Mencari container/card yang menampung data experience
                experien = driver.page_source
                soup = BeautifulSoup(experien, "html.parser")
                expcl = soup.find_all("section", attrs={"data-view-name" : "profile-card"})

                for i in expcl:
                    if(i.find("h2", class_="pvs-header__title text-heading-large")):
                        head = i.find("h2", class_="pvs-header__title text-heading-large")
                        if(head.find("span", attrs={"aria-hidden" : "true"}).text.strip() == "Experience"):

                            # Ekstraksi data experience
                            exp = i.find_all("div", attrs={"data-view-name" : "profile-component-entity"})

                            for e in exp:
                                exprn = e.find("div", class_="display-flex flex-row justify-space-between")

                                # Jika data experience bukan uraian
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

                                # Jika data experience adalah uraian
                                else:
                                    if(exprn.find("a", attrs={"data-field" : "experience_company_logo"})):
                                        # Mencari lokasi bekerja
                                        exp_loc = ""

                                        c = exprn.find("a", attrs={"data-field" : "experience_company_logo"})
                                        cpy = c.find("div", class_="display-flex align-items-center mr1 hoverable-link-text t-bold")
                                        company = cpy.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                                        job_type = ""
                                        if(c.find("span", class_="t-14 t-normal")):
                                            tp = c.find("span", class_="t-14 t-normal")
                                            job_and_time = tp.find("span", attrs={"aria-hidden" : "true"}).text.strip()
                                            job_type = job_and_time.split("\u00b7")[0].strip()

                                        # lokasi bekerja + tipe pekerjaan
                                        if job_type:
                                            exp_loc = company + " \u00b7 " + job_type
                                        else:
                                            exp_loc = company

                                        # Menampung container experience
                                        if(e.find("div", attrs={"data-view-name" : "profile-component-entity"})):
                                            extd_exp = e.find_all("div", attrs={"data-view-name" : "profile-component-entity"})

                                            for ep in extd_exp:

                                                data_container = ep.find("div", class_="display-flex flex-row justify-space-between")

                                                # Mencari dan memasukkan data experience
                                                if(data_container.find("div", class_="display-flex align-items-center mr1 hoverable-link-text t-bold")):
                                                    n = data_container.find("div", class_="display-flex align-items-center mr1 hoverable-link-text t-bold")
                                                    exp_name = n.find("span", attrs={"aria-hidden" : "true"}).text.strip()

                                                    exp_tm = ""
                                                    if(data_container.find_all("span", class_="t-14 t-normal t-black--light")):
                                                        grey_text = data_container.find_all("span", class_="t-14 t-normal t-black--light")
                                                        for t in grey_text:
                                                            if(t.find("span", class_="pvs-entity__caption-wrapper")):
                                                                exp_tm = t.find("span", class_="pvs-entity__caption-wrapper").text.strip()

                                                    exp_dict = {"name" : exp_name, "location" : exp_loc, "time" : exp_tm}
                                                    experience.append(exp_dict)    

            current_time = datetime.now()
            time_string = str(current_time)

            profile_dict = {
                "name" : name,
                "work" : work,
                "location" : loc,
                "link" : link,
                "experiences" : experience,
                "modified" : time_string
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

# Menuliskan database yang sudah terupdate pada file json database
json_data = json.dumps(people_data, indent=3)
with open("D:\\Dokumen\\dashboardPro\\people_data.json", "r+") as pd:
    pd.seek(0)
    pd.write(json_data)
    pd.truncate()

# Menutup selenium webdriver
driver.close()