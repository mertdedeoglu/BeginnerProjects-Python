from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 

browser = webdriver.Edge(executable_path=r'C:\Users\Dede\Downloads\edgedriver_win64\MSEdgeDriver.exe')
browser.get("https://www.instagram.com/")
time.sleep(2)

browser.find_element_by_name("username").send_keys("username")
browser.find_element_by_name("password").send_keys("password"+ Keys.ENTER)

time.sleep(3)

browser.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[6]/span").click()
time.sleep(2)
browser.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/a[1]").click()
time.sleep(2)

button = browser.find_elements_by_css_selector(".Y8-fY ")[1].click()
"""followersbutton= button[1]
followersbutton.click()"""
time.sleep(3)

jscommand =""" followers = document.querySelector('.isgrP');
followers.scrollTo(0,followers.scrollHeight); 
var lenOfPage = followers.scrollHeight;
return lenOfPage;
"""
lenOfPage = browser.execute_script(jscommand)
match = False
while(match == False):
    lastcount = lenOfPage
    time.sleep(1)
    lenOfPage = browser.execute_script(jscommand)
    if lastcount == lenOfPage:
        match = True
time.sleep(5) 
followersList = []
followers = browser.find_elements_by_css_selector('.FPmhX.notranslate._0imsa')

for follower in followers :
    followersList.append(follower.text)

with open (r"c:\Users\Dede\Desktop\Selenium\İnstagram\followers.txt","w",encoding="UTF-8") as file:
    for follower in followersList:
        file.write(follower + "\n")
    
    

