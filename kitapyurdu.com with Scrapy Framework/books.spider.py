import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    page_count = 0
    file = open("books.txt","a",encoding="utf-8")
    book_count = 1
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/best_sellers&list_id=1&filter_in_stock=1&filter_in_stock=1&page=1"
    ]

    def parse(self, response):
        kitapismi = response.css("div.name.ellipsis a span::text").extract()
        kitapyazari = response.css("div.author.compact.ellipsis a.alt::text").extract()
        kitapyayinevi = response.css("div.publisher span a.alt span::text").extract()

        i = 0
        while (i <len(kitapismi)):
            """yield {
                "name":kitapismi[i],
                "author":kitapyazari[i],
                "publisher":kitapyayinevi[i]
            }"""
            self.file.write("******************" +"\n")
            self.file.write(str(self.book_count) +".\n")
            self.file.write("Kitap İsmi :" +kitapismi[i] +"\n")
            self.file.write("Kitap Yazarı : " +kitapyazari[i]+ "\n")
            self.file.write("Kitap Yayınevi :" + kitapyayinevi[i] +"\n")
            
            self.book_count += 1
            i+=1
        next_url = response.css("a.next::attr(href)").extract_first()
        self.page_count += 1
        if next_url is not None and self.page_count != 5:
            yield scrapy.Request(url=next_url,callback= self.parse)
        else:
            self.file.close()


        

