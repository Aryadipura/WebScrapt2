from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import json

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.adidas.co.id/sport.html")

produklist = []
i = 1

while i<=100:
    for produk in driver.find_elements_by_class_name("ProductCard "):
        driver.execute_script("arguments[0].scrollIntoView();", produk) #auto scroll
        print(produk.text.split("\n"))
        for img in produk.find_elements_by_tag_name("img"):
            print(img.get_attribute("src"))
            urllib.request.urlretrieve(img.get_attribute("src"), str(i)+".jpg")
            i = i+1
            produklist.append(
                {
                    "Kategori": produk.text.split("\n")[0],
                    "Nama_Produk": produk.text.split("\n")[1],
                    "Harga": produk.text.split("\n")[2],
                    "Warna": produk.text.split("\n")[3],
                    "Image": img.get_attribute("src")
                }
            )
    try:
        driver.find_element_by_class_name("CategoryPagination").find_element_by_link_text("NEXT").click()
    except NoSuchElementException as e:
        break

hasil_scraping = open("hasilscrapingadidas.json", "w")
json.dump(produklist, hasil_scraping, indent=6)
hasil_scraping.close()

driver.quit