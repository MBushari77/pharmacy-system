from peewee import *
import datetime
import json

class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

db = SqliteDatabase('p_database.db')
# PRODUCTS TABLE
class Product(Model):
	name = CharField()
	madeIn = CharField()
	price = IntegerField()
	ppp = IntegerField()
	totPs = IntegerField()
	expd = CharField()
	grams = IntegerField()
	oldPack = IntegerField()
	expYear = IntegerField()
	expMonth = IntegerField()
	expDay = IntegerField()
	costPBC = IntegerField() # sear altaklifa
	active = BooleanField(default=True)
	# counter = IntegerField()

	class Meta:
		database = db

# DEAL TABLE
class Deal(Model):
	number = CharField()
	date = CharField()
	data = JSONField()
	isDone = BooleanField(default=False)
	price = IntegerField()
	userId = IntegerField()

	class Meta:
		database = db

# USER TABLE
class User(Model):
	username = CharField()
	password = CharField()
	userType = CharField()
	lastDeal = CharField(default='---')
	counter = IntegerField(default=0)

	class Meta:
		database = db

# USER TABLE
class Cut(Model):
	about = CharField()
	mount = IntegerField()
	date = CharField()

	class Meta:
		database = db




# initialize the database
def initialize_db():
	db.connect()
	db.create_tables([Product, Deal, User, Cut], safe = True)

initialize_db()

# >>> q = Day.select().where((Day.month == 'jan') & (Day.room == 1) & (Day.num <= 10)).get()
# >>> q.status = 'booked'
# >>> q.save()

# User.create(username="admin", password="admin", userType="admin")