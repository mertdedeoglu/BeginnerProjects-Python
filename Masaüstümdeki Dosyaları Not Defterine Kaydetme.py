import os #Os modulünü içeri aktarıyoruz.
dizinimiz = os.chdir("C:\\Users\\ITOPYA\\Desktop\\MASAÜSTÜ") # os.chdir() fonksiyonu ile masaüstü dizinine gidiyoruz.
klasorler=os.listdir(dizinimiz) # os.listdir() fonksiyonu ile masaüstündeki tüm dosyaları listeliyoruz.

for i in klasorler:   # Masaüstündeki tüm dosyaların üzerinde işlem yapabilmek için for döngüsü ile geziniyoruz.
    if i.endswith(".txt"):   # Txt dosyalarını ayıklamak için koşul sağlıyorum.
        with open("Txt Dosyası.txt", "a", encoding="utf-8") as f: # Txt dosyalarını bir txt dosyası açtırıp yazdırmak üzere dosya açıyoruz.
            f.write(i+"\n")
    if i.endswith(".pdf"):   # Pdf dosyalarını ayıklamak için koşul sağlıyorum.
        with open("Pdf Dosyası.txt", "a", encoding="utf-8") as f: # Pdf dosyalarını bir txt dosyası açtırıp yazdırmak üzere dosya açıyoruz.
            f.write(i+"\n")
    if i.endswith(".docx"):   # Docx dosyalarını ayıklamak için koşul sağlıyorum.
        with open("Docx Dosyası.txt", "a", encoding="utf-8") as f: # Docx dosyalarını bir txt dosyası açtırıp yazdırmak üzere dosya açıyoruz.
            f.write(i+"\n")
