from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Accounts(db.Model):
    #Parameters for each account
    id = db.Column(db.Text, primary_key = True)
    balance = db.Column(db.Text, unique = True)
    credit = db.Column(db.Integer, unique = True) 
    picture = db.Column(db.Text, unique = True)
    name_first = db.Column(db.Text, unique = True)
    name_last = db.Column(db.Text, unique = True)
    employer = db.Column(db.Text, unique = True)
    email = db.Column(db.Text, unique = True)
    phone = db.Column(db.Integer, unique = True)
    address = db.Column(db.Text, unique = True)
    comments = db.Column(db.Text, unique = True)
    created = db.Column(db.Text, unique = True)
    tags = db.Column(db.Text, unique = True)


    def __init__(self, id, balance, credit, picture, name_first, name_last, employer, email, phone, address, comments, created, tags):
        self.id = id
        self.balance = balance
        self.credit = credit
        self.picture = picture
        self.name_first = name_first
        self.name_last = name_last
        self.employer = employer
        self.email = email
        self.phone = phone
        self.address = address
        self.comments = comments
        self.created = created
        self.tags = tags

    def serialize(self):
    """
    Returns a dictionary containing the parameters of the account
    Useful for serializing into JSON
    """
        return {
            'id' : self.id,
            'balance' : self.balance,
            'credit' : self.credit,
            'picture' : self.picture,
            'name_first' : self.name_first,
            'name_last' : self.name_last,
            'employer' : self.employer,
            'email' : self.email,
            'phone' : self.phone,
            'address' : self.address,
            'comments' : self.comments,
            'created' : self.created,
            'tags' : self.tags
        }

class AccountsSchema(ma.Schema):
    class Meta:
        #Fields to expose
        fields = ('id', 'balance', 'credit', 'picture', 'name_first', 'name_last', 'employer', 'email', 'phone', 'address', 'comments', 'created', 'tags')

account_schema = AccountsSchema()
accounts_schema = AccountsSchema(many = True)

@app.route('/')
def hello_world():
    """
    Renders static html page (home page)
    """
    message = 'Start of front end'
    return (render_template('index.html', message = message))

@app.route("/account/", methods = ["POST"])
def add_account():
    """
    POST request endpoint that creates a new account
    Return: JSON of the new account parameters
    """
    id = request.json['id']
    balance = request.json['balance']
    credit = request.json['credit']
    picture = request.json['picture']
    name_first = request.json['name_first']
    name_last = request.json['name_last']
    employer = request.json['employer']
    email = request.json['email']
    phone = request.json['phone']
    address = request.json['address']
    comments = request.json['comments']
    created = request.json['created']
    tags = request.json['tags']

    new_account = Accounts(id, balance, credit, picture, name_first, name_last, employer, email, phone, address, comments, created, tags)
    db.session.add(new_account)
    db.session.commit()

    return jsonify(new_account.serialize())

@app.route("/account", methods = ["GET"])
def get_account():
    """
    GET request endpoint that shows all accounts in the database
    Return: JSON of all accounts
    """
    all_accounts = Accounts.query.all()
    result = accounts_schema.dump(all_accounts)
    return jsonify(result.data)

@app.route("/account/<id>", methods=["GET"])
def user_detail(id):
    """
    GET request endpoint that gets an account specified by id
    Return: JSON of specific account
    """
    account = Accounts.query.get(id)
    return account_schema.jsonify(account)

@app.route("/account/<id>", methods = ["PUT"])
def account_update(id):
    """
    PUT request endpoint that updates the parameters of an account
    Return: JSON with new account parameters
    """
    account = Accounts.query.get(id)
    balance = request.json['balance']
    credit = request.json['credit']
    picture = request.json['picture']
    name_first = request.json['name_first']
    name_last = request.json['name_last']
    employer = request.json['employer']
    email = request.json['email']
    phone = request.json['phone']
    address = request.json['address']
    comments = request.json['comments']
    created = request.json['created']
    tags = request.json['tags']

    account.balance = balance
    account.credit = credit
    account.picture = picture
    account.name_first = name_first
    account.name_last = name_last
    account.employer = employer
    account.email = email
    account.phone = phone
    account.address = address
    account.comments = comments
    account.created = created
    account.tags = tags

    db.session.commit()
    return account_schema.jsonify(account)

@app.route("/account/<id>", methods = ["DELETE"])
def account_delete(id):
    """
    DELETE request endpoint that deletes the account with a specified id
    Return: JSON of the account that was deleted
    """
    account = Accounts.query.get(id)
    db.session.delete(account)
    db.session.commit()

    return account_schema.jsonify(account)

if __name__ == '__main__':
    app.run(debug = True)
