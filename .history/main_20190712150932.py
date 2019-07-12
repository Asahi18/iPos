from flask import Flask,render_template,request
import csv
from datetime import datetime
import pandas as pd
app=Flask(__name__)

class Menu:
    def __init__(self,name,price):
        self.name=name
        self.price=price
        self.count=0
    def add(self):
        self.count+=1
    def take(self):
        self.count-=1

food1=Menu("タコス",300)
food2=Menu("ポンデケージョ",200)
drink1=Menu("チチャモラーダ",200)
drink2=Menu("アグアデオルチャダ",300)
foods=[food1,food2]
drinks=[drink1,drink2]

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

@app.route("/")
def home():
	return render_template("index.html",title='index')

@app.route("/menu",methods=['POST'])
def menu():
	tableno=request.form['table']
	return render_template("menu.html",title='menu',foods=foods,drinks=drinks,tableno=tableno)

@app.route("/add",methods=['POST'])
def add():
	for food in foods:
		food.count=int(request.form[food.name])
	for drink in drinks:
		drink.count=int(request.form[drink.name])
	return render_template("menu.html",title='menu',foods=foods,drinks=drinks)

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
	f=open('kitchen_f.csv','r') 
	reader=csv.reader(f)
	for row in reader:
		ft.append(row)
	f.close()
	return render_template("kitchen_food.html",title='kitchen_food',fnt=fnt,ft=ft)

@app.route("/kitchen_drink")
def kitchen_drink():
	dn=[]
	for drink in drinks:
		dn.append(drink.name)
	dnt=['time','table']+dn
	dt=[]
	f=open('kitchen_d.csv','r') 
	reader=csv.reader(f)
	for row in reader:
		dt.append(row)
	f.close()
	return render_template("kitchen_drink.html",title='kitchen_drink',dnt=dnt,dt=dt)

@app.route("/history")
def history():
	return render_template("history.html",title='history')

@app.route("/serve")
def serve():
	return "served!"

@app.route("/table")
def table():
	return render_template("table.html")

@app.route("/debug1")#,methods=['POST'])
def debug1():
	fn=[]
	for food in foods:
		fn.append(food.name)
	fnt=['time','table']+fn
	df_f=pd.read_csv('kitchen_f.csv',names=fnt)
	df_f.to_html('debug1.html')
	return render_template("debug1.html")