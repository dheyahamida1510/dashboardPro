# deklarasi library yang akan digunakan
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

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
driver = webdriver.Chrome(executable_path="D:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe", options=options)

# membuka halaman login LinkedIn
driver.get("https://linkedin.com/uas/login")
 
# tunggu loading halaman
time.sleep(5)

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
time.sleep(5)

# check code
#print(driver.page_source)

