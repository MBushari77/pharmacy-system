from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import datetime
from model import *
# from bson import *
from functions import *
import os
import json


# initializing flask
app = Flask(__name__)
app.secret_key = os.urandom(24)


# LOGIN PAGE ROUTE
@app.route('/')
def index():
	try:
		if session['userType'] == 'admin':
			return redirect(url_for('store'))
		elif session['userType'] == 'pharmacist':
			return redirect(url_for('makelist'))
		elif session['userType'] == 'accounter':
			return redirect(url_for('deals'))
	except KeyError:
		return render_template('login.html')

# LOGIN PAGE ROUTE
@app.route('/logingin', methods=['GET', 'POST'])
def logingin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		for user in User.select():
			if (user.username == username) & (user.password == password):
				session['userType'] = user.userType
				session['userId'] = user.id
				if session['userType'] == 'admin':
					return redirect(url_for('store'))
				elif session['userType'] == 'pharmacist':
					return redirect(url_for('makelist'))
				elif session['userType'] == 'accounter':
					return redirect(url_for('deals'))
		return 'not found'

# LIST THE DEALS
@app.route('/deals')
def deals():
	try:
		deals = []
		for d in Deal.select().where(Deal.isDone == False):
			if d.date == str(datetime.datetime.now())[0:10]:
				deals.append({'id': d.id, 'number': d.number, 'isDone': d.isDone, 'price': d.price})
		deals.reverse()
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('deals.html', deals=deals, userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# LIST THE DEALS
@app.route('/donedeals')
def donedeals():
	try:
		deals = []
		for d in Deal.select().where(Deal.isDone == True):
			if d.date == str(datetime.datetime.now())[0:10]:
				deals.append({'id': d.id, 'number': d.number, 'isDone': d.isDone, 'price': d.price, 'data':d.data})
		deals.reverse()
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('donedeals.html', deals=deals, userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# ADD NEW PRODUCT
@app.route('/newproduct')
def newproduct():
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('newproduct.html', userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# ADDING PRODUCT
@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
	try:
		if request.method == 'POST':
			Product.create(
				name = request.form['name'],
				price = request.form['price'],
				madeIn = request.form['madeIn'], 
				ppp = request.form['ppp'],
				grams = request.form['grams'],
				oldPack = request.form['pNo'],
				expYear = int(str(request.form['expd'])[0:4]),
				expMonth = int(str(request.form['expd'])[5:7]),
				expDay = int(str(request.form['expd'])[8:10]),
				expd = str(request.form['expd']),
				totPs = int(int(request.form['pNo']) * int(request.form['ppp'])),
				costPBC = request.form['costPBC']
			)
			# last = Product.select().where((Product.name == request.form['name']) & (Product.madeIn == request.form['madeIn']))
			return redirect(url_for('newproduct'))
	except KeyError:
		return redirect(url_for('index'))


# EDIT PRODUCT
@app.route('/searchproduct')
def searchproduct():
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('searchproduct.html', userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# MAKE A LIST OF PRODUCTS
@app.route('/makelist')
def makelist():
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('makelist.html', userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# ADD NEW USER
@app.route('/newuser')
def newuser():
	# return render_template('newuser.html', userType='admin')
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('newuser.html', userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# EDITING PRODUCT
@app.route('/editingproduct')
def editingproduct():
	data = []
	for pro in Product.select().where((Product.totPs > 0) & (Product.active == True)):
		data.append({'id': pro.id, 'name': pro.name, 'madeIn': pro.madeIn, 'price': pro.price})
	print(data)
	return jsonify({'data': data})

# STORE OF THE MIDKIT
@app.route('/store')
def store():
	try:
		allProducts = Product.select().where(Product.active == True)
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('store.html', allProducts=allProducts, todayDate=todayDate, userType=session['userType'])
	except KeyError:
		return redirect(url_for('index'))

# DAILY DEALS
@app.route('/daily/<selectedDate>')
def daily(selectedDate):
	try:
		listOfElemn = []
		dealsIds = []
		dealsDict = dict()
		deals =  Deal.select().where(Deal.isDone == True, Deal.date == selectedDate)
		for deal in deals:
			for did in deal.data:
				dealsIds.append(did['id'])
			# print("deal.data")
			# print(deal.data)
		# deals id's list
		dictOfElems = getRepPro(dealsIds)
		# print("dictOfElems")
		# print(dictOfElems)
		# print("###################################")
		for d in dictOfElems:
			pro = 0
			for pro in Product.select().where(Product.id == int(d)):
				dictOfElems[int(d)]['name'] = pro.name
				dictOfElems[int(d)]['price'] = pro.price
				dictOfElems[int(d)]['costPBC'] = pro.costPBC
				dictOfElems[int(d)]['ppp'] = pro.ppp
				dictOfElems[int(d)]['totPs'] = pro.totPs

			for deal in deals:
				# print(deal.data)
				for dd in deal.data:
					if dd['id'] == int(d):
						dictOfElems[int(d)]['pices'] += dd['pices']
					# print(deal)
					# if deal['id'] == int(d):
					# 	dictOfElems[int(d)]['pices'] += deal['pices']
					# print('deal.data')
					# print(deal.data)
				# print("************************")
				# print(dictOfElems)
			listOfElemn.append(dictOfElems[int(d)])
		cuts = Cut.select().where(Cut.date == selectedDate)
		todayDate = str(datetime.datetime.now())[0:10]
		# GET THE TOTOAL OF THE PRODUCTS MOUNT
		totalOfProductsMount = 0
		for pro in Product.select().where(Product.active == True):
			totalOfProductsMount += ((pro.totPs / pro.ppp) * pro.costPBC)
		return render_template('daily.html', listOfElemn=listOfElemn, 
			cuts=cuts, userType=session['userType'], todayDate=todayDate, 
			totalOfProductsMount=totalOfProductsMount)
	except KeyError:
		return redirect(url_for('index'))

# ADD NEW USER
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		User.create(
			username = request.form['username'],
			password = request.form['password'],
			userType = request.form['userType']
		)
	# redirect to show all users page
	return redirect(url_for('allusers'))

# SHOW USERS
@app.route('/allusers')
def allusers():
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		users = User.select()
		return render_template('allusers.html', users=users, userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# run the app automatically
# runpy.run_path('wb.py')
@app.route('/all')
def all():
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('show.html', userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# ADD NEW CUT
@app.route('/newcut')
def newcut():
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		return render_template('newcut.html', userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))


# SAVE NEW CUT
@app.route('/savenewcut', methods=['GET', 'POST'])
def savenewcut():
	if request.method == 'POST':
		Cut.create(
			mount = request.form['mount'],
			about = request.form['about'],
			date = str(datetime.datetime.now())[0:10]
		)
	return redirect(url_for('deals'))


# PEEWEE MODEL TO JSON
@app.route('/show')
def show():
	data = []
	for pro in Product.select():
		data.append({'id': pro.id, 'name': pro.name, 'madeIn': pro.madeIn})
	print(data)
	return jsonify({'data': data})

# GET JSON FILE
@app.route('/getjson', methods=['GET', 'POST'])
def getjson():
	if request.method == 'POST':
		jsonData = request.get_json()
		totalOfPrice = 0
		for i in range(len(jsonData)):
			totalOfPrice += ((jsonData[i]['pices'] * jsonData[i]['price']) - ((jsonData[i]['discount']/100) * (jsonData[i]['pices'] * jsonData[i]['price'])))
		# INSERT THE JSON AND THE TOTAL PRICE INTO THE DEAL OBJECT
		user = 0
		for u in User.select():
			if u.id == session['userId']:
				user = u
		# print(type(user.id))
		thisDeal = "{}-{}".format(user.id, user.counter)
		print(thisDeal)
		Deal.create(
			number = thisDeal,
			date = str(datetime.datetime.now())[0:10],
			data = jsonData,
			price = totalOfPrice,
			userId = user.id
		)
		user.get()
		user.counter = (user.counter+1 % 1000)
		user.lastDeal = thisDeal
		user.save()


		return 'done' #redirect(url_for('makelist'))

# DEAL PAYING
@app.route('/paid/<int:id>')
def paid(id):
	deal = 0
	for d in Deal.select():
		if d.id == id:
			deal = d
	print(deal.data)
	# THE FUNCTION START FROM HERE
	totalOfPrice = deal.price
	jsonData = deal.data
	for i in range(len(jsonData)):
		totalOfPrice += ((jsonData[i]['pices'] * jsonData[i]['price']) - ((jsonData[i]['discount']/100) * (jsonData[i]['pices'] * jsonData[i]['price'])))
		
		product = Product.select().where(Product.id == jsonData[i]['id']).get()
		product.totPs -= jsonData[i]['pices']
		product.save()
	# DELETE THE DEAL BUT WE CAN MAKE IT DISABLE
	# Deal.delete().where(Deal.id == id).execute()
	deal.get()
	deal.isDone = True
	deal.save()
	print("deal data #$%#$%&$%^&$^*$^&$%^&$%^&$%^&$%")
	print(deal.data)
	return redirect(url_for('deals'))
	

# GET THE LAST DEAL NUBER
@app.route('/dealnum')
def dealnum():
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		"""# ROUTING TO SHOW THE ID OF THE CURRENT
		 USER AND THE USER COUNTER % 1000 """
		user = 0
		for u in User.select():
			if u.id == session['userId']:
				user = u
		lastDeal = user.lastDeal
		return render_template('dealnumber.html', lastDeal=lastDeal, userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))


# GET PRODUCT TO SELL
@app.route('/getproducts')
def getproducts():
	data = []
	for pro in Product.select():
		data.append({'id': pro.id, 'name': pro.name, 'madeIn': pro.madeIn, 'price': pro.price})
	print(data)
	return jsonify({'data': data})

# NOTIFY ROUTE
@app.route('/notify')
def notify():
	try:
		todayDate = str(datetime.datetime.now())[0:10]
		prosArr = []
		today = str(datetime.datetime.now())[0:10].split('-')
		year = int(today[0])
		month = int(today[1])
		day = int(today[2])
		date1 = datetime.date(year, month, day)
		for pro in Product.select().where(Product.active == True):
			date2 = datetime.date(pro.expYear, pro.expMonth, pro.expDay)
			delta = date2 - date1
			if delta.days <= 60:
				prosArr.append({'id': pro.id, 'name': pro.name, 'left': (pro.totPs/pro.ppp), 'expd': pro.expd, 'supplier': pro.madeIn})

		return render_template('notify.html', pros=prosArr, userType=session['userType'], todayDate=todayDate)
	except KeyError:
		return redirect(url_for('index'))

# DELETE PRODUCT
@app.route('/deleteproduct/<int:id>')
def deleteproduct(id):
	pro = 0
	for p in Product.select().where(Product.id == id):
		pro = p
	pro.get()
	pro.active = False
	pro.save()
	return redirect(url_for('notify'))

@app.route('/logout')
def logout():
	session['userType'] = 'null'
	session['userId'] = 'null'
	del session['userType']
	del session['userId']
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True)

