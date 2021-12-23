from logging import info
from flask import Flask,request
from flask.templating import render_template
import requests

api_key = "8ef6742fc12569011ac9980c2ed68f49"
url = "http://data.fixer.io/api/latest?access_key="+api_key

app = Flask(__name__)
@app.route("/",methods = ["GET" , "POST"])
def index():
    if request.method == "POST":
        firstCurreny = request.form.get("firstCurrency")
        secondCurreny = request.form.get("secondCurrency")

        amount = request.form.get("amount")

        response = requests.get(url) # GET request atıp geri dönüş 200 kodlu bir dönüş olacak.
        # app.logger.info(response) gelen cevabın ne olduğuna bakabiliyoruz.
        infos = response.json() # json formatına çeviriyoruz.

        firstValue = infos["rates"][firstCurreny] # İnfosun içindeki rates başlığına gidip oradaki json formatını alıyoruz.
        secondValue = infos["rates"][secondCurreny]

        result = (secondValue / firstValue) * float(amount) # 1 dolar kaç tl çevirme yapıldı.

        currencyinfo=dict()

        currencyinfo["firstCurrency"] = firstCurreny
        currencyinfo["secondCurrency"] = secondCurreny
        currencyinfo["amount"] = amount
        currencyinfo["result"] = result
        return render_template("index.html", info = currencyinfo)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)