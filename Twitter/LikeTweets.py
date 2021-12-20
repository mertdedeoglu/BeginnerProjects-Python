from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Edge(executable_path=r'C:\Users\Dede\Downloads\edgedriver_win64\MSEdgeDriver.exe')

url = "https://twitter.com"
browser.get(url)
time.sleep(2)
browser.find_element_by_xpath("//*[@id='react-root']/div/div/div/main/div/div/div/div[1]/div/div[3]/div[5]/a/div/span").click() # URL gittiğinde Giriş yap butonunu bulmak için bir obje atandı.

time.sleep(2)
browser.find_element_by_xpath("//*[@autocomplete='username']").send_keys("mert.dedeoglu.1903@hotmail.com" + Keys.ENTER) # Email yerine mailimizi yazıyoruz.


time.sleep(2)
browser.find_element_by_xpath("//*[@name='text']").send_keys("ddoglumrt" + Keys.ENTER) # Adımı yazıyorum. ve enter diyorum.


time.sleep(2)
browser.find_element_by_xpath("//*[@autocomplete='current-password']").send_keys("94287m.Dede123" + Keys.ENTER) # Şifre giriyoruz. ve Enter diyip Giriş Yapıyoruz.

time.sleep(2)

browser.find_element_by_xpath("//*[@aria-label='Search and explore']").click()
time.sleep(2)
browser.find_element_by_xpath("//*[@aria-label='Search query']").send_keys("#Merhaba" + Keys.ENTER) 

time.sleep(4)
# Javascript kodu ile scrollumuzu aşağıya taşıyoruz.
lenOfPage = browser.execute_script("window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = browser.execute_script("window.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage :
        match=True
        
time.sleep(5)

begen = browser.find_elements_by_xpath("//*[@data-testid='like']") # Tüm beğeni butonlarına basar .

for i in begen:
    i.click()

browser.close() 
