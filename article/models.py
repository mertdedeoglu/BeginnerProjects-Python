from tabnanny import verbose
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE, verbose_name="Yazar") # Diğer tablodaki usera ait yazar tablosundaki isim geliyor ve Yazar silinirse burdada silinir.
    title = models.CharField(max_length=50,verbose_name="Başlık") # Başlık kısmı
    content = RichTextField() # İçeriği yazabileceğimiz konu
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi") # Otomatik olarak date tarihi oluşturdu
    article_image = models.FileField(blank= True,null = True,verbose_name = "Makaleye Fotoğraf Ekle")
    def __str__(self): # Admin sayfasında title gözükmesini sağlar.
        return self.title
    class Meta:
        ordering=['-created_date']
class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete= models.CASCADE,verbose_name="Makale",related_name="comments")
    comment_author = models.CharField(max_length=50,verbose_name="İsim")
    comment_content = models.CharField(max_length=150,verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True,verbose_name="Yorum Saati")
    def __str__(self): # Admin sayfasında title gözükmesini sağlar.
        return self.comment_content
    class Meta:
        ordering=['-comment_date']

""" eğer modellerde değişiklik yaparsın 
önce - python manage.py makemigrations
sonra - python manage.py migrate
"""