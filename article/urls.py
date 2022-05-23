from django.contrib import admin
from django.urls import path
from article import views

app_name = "article"

urlpatterns = [
    path('create/',views.index,name="index"),
    path('',views.articles,name="articles"),
    path('addarticle/',views.addarticle,name="addarticle"),
    path('article/<int:id>',views.detail,name="detail"),
    path('update/<int:id>',views.updateArticle,name="update"),
    path('delete/<int:id>',views.deleteArticle,name="delete"),
    path('comment/<int:id>',views.addcomment,name="comment")

]
