import requests 
from bs4 import BeautifulSoup

url = "https://www.doviz.com/"
erisim = requests.get(url) # Link üzerindeki tüm bilgileri çekiyorum.
soup = erisim.content # Web sayfasının html görüntüsünü ortaya çıkarıyorum.

goruntu = BeautifulSoup(soup, "html.parser")    # Html bağlantısını güzel bir görüntü vermesi için ayıklıyorum.
isimler = goruntu.find_all("span",{"class":"name"})  # Url'deki para biriminin ismini çekiyorum.
sayılar = goruntu.find_all("span",{"class":"value"}) # Url'deki para biriminin fiyatını çekiyorum.

for isim,sayı in zip(isimler,sayılar): # İki listeyi bir listede birleştirip değerlerine erişiyorum.
    isim = isim.text
    sayı = sayı.text

    print("{} : {} ".format(isim,sayı)) # İstediğim formatta yazdırıyorum.
# Çalıştırıldığında anlık güncel fiyat bilgisini gösterir.
