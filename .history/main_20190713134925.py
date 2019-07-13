from flask import Flask,render_template,request,redirect
import flask_login
import csv
from datetime import datetime
import pandas as pd
app=Flask(__name__)
app.secret_key='deep learning corsera'
login_manager=flask_login.LoginManager()
login_manager.init_app(app)

class Menu:
    def __init__(self,name,price):
        self.name=name
        self.price=price
        self.count=0

food1=Menu("タコス",300)
food2=Menu("ポンデケージョ",200)
drink1=Menu("チチャモラーダ",200)
drink2=Menu("アグアデオルチャダ",300)
foods=[food1,food2]
drinks=[drink1,drink2]

p_id="cafelatina"
p_pwd="elsariri"

def save_order(tableno,foods,drinks):
	fc=[]
	dc=[]
	for food in foods:
		fc.append(str(food.count))
	for drink in drinks:
		dc.append(str(drink.count))
	order_data=[datetime.now(),tableno,]+fc+dc

	with open('order_history.csv','a') as f:
		writer=csv.writer(f)
		writer.writerow(order_data)

	with open('kitchen_f.csv','a') as f:
		writer=csv.writer(f)
		kitchen_food=[datetime.now().strftime('%H:%M:%S'),tableno,]+fc
		writer.writerow(kitchen_food)

	with open('kitchen_d.csv','a') as f:
		writer=csv.writer(f)
		kitchen_drink=[datetime.now().strftime('%H:%M:%S'),tableno,]+dc
		writer.writerow(kitchen_drink)

class User(flask_login.UserMixin):
	pass

users=[]
with open('users.csv','r') as f:
	reader=csv.reader(f)
	for row in reader:
		users.append(row)

with open('users.csv','a') as f:
	writer=csv.writer(f)
	writer.writerow(new_user)




@login_manager.user_loader
def user_loader(u_name):
	if u_name not in users:
		return render_template("error_login.html",msg="このユーザーはアカウント登録されていません")
	user=User()
	user.name=u_name
	return user

@login_manager.request_loader
def request_loader(request):
	u_name=request.form['u_name']
	if u_name not in users:
		return render_template("error_login.html",msg="このユーザーはアカウント登録されていません")
	user=User()
	user.id=u_name
	user.is_auth=request.form['password']==p_pwd
	return user

@app.route("/register")
def register():
	return render_template("register.html")

@app.route("/register_check",methods=['POST'])
def register_check():
	new_user=request.form['u_name']
	new_id=request.form['id']
	new_pwd=request.form['password']
	if new_id!=p_id or new_pwd!=p_pwd:
		return render_template("error_login.html",msg="不正なIDまたはpasswordです")
	users=[]
	with open('users.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			users.append(row)
	if users.count(new_user)!=0:
		return render_template("error_login.html",msg="既に登録されている名前です")
	with open('users.csv','a') as f:
		writer=csv.writer(f)
		writer.writerow(new_user)
	return render_template("login.html")

@app.route("/login_check",methods=['POST'])
def login_check():
	u_name=request.form['u_name']
	if request.form['password']==users[u_name]:
		user=User()
		user.name=u_name
		flask_login.login_user(user)
		return redirect('/')
	return render_template("error_login.html",msg="ログインできませんでした")

@app.route("/logout")
def logout():
	flask_login.logout_user()
	return render_template("error_message.html",msg="ログアウトしました")

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template("error_login.html",msg="ログインされていません")

def error_message(msg):
	return render_template("error_message.html",title='error_message',msg=msg)

@app.route("/")
def home():
	return render_template("index.html",title='index')

@app.route("/table")
def table():
	return render_template("table.html")

@app.route("/menu",methods=['POST'])
def menu():
	tableno=request.form['table']
	if tableno=='0':
		return error_message("テーブル番号を選択してください")
	else:
		return render_template("menu.html",title='menu',foods=foods,drinks=drinks,tableno=tableno)

@app.route("/check",methods=['POST'])
def check():
	for food in foods:
		food.count=int(request.form[food.name])
	for drink in drinks:
		drink.count=int(request.form[drink.name])

	tableno=request.form['table']

	sum=0
	for food in foods:
		sum += food.count * food.price
	for drink in drinks:
		sum += drink.count * drink.price

	return render_template("check.html",title='check',foods=foods,drinks=drinks,sum=sum,tableno=tableno)

@app.route("/confirm",methods=['POST'])
def confirm():
	for food in foods:
		food.count=int(request.form[food.name])
	for drink in drinks:
		drink.count=int(request.form[drink.name])
	tableno=request.form['table']

	save_order(tableno,foods,drinks)

	for food in foods:
		food.count=0
	for drink in drinks:
		drink.count=0
	return render_template("confirm.html",title='confirm')

@app.route("/kitchen")
def kitchen():
	return render_template("kitchen.html",title='kitchen')

@app.route("/kitchen_food")
def kitchen_food():
	fn=[]
	for food in foods:
		fn.append(food.name)
	fnt=['time','table']+fn
	ft=[]
	with open('kitchen_f.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			ft.append(row)
	num_f=range(len(ft))
	if len(ft)==0:
		return render_template("error_message.html",msg="まだ注文はありません")
	else:
		return render_template("kitchen_food.html",title='kitchen_food',fnt=fnt,ft=ft,num_f=num_f)

@app.route("/kitchen_drink")
def kitchen_drink():
	dn=[]
	for drink in drinks:
		dn.append(drink.name)
	dnt=['time','table']+dn
	dt=[]
	with open('kitchen_d.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			dt.append(row)
	num_d=range(len(dt))
	if len(dt)==0:
		return render_template("error_message.html",msg="まだ注文はありません")
	else:
		return render_template("kitchen_drink.html",title='kitchen_drink',dnt=dnt,dt=dt,num_d=num_d)

@app.route("/served_f",methods=['POST'])
def served_f():
	ft=[]
	f=open('kitchen_f.csv','r') 
	reader=csv.reader(f)
	for row in reader:
		ft.append(row)
	f.close()
	idx=int(request.form['servedno_f'])
	ft.pop(idx)
	with open('kitchen_f.csv','w') as f:
		writer=csv.writer(f,lineterminator="\n")
		writer.writerows(ft)
	return render_template("served.html",key="food")

@app.route("/served_d",methods=['POST'])
def served_d():
	dt=[]
	f=open('kitchen_d.csv','r') 
	reader=csv.reader(f,lineterminator="\n")
	for row in reader:
		dt.append(row)
	f.close()
	idx=int(request.form['servedno_d'])
	dt.pop(idx)
	with open('kitchen_d.csv','w') as f:
		writer=csv.writer(f)
		writer.writerows(dt)
	return render_template("served.html",key="drink")

@app.route("/history")
def history():
	history=[]
	with open('order_history.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			history.append(row)
	menus=[]
	for food in foods:
		menus.append(food.name)
	for drink in drinks:
		menus.append(drink.name)
	header=['time','table']+menus
	num=len(history)
	if num==0:
		return render_template("error_message.html",msg='まだ注文が記録されていません')
	else:
		return render_template("history.html",title='history',history=history,header=header,num=num)

@app.route("/correct",methods=['POST'])
def correct():
	comment=request.form['comment']
	idx=request.form['orderno']
	if comment=='':
		return render_template("error_message",msg='訂正内容が記入されていません')
	else:
		with open('corrected.csv','a') as f:
			writer=csv.writer(f)
			writer.writerow([idx,comment])
		return render_template("correct.html")

@app.route("/debug1")
def debug1():
	fn=[]
	for food in foods:
		fn.append(food.name)
	fnt=['time','table']+fn
	df_f=pd.read_csv('kitchen_f.csv',names=fnt)
	df_f.to_html('debug1.html')
	return render_template("debug1.html")