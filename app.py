from flask import Flask,render_template,redirect,request,session,url_for
import random
import string
from datetime import timedelta
import db
import MySQLdb
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

app.secret_key = "".join(random.choices(string.ascii_letters,k=256))

#アカウント作成
# @app.route("/create_account")
# def create_account():
#     error = request.args.get("error")
#     return render_template("c_account.html",error=error)


# @app.route("/create_result", methods=[ 'POST' ])
# def create_result():
#     mail = request.form.get("mail")
#     pw = request.form.get("pw")
#     name = request.form.get("name")
#     bir = request.form.get("bir")
#     depa = request.form.get("depa")
#     tclass = request.form.get("tclass")
    
#     a = request.form.get("a")

#     if a == "14296":

#         db.insert(mail,pw,name,bir,depa,tclass)

#         ID = "ooooa1321@gmail.com"
#         PASS = "gogototaiga1"
#         HOST = "smtp.gmail.com"
#         PORT = 587
#         to = mail
#         body =f"""\
#             ------------------------------------------------------------------<br>
#             このメールは、学生管理システムにご登録された<br>
#             メールアドレス宛に自動送信しています。そのため、お問合せ等のメッセージをご返信いただいても、回答できません。<br>
#             ※お心当たりがない場合は、お手数ですがメールの破棄をお願いいたします。<br>
#             ------------------------------------------------------------------<br>
#             ■ご登録内容（学生管理システム申込み）<br>
#             ------------------------------------------------------------------<br>
#             ------------------------------------------------------------------<br>
#             ご登録ありがとうございました。
#             """
#         subject = "アカウントご登録確認完了のお知らせ"
#         msg = MIMEMultipart()
#         msg.attach(MIMEText(body, "html"))
#         msg["Subject"] = subject
#         msg["From"] = ID
#         msg["To"] = to
#         server=SMTP(HOST, PORT)
#         server.starttls()   
#         server.login(ID, PASS) 
#         server.send_message(msg)    

#         print("メール送信完了！")

#         return render_template("sub.html")

#     else:
#        return redirect(url_for("create_account",error="The entry is omitted or the authorization number is incorrect."))  

# 社員ログイン
# @app.route("/")
# def login():
#     error = request.args.get("error")
#     return render_template("Member_login.html",error=error)

# @app.route("/login_result", methods=['POST'])
# def login_result():
#     id = request.form.get("id")
#     pw = request.form.get("pw")

#     result = db.login(id,pw)

#     if result != None:
#         session["user"] = True 
#         session.permanent = True 
#         app.permanent_session_lifetime = timedelta(minutes=30)

#         yakusyoku = db.yakusyoku(id)
#         if yakusyoku == "一般社員":
#             return render_template("ippansyain_result.html")
#         elif yakusyoku == "主任":
#             return render_template("syunin_result.html")
#         elif yakusyoku == "部長":
#             return render_template("butyou_result.html")
#         elif yakusyoku == "常務取締役":
#             return render_template("joumu_result.html")
#         elif yakusyoku == "社長":
#             return render_template("syatyou_result.html")
#         else:
#             return redirect(url_for("login",error="yakusyoku is different"))
#     else:
#         return redirect(url_for("login",error="ID or PW is different"))

# 管理者ログイン
# @app.route("/kanrisya_login")
@app.route("/")
def login():
    error = request.args.get("error")
    return render_template("login.html",error=error)

@app.route("/kanrisya_result", methods=['POST'])
def login_result():
    id = request.form.get("id")
    pw = request.form.get("pw")

    result = db.login(id,pw)

    if result != None:
        session["user"] = True 
        session.permanent = True 
        app.permanent_session_lifetime = timedelta(minutes=30)

        return render_template("kanrisya_result.html")
    else:
        return redirect(url_for("login",error="ID or PW is different"))


#登録
@app.route("/register")
def register():
    if "user" in session:
        return render_template("register.html")
    else:
        return redirect("/")
@app.route("/register_result")
def register_result():
    id = request.args.get("id")
    pw= request.args.get("pw")
    mail = request.args.get("mail")
    name = request.args.get("name")
    department = request.args.get("department")
    jyousi_id = request.args.get("jyousi_id")
    jyousi_name = request.args.get("jyousi_name")
    yakusyoku = request.args.get("yakusyoku")
    db.insert(id,pw,mail,name,department,jyousi_id,jyousi_name,yakusyoku)
    return render_template("register-result.html",id=id,pw=pw,mail=mail,name=name,department=department,jyousi_id=jyousi_id,jyousi_name=jyousi_name,yakusyoku=yakusyoku)




#ログアウト
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")

def get_connection():
    return MySQLdb.connect(user='root',passwd="gogototaiga1",host='localhost',db='ringisyosystem',charset="utf8")

if __name__ == "__main__":
    app.run(debug=True)

    