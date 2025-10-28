from flask import *
from CreateUserAcctCont import *
from UpdateUserAcctCont import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def userLogin():
    userID = request.form["userID"]
    password = request.form["password"]

#Goes to View user list
@app.route("/ViewUsers")
def ViewUsers():
    return render_template("users.html")

#Goes to Create user pg
@app.route("/RegisterUsers")
def RegisterUsers():
    return render_template("register.html")

#Goes to update user pg
@app.route("/UpdateUsers")
def UpdateUsers():
    return render_template("updateUser.html")

#UserCreateAcct
@app.route("/createAccountPage")
def CreateAccountPage():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def createAcct():
    message = None
    userID = request.form['userID']
    password = request.form['password']
    name = request.form['name']
    email = request.form['email']
    profile = request.form['profile']
    userState = request.form['userState']

    controller = CreateUserAccount()
    response = controller.createUserAccount(userID, password, name, email, profile, userState)
    message = response["message"]

    return render_template('register.html', message=message)

@app.route('/update', methods=['POST'])
def updateAcct():
    message = None
    userID = request.form['userID']
    password = request.form['password']
    name = request.form['name']
    email = request.form['email']
    profile = request.form['profile']
    userState = request.form['userState']

    response = UpdateUserAccount.updateUserAccount(userID, password, name, email, profile, userState)
    message = response["message"]

    return render_template('updateUser.html', message=message)

#Main
if __name__ == '__main__':
    app.run()
