import re
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import ArticleForm
from .models import Comment,Article
# Create your views here.
def index(request):
    context = {
        "numbers": [1,2,3,4,5,6,7,8]
        
    }
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles= Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})

    articles = Article.objects.all()

    return render(request,"articles.html",{"articles":articles})

@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        articleinfo =form.save(commit=False)
        articleinfo.author = request.user
        articleinfo.save()
        messages.success(request,"Makaleniz Başarıyla Oluşturuldu.")
        return render(request,"dashboard.html")

    return render(request,"addarticle.html",{"form":form})
def detail(request,id):
    # article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article,id=id)

    comments = article.comments.all()
    
    return render(request,"detail.html",{"article":article,"comments":comments})
    
@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article) # Tüm bilgileri instance sayesinde içeri gönderiyoruz.
    if form.is_valid():
        articleinfo =form.save(commit=False)
        articleinfo.author = request.user
        articleinfo.save()
        messages.success(request,"Makaleniz Başarıyla Güncellendi.")
        return render(request,"dashboard.html")

    return render(request,"update.html",{"form":form})
@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()

    messages.success(request,"Makale Başarıyla Silindi.")
    return redirect("user:dashboard")

def addcomment(request,id):
    article = get_object_or_404(Article,id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))

