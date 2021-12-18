from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL 
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
# Kullanıcı Giriş Decorator 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session: # sessionun içinde logged in var mı yok mu kontrolü yapılır.
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapınız.","danger")
            return redirect(url_for("login"))        
    return decorated_function
# Kullanıcı Kayıt Formu 
class RegisterForm(Form):
    name = StringField("İsim Soyisim" , validators = [validators.Length(min=4,max = 25)])
    email = StringField("Email Adresi",validators = [validators.Email(message = "Geçersiz Email")])
    username = StringField("Kullanıcı Adı" , validators = [validators.Length(min=5,max = 35)])
    password = PasswordField("Parola" ,validators = [validators.DataRequired(message = "Lütfen bir parola belirleyin."), validators.EqualTo(fieldname = "confirm", message= "Parolanız Uyuşmuyor")])
    confirm = PasswordField("Parola Doğrula")
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

app = Flask(__name__)
app.secret_key="ybblog"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ybblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index(): 
    
    return render_template("index.html")


@app.route("/about")
def about():
   return render_template("about.html")


# Kayıt Olma 
@app.route("/register" , methods = ["GET","POST"]) # Bu url yapısı hem get hem de post methodu alabilir demek istiyoruz.
def register():
    form = RegisterForm(request.form) # yukarı bahsettiğimiz RegisterForm classının yapısını çekip form objesine eşitliyoruz.

    if request.method == "POST" and form.validate(): # Formumuzda validate fonksiyonu ile kontrol yapıp , bir sıkıntı yoksa true ,var ise false yapıcak.
        isim = form.name.data                          # Yukarıdaki formdaki bilgilerin datalarını alıp objelere dönüştürüyoruz.
        mail = form.email.data
        kullaniciadi = form.username.data
        
        sifre = sha256_crypt.encrypt(form.password.data) # Veritabanındaki şifreyi gizler.

        imlec = mysql.connection.cursor()  # Mysql veritabanında bir imleç oluşturuyoruz.

        sorgu= "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)" #SQL sorgusunda tablodaki yerleri sırasıyla değerleri ekleyeceğiz.

        imlec.execute(sorgu,(isim,mail,kullaniciadi,sifre)) #İmleç çalışır ve sorguyu çalıştırır, Demet şeklinde verilen bilgileri tablo üzerinde çalıştırır.

        mysql.connection.commit() # Veritabanında bir güncelleme bir değişiklik yapılacağı için commit komutu yapmak zorundayız.

        imlec.close() # İmleci kapatır.
        flash("Başarıyla Kayıt Oldunuz...","success") # Flash fonksiyonu, mesajımız ile ve category belirleyerek ekrana mesaj yazdırıyoruz.

        return redirect(url_for("login")) # index fonksiyonuna gitmek istediğimizi url_for ile belirtiyoruz.
    else:
        return render_template("register.html" , form = form) # Methodumuz GET olduğunda register.html sayfasına gidip formu karşımıza çıkartıyor.

# Giriş Yap İşlemi
@app.route("/login",methods = ["GET","POST"]) # Bu url'mizde GET ve POST methodları kullanılabilir.
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        sorgu = "Select * from users where username = %s" # Veritabanında usernameyi arayacağız.
        result = cursor.execute(sorgu,(username,)) # Sorgumuzu çalıştırıyoruz ve sonuç alıyoruz.Hiçbir sonuç almazsak result 0 olacak.
        if result > 0:
            data = cursor.fetchone() # Kullanıcının tüm bilgilerini almış olduk.
            real_password = data["password"] # Verilerden password bilgimizi çekiyoruz.
            if sha256_crypt.verify(password_entered,real_password): # iki parolanın aynı olup olmadığını verify ile kontrol etmiş olucaz.
                flash("Başarıyla giriş yapıldı","success")
                
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))

            else:   # Parolam yanlış ise 
                flash("Lütfen Parolanızı Doğru Giriniz.","danger")
                return redirect(url_for("login")) 

        else:
            flash("Böyle bir kullanıcı bulunmuyor.","danger")
            return redirect(url_for("login"))

    return render_template("login.html",form = form)

# Kontrol Paneli 
@app.route("/dashboard")
@login_required # Decoratora gidip sessionu sorgulayıp dashboard fonksiyonunu çalıştırır.
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles where author = %s"
    result = cursor.execute(sorgu,(session["username"],))
    if result >0:
        articles = cursor.fetchall()
        return render_template("dashboard.html",articles = articles)
    else:
        return render_template("dashboard.html")

# Detay Sayfası
@app.route("/article/<string:id>")
def articleid(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result >0 :
        article = cursor.fetchone()
        return render_template("article.html",article=article)
    else:
        return render_template("article.html")

# Çıkış Yap İşlemi
@app.route("/logout")
def logout():
    session.clear()
    flash("Başarıyla Çıkış Yapıldı.","success")
    return redirect(url_for("index"))

# Makale Oluşturma
@app.route("/addarticle", methods = ["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate(): 
        konu = form.title.data
        icerik = form.content.data

        cursor = mysql.connection.cursor()

        sorgu = "Insert into articles(title,author,content) VALUES (%s,%s,%s)"
        cursor.execute(sorgu,(konu,session["username"],icerik))

        mysql.connection.commit()
        cursor.close()
            
        flash("Makaleniz Başarıyla Eklendi","success")
        return redirect(url_for("dashboard"))

    return render_template("addarticle.html",form = form)

# Makale Sayfası
@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles" # Articles tablosundaki tüm verileri alıcak.
    result = cursor.execute(sorgu)  # Sonuçlar için sorguyu çalıştırır ve makale varsa 0 dan farklı bir değer ile sonuç gelir.

    if result > 0 :
        makale = cursor.fetchall() # Tüm verileri listenin içinde sözlük halinde alıyor.
        return render_template("articles.html",makale = makale)
    else:
        return render_template("articles.html")
    
# Arama URL
@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method=="GET":
        return redirect(url_for("articles"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "Select * from articles where title like '%"+ keyword +"%'"

        result = cursor.execute(sorgu)
        if result == 0 :
            flash("Böyle bir makale bulunmamaktadır.","warning")
            return redirect(url_for("articles"))
        else:
            makale = cursor.fetchall()
            return render_template("articles.html",makale = makale)


    
# Makale Silme
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor=mysql.connection.cursor()
    sorgu = "Select * From articles where author = %s and id = %s"

    result = cursor.execute(sorgu,(session["username"],id))

    if result > 0 :
        sorgu2= "Delete from articles where id = %s"

        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for("index"))
    else:
        flash("Böyle bir makale yoktur veya bu makaleyi silme yetkiniz yoktur.","danger")
        return redirect(url_for("index"))


# Makale Güncelleme
@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def update(id):
    if request.method =="GET":
        cursor = mysql.connection.cursor()
        sorgu = "Select * from articles where id = %s and author = %s"

        result = cursor.execute(sorgu,(id,session["username"]))
        
        if result == 0:
            flash("Makale bulunanamaktadır ya da size ait değildir.","danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm() # Makale form kısmından form şeklinde alıyoruz.

            form.title.data = article["title"] # Veritabanımızdaki verileri formda gösterir.
            form.content.data = article["content"]

            return render_template("update.html",form = form)
    else:
        #POST REQUEST
        form = ArticleForm(request.form)
        newTitle = form.title.data # Yeni verileri farklı objelere çevirdik.
        newContent = form.content.data
        
        cursor = mysql.connection.cursor()
        sorgu2 = "Update articles Set title = %s,content = %s where id = %s" # Veritabanında güncelleme yaptık.
        cursor.execute(sorgu2,(newTitle,newContent,id)) 
        mysql.connection.commit()
        
        flash("Makaleniz başarıyla güncellendi","success")
        return redirect(url_for("dashboard"))





# Makale Form 
class ArticleForm(Form):
    title = StringField("Makale Başlığı", validators= [validators.Length(min =5,max=100)])
    content = TextAreaField("Makale İçeriği", validators=[validators.Length(min=10)])  




if __name__ == "__main__":
    app.run(debug=True)
