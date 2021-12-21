from selenium import webdriver
import random
import time

browser = webdriver.Edge(executable_path=r'C:\Users\Dede\Downloads\edgedriver_win64\MSEdgeDriver.exe')

url = "https://eksisozluk.com/mustafa-kemal-ataturk--34712?p="
pageCount = 1
cümleler = [] # Boş bir liste
entryCount = 1

while pageCount <= 10: # Döngü oluşturuyoruz.
    randomPage = random.randint(1,1290) # 1 ile 1290 arasında rastgele sayı veriyor.
    newUrl = url + str(randomPage) # Yeni url'ye yukarıdakinin sonunda string bir sayı getirerek sayfaya gidiyor.
    browser.get(newUrl) # 10 defa sayfalara gidiyor.
    elements = browser.find_elements_by_css_selector(".content") # classı .content olanı bul ve getir.
    for element in elements :
        cümleler.append(element.text) # Döngüden gelen tüm cümleleri yukarıdaki listeye atar.  
    pageCount +=1


with open ("entries.txt", "w", encoding="UTF-8") as file:
    for entry in cümleler:
        file.write(str(entryCount)+".\n" + entry + "\n" ) # Güzel bir yazım ile txt dosyasına yazdırılır)
        file.write("*********************************************")
        entryCount += 1
    


browser.close() # Sayfa kapanıyor.





