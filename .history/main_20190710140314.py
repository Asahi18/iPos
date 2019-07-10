from flask import Flask,render_template,request
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
		fc.append(food.count)
	for drink in drinks:
		dc.append(drink.count)
	f=open('oreder_history.txt','w')
	f.write(tableno,fc,dc)
	f.close()


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
	#これらの情報を保存した後で厨房にも送り、その後初期化する

	for food in foods:
		food.count=0
	for drink in drinks:
		drink.count=0
	return render_template("confirm.html",title='confirm')

@app.route("/kitchen")
def kitchen():
	return render_template("kitchen.html",title='kitchen')

@app.route("/history")
def history():
	return render_template("history.html",title='history')

@app.route("/serve")
def serve():
	return "served!"

@app.route("/table")
def table():
	return render_template("table.html")

@app.route("/debug1",methods=['POST'])
def debug1():
	for food in foods:
		food.count=int(request.form[food.name])
	for drink in drinks:
		drink.count=int(request.form[drink.name])
	tableno=request.form['table']

	return render_template("debug1.html",foods=foods,drinks=drinks,tableno=tableno)