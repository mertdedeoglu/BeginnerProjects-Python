from flask import Flask,request,render_template
import requests

app = Flask(__name__)

url = "https://api.github.com/users/"
@app.route("/",methods = ["GET","POST"])
def index():

    if request.method == "POST":
        githubname = request.form.get("githubname") # Usernameyi index.html den çektik.

        response_user = requests.get(url+githubname) # Url ile usernameyi birleştirip o sayfadaki bilgileri çektik.
        response_repos = requests.get(url+githubname+"/repos") # Reposların olduğu json url'si

        repos = response_repos.json()
        user_info = response_user.json() # json formatında gösterdik.
        if "message" in user_info:
            return render_template("index.html",error = "Kullanıcı Bulunamadı") # Hata mesajı gönderiyoruz kullanıcı yok ise
        else:       
            return render_template("index.html",profile = user_info,repos = repos) # Tüm bilgileri index.html deki forma profile şeklinde gönderiyoruz.

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
