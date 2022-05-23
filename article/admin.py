from django.contrib import admin

from .models import Article,Comment

admin.site.register(Comment)

# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ["title","author","created_date"] # admin tarafında hangi objelerin görünmesini sağlar.
    list_display_links = ["title","created_date"] # Üstüne tıklamayı sağlıyor.

    search_fields = ["title"] # Arama yeri açıyor.

    list_filter = ["created_date"] # Filtrelemeyi sağlıyor.
    class Meta: # Article ile ArticleAdmin birleştiriliyor sabit kod
        model = Article
