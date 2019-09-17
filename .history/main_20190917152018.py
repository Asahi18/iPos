from flask import Flask,render_template,request,redirect
# from flask_login import login_user,logout_user,login_required,LoginManager,UserMixin
import csv
from datetime import datetime, timedelta, timezone
# import pandas as pd
app=Flask(__name__)

# app.secret_key='deep learning corsera'
# login_manager=LoginManager()
# login_manager.init_app(app)
# login_manager.login_view="users.login"

JST = timezone(timedelta(hours=+9),'JST')

class Menu:
    def __init__(self,name,price):
        self.name=name
        self.price=price
        self.count=0

food1=Menu("タコス",300)
food2=Menu("ポンデケージョ",200)
food3=Menu("チュロス",300)
drink1=Menu("チチャモラーダ",200)
drink2=Menu("アグアデオルチャダ",300)
drink3=Menu("マテ茶",200)
foods=[food1,food2,food3]
drinks=[drink1,drink2,drink3]

# p_id="cafelatina"
# p_pwd="elsariri"

def save_order(tableno,foods,drinks,name):
	fc=[]
	dc=[]
	sum_f=0
	sum_d=0
	for food in foods:
		fc.append(str(food.count))
		sum_f+=food.count
	for drink in drinks:
		dc.append(str(drink.count))
		sum_d+=drink.count
	order_data=[datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'),tableno,name]+fc+dc

	with open('order_history.csv','a') as f:
		writer=csv.writer(f)
		writer.writerow(order_data)

	if sum_f>0:
		with open('kitchen_f.csv','a') as f:
			writer=csv.writer(f)
			kitchen_food=[datetime.now(JST).strftime('%H:%M:%S'),tableno,name]+fc
			writer.writerow(kitchen_food)

	if sum_d>0:
		with open('kitchen_d.csv','a') as f:
			writer=csv.writer(f)
			kitchen_drink=[datetime.now(JST).strftime('%H:%M:%S'),tableno,name]+dc
			writer.writerow(kitchen_drink)

def error_message(msg):
	return render_template("error_message.html",title='error_message',msg=msg)

def reset(fname):
	history=[]
	with open('order_history.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			history.append(row)
	backup_name='order_history_'+fname+'.csv'
	with open(backup_name,'w') as f:
		writer=csv.writer(f,lineterminator='\n')
		writer.writerows(history)
	# with open('order_history.csv','w') as f:
	# 	pass

	comment=[]
	with open('corrected.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			comment.append(row)
	backup_name='corrected_'+fname+'.csv'
	with open(backup_name,'w') as f:
		writer=csv.writer(f,lineterminator='\n')
		writer.writerows(comment)
	# with open('corrected.csv','w') as f:
	# 	pass


##### 一番下のコード群はここにあったもので、ログイン機能の実装を試みた #####


@app.route("/")
def start():
	return redirect('/sign_up')

@app.route("/sign_up")
def sign_up():
	return render_template("name.html",title='sign_up')

@app.route("/main",methods=['POST'])
def home():
	name=request.form['name']
	if name=='':
		return error_message("名前を入力して下さい")
	if name=='reset'
		return redirect('/reset',code=307)
	return render_template("index.html",title='index',name=name)

@app.route("/table",methods=['POST'])
def table():
	name=request.form['name']
	return render_template("table.html", name=name)

@app.route("/menu",methods=['POST'])
def menu():
	name=request.form['name']
	tableno=request.form['table']
	if tableno=='0':
		return error_message("テーブル番号を選択してください")
	else:
		return render_template("menu.html",title='menu',foods=foods,drinks=drinks,tableno=tableno,name=name)

@app.route("/check",methods=['POST'])
def check():
	for food in foods:
		food.count=int(request.form[food.name])
	for drink in drinks:
		drink.count=int(request.form[drink.name])

	name=request.form['name']
	tableno=request.form['table']

	sum=0
	for food in foods:
		sum += food.count * food.price
	for drink in drinks:
		sum += drink.count * drink.price

	if sum==0:
		return error_message('商品が選択されていません')

	return render_template("check.html",title='check',foods=foods,drinks=drinks,sum=sum,tableno=tableno,name=name)

@app.route("/confirm",methods=['POST'])
def confirm():
	for food in foods:
		food.count=int(request.form[food.name])
	for drink in drinks:
		drink.count=int(request.form[drink.name])
	name=request.form['name']
	tableno=request.form['table']

	save_order(tableno,foods,drinks,name)

	for food in foods:
		food.count=0
	for drink in drinks:
		drink.count=0
	return render_template("confirm.html",title='confirm',name=name)

@app.route("/kitchen",methods=['POST'])
def kitchen():
	name=request.form['name']
	return render_template("kitchen.html",title='kitchen',name=name)

@app.route("/kitchen_food",methods=['POST'])
def kitchen_food():
	name=request.form['name']
	fn=[]
	for food in foods:
		fn.append(food.name)
	fnt=['time','table','name']+fn
	ft=[]
	with open('kitchen_f.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			ft.append(row)
	num_f=range(len(ft))
	if len(ft)==0:
		return render_template("error_message_no_order.html",msg="まだ注文はありません")
	else:
		return render_template("kitchen_food.html",title='kitchen_food',fnt=fnt,ft=ft,num_f=num_f,name=name)

@app.route("/kitchen_drink",methods=['POST'])
def kitchen_drink():
	name=request.form['name']
	dn=[]
	for drink in drinks:
		dn.append(drink.name)
	dnt=['time','table','name']+dn
	dt=[]
	with open('kitchen_d.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			dt.append(row)
	num_d=range(len(dt))
	if len(dt)==0:
		return render_template("error_message_no_order.html",msg="まだ注文はありません")
	else:
		return render_template("kitchen_drink.html",title='kitchen_drink',dnt=dnt,dt=dt,num_d=num_d,name=name)

@app.route("/served_f",methods=['POST'])
def served_f():
	name=request.form['name']
	ft=[]
	with open('kitchen_f.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			ft.append(row)
	idx=int(request.form['servedno_f'])
	ft.pop(idx)
	with open('kitchen_f.csv','w') as f:
		writer=csv.writer(f,lineterminator="\n")
		writer.writerows(ft)
	return render_template("served.html",key="food",name=name)

@app.route("/served_d",methods=['POST'])
def served_d():
	name=request.form['name']
	dt=[]
	with open('kitchen_d.csv','r') as f:
		reader=csv.reader(f,lineterminator="\n")
		for row in reader:
			dt.append(row)
	idx=int(request.form['servedno_d'])
	dt.pop(idx)
	with open('kitchen_d.csv','w') as f:
		writer=csv.writer(f)
		writer.writerows(dt)
	return render_template("served.html",key="drink",name=name)

@app.route("/history",methods=['POST'])
def history():
	name=request.form['name']
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
	header=['time','table','name']+menus
	num=len(history)
	if num==0:
		return error_message('まだ注文が記録されていません')
	else:
		return render_template("history.html",title='history',history=history,header=header,num=num,name=name)

@app.route("/correct",methods=['POST'])
def correct():
	name=request.form['name']
	comment=request.form['comment']
	idx=request.form['orderno']
	if comment=='':
		return error_message('記録内容が記入されていません')
	else:
		with open('corrected.csv','a') as f:
			writer=csv.writer(f)
			writer.writerow([datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S'),idx,name,comment])
		return render_template("correct.html",name=name)

@app.route("/comments",methods=['POST'])
def comments():
	name=request.form['name']
	header=['time','通し番号','記録者','内容']
	corrects=[]
	with open('corrected.csv','r') as f:
		reader=csv.reader(f)
		for row in reader:
			corrects.append(row)
	num=len(corrects)
	if num==0:
		return error_message('まだ備考欄が記録されていません')
	else:
		return render_template("comments.html",title='comments',header=header,name=name,corrects=corrects,num=num)

@app.route("/reset",methods=['POST'])
def reset():
	return render_template("caution.html",title='CAUTION!')

@app.route("/backup",methods=['POST'])
def backup():
	fname=request.form['fname']
	reset(fname)
	return render_template("comments.html",title='comments',header=header,name=name,corrects=corrects,num=num)


# @app.route("/debug1")
# def debug1():
# 	fn=[]
# 	for food in foods:
# 		fn.append(food.name)
# 	fnt=['time','table']+fn
# 	df_f=pd.read_csv('kitchen_f.csv',names=fnt)
# 	df_f.to_html('debug1.html')
# 	return render_template("debug1.html")






# users=[]
# with open('users.csv','r') as f:
# 	reader=csv.reader(f)
# 	for row in reader:
# 		users.append(row)

# with open('users.csv','a') as f:
# 	writer=csv.writer(f)
# 	writer.writerow(new_user)



# class User(UserMixin):
# 	pass

# @login_manager.user_loader
# def user_loader(u_name):
# 	users=[]
# 	with open('users.csv','r') as f:
# 		reader=csv.reader(f)
# 		for row in reader:
# 			users.append(row)
# 	if u_name not in users:
# 		return render_template("error_login.html",msg="このユーザーはアカウント登録されていません")
# 	user=User()
# 	user.name=u_name
# 	return user

# @login_manager.request_loader
# def request_loader(request):
# 	users=[]
# 	with open('users.csv','r') as f:
# 		reader=csv.reader(f)
# 		for row in reader:
# 			users.append(row)
# 	u_name=request.form['u_name']
# 	if u_name not in users:
# 		return render_template("error_login.html",msg="このユーザーはアカウント登録されていません")
# 	user=User()
# 	user.id=u_name
# 	user.is_authenticated=request.form['password']==p_pwd
# 	return user

# @app.route("/register")
# def register():
# 	return render_template("register.html")

# @app.route("/register_check",methods=['POST'])
# def register_check():
# 	new_user=request.form['u_name']
# 	new_id=request.form['id']
# 	new_pwd=request.form['password']
# 	if new_id!=p_id or new_pwd!=p_pwd:
# 		return render_template("error_login.html",msg="不正なIDまたはpasswordです")
# 	users=[]
# 	with open('users.csv','r') as f:
# 		reader=csv.reader(f)
# 		for row in reader:
# 			users.append(row)
# 	if users.count(new_user)!=0:
# 		return render_template("error_login.html",msg="既に登録されている名前です")
# 	with open('users.csv','a') as f:
# 		writer=csv.writer(f)
# 		writer.writerow(new_user)
# 	return redirect('/login')

# @app.route("/login")
# def login():
# 	render_template("login.html")

# @app.route("/login_check",methods=['POST'])
# def login_check():
# 	u_name=request.form['u_name']
# 	u_id=request.form['id']
# 	u_pwd=request.form['password']
# 	users=[]
# 	with open('users.csv','r') as f:
# 		reader=csv.reader(f)
# 		for row in reader:
# 			users.append(row)
# 	u_count=users.count(u_name)

# 	if u_id==p_id and u_pwd==p_pwd and u_count!=0:
# 		user=User()
# 		user.name=u_name
# 		login_user(user)
# 		return redirect('/')
# 	return render_template("error_login.html",msg="ログインできませんでした")

# @app.route("/logout")
# def logout():
# 	logout_user()
# 	return render_template("error_login.html",msg="ログアウトしました")

# @login_manager.unauthorized_handler
# def unauthorized_handler():
# 	return render_template("error_login.html",msg="ログインされていません")
