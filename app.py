from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import reduce

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expense(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	value = db.Column(db.Integer, nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	month = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<Expense %r: %r zł>' % (self.name, self.value)

class Month(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Month %r, id: %r>' % (self.name, self.id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:month_id>', methods=['GET', 'POST'])
def index(month_id=''):

	if request.method == 'POST':
		new_expense = Expense(
			name=request.form['name'],
			value=request.form['value'],
			month=request.form['month']
		)

		try:
			db.session.add(new_expense)
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue adding your expense.'

	else:
		months = Month.query.order_by(Month.date_created.desc()).limit(3).all()

		if len(months) > 0:
			if not month_id:
				month_id = months[0].id

			current_month = list(filter(lambda m: m.id == month_id, months))

			if len(current_month) == 0:
				current_month = months[0]
			else:
				current_month=current_month[0]


			expenses = Expense.query.order_by(Expense.date_created).filter(Expense.month == current_month.id).all()
			balance = reduce(lambda a, b: a + b.value, expenses, 0)

			return render_template(
				'index.html',
				expenses=expenses,
				balance=balance,
				months=months,
				current_month=current_month
			)
		else:
			return render_template(
				'add-month.html',
				expenses=[],
				balance=0,
				months=[],
				current_month={ "name": "", "id": "" }
			)

@app.route('/add-month', methods=['GET', 'POST'])
def add_month():
	if request.method == 'GET':
		return redirect('/')
	else:
		month_name = request.form['month_name']
		new_month = Month(name=month_name)
		try:
			db.session.add(new_month)
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue adding your month.'

if __name__ == '__main__':
	app.run(debug=True)