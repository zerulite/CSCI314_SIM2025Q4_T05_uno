from flask import *
from LoginCont import *
from CreateUserAcctCont import *
from UpdateUserAcctCont import *
from ViewUserAcctCont import *
from ListUserAcctCont import *
from SearchUserAcctCont import *
from SuspendUserAccountCont import *
from CreateUserProfileCont import *
from ViewUserProfileCont import *
from ListUserProfileCont import *
from UpdateUserProfileCont import *
from SuspendUserProfileCont import *
from SearchUserProfileCont import *
from CreateCategoryCont import *
from ViewCategoryCont import *
from ListCategoryCont import *
from UpdateCategoryCont import *
from DeleteCategoryCont import *
from SearchCategoryCont import *
from GenerateDailyReportCont import *
from GenerateWeeklyReportCont import *
from GenerateMonthlyReportCont import *

app = Flask(__name__)
app.secret_key = "Spt2!31oon"

@app.route('/')
def home():
    return render_template('login.html')

#Login pg
@app.route('/login', methods=['GET', 'POST'])
def userLogin():
    controller = Login()

    if request.method == 'POST':
        userID = request.form['userID']
        password = request.form['password']
        
        result = controller.login_user(userID, password)

        if result["success"]:
            user = result["user"]
            session['userID'] = user["userID"]
            session['profile'] = user["profile"]
            flash(result["message"], "success")

            if user["profile"] == "CSR Representative":
                return redirect(url_for('csr_main'))
            elif user["profile"] == "Platform Management":
                return redirect(url_for('PM_main'))
            elif user["profile"] == "User Admin":
                return redirect(url_for('admin_main'))
            elif user["profile"] == "Person In Need":
                return redirect(url_for('PIN_main'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash(result["message"], "danger")
    
    return render_template('login.html')


#Logout
@app.route('/logout')
def userLogout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('userLogin'))

@app.route('/csr_main')
def csr_main():
    # Optional: check session/profile
    if 'profile' not in session or session['profile'] != "CSR Representative":
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    return render_template('csr_main.html')


@app.route('/PM_main')
def PM_main():
    if 'profile' not in session or session['profile'] != "Platform Management":
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    return render_template('PM_main.html')


@app.route('/admin_main')
def admin_main():
    if 'profile' not in session or session['profile'] != "User Admin":
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    return render_template('admin_main.html')


@app.route('/PIN_main')
def PIN_main():
    if 'profile' not in session or session['profile'] != "Person In Need":
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    return render_template('PIN_main.html')

#Create User Account
@app.route('/createUserAcct', methods=['GET', 'POST'])
def createUserAcct():
    controller = CreateUserAccount()
    message = None
    if request.method == 'POST':

        userID = request.form['userID']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        profile = request.form['profile']
        userState = request.form['userState']

        response = controller.createUserAccount(userID, password, name, email, profile, userState)
        message = response["message"]

    return render_template('createUserAcct.html', message=message)

#View User Account details
@app.route('/viewUserAcct', methods=['GET', 'POST'])
def viewUserAcct():
    controller = ViewUserAccount()

    if request.method == 'POST':
        user_id = request.form['userID']
        user_data = controller.view_user_account(user_id)
    return render_template("viewUserAcct.html", user=user_data)

#List of all User Account
@app.route('/listUsers')
def listUsers():
    controller = ListUserAccount()
    users_data = controller.list_acct()  # This returns the list of users
    return render_template("listUsers.html", users=users_data)

#Update User Account
@app.route('/UpdateUserAcct/<userID>', methods=['GET', 'POST'])
def updateAcct(userID):
    controller = UpdateUserAccount()
    message = None

    if request.method == 'POST':
        # Handle form submission to update user
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        profile = request.form['profile']
        userState = request.form['userState']

        response = controller.updateUserAccount(userID, password, name, email, profile, userState)
        message = response.get("message", "Update failed")

    # Fetch user details to pre-fill the form
    user = controller.getUserByID(userID)

    return render_template('updateUserAcct.html', user=user, message=message)


#Suspend User Account
@app.route('/suspendUserAcct/<userID>', methods=['GET', 'POST'])
def suspendAcct(userID):
    controller = SuspendUserAccount()
    message = None

    if request.method == 'POST':
        # Handle form submission to update user
        userState = request.form['userState']

        response = controller.suspendUserAccount(userID, userState)
        message = response.get("message", "Update failed")

    # Fetch user details to pre-fill the form
    user = controller.getUserByID(userID)

    return render_template('suspendUserAcct.html', user=user, message=message)

#Search User Account
@app.route('/SearchUserAcct', methods=['GET', 'POST'])
def searchUsers():
    users = []
    if request.method == "POST":
        search_fields = {
            "userID": request.form.get("userID"),
            "password": request.form.get("password"),
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "profile": request.form.get("profile"),
            "userState": request.form.get("userState")
        }
        controller = SearchUserAccount()
        users = controller.search_users(search_fields)
    return render_template("searchUserAcct.html", users=users)

#Create User Profile
@app.route('/createUserProfile', methods=['GET', 'POST'])
def createProfile():
    controller = CreateUserProfile()
    message = None
    if request.method == 'POST':

        profile = request.form['profile']
        description = request.form['description']
        profileState = request.form['profileState']

        response = controller.createUserProfile(profile, description, profileState)
        message = response["message"]

    return render_template('createUserProfile.html', message=message)

#View User Profile
@app.route('/viewUserProfile', methods=['GET', 'POST'])
def viewProfile():
    controller = ViewUserProfile()

    if request.method == 'POST':
        profile = request.form.get('profile')
        profile_data = controller.view_user_profile(profile)
    return render_template("viewUserProfile.html", profile=profile_data)

#List of all User Profile
@app.route('/listProfile')
def listProfiles():
    controller = ListUserProfile()
    profile_data = controller.list_profile() 
    return render_template("listProfiles.html", profiles=profile_data)

#Update User Profile
@app.route('/updateUserProfile/<profile>', methods=['GET', 'POST'])
def updateProfile(profile):
    controller = UpdateUserProfile()
    message = None

    if request.method == 'POST':
        # Handle form submission to update user
        profile = request.form['profile']
        description = request.form['description']
        profileState = request.form['profileState']

        response = controller.updateUserProfile(profile, description, profileState)
        message = response.get("message", "Update failed")

    # Fetch user details to pre-fill the form
    profile_data = controller.getProfile(profile)

    return render_template('updateUserProfile.html', profile=profile_data, message=message)


#Suspend User Profile
@app.route('/suspendUserProfile/<profile>', methods=['GET', 'POST'])
def suspendProfile(profile):
    controller = SuspendUserProfile()
    message = None

    if request.method == 'POST':
        # Handle form submission to update user
        profileState = request.form['profileState']

        response = controller.suspendUserProfile(profile, profileState)
        message = response.get("message", "Update failed")

    # Fetch user details to pre-fill the form
    profile_data = controller.getProfile(profile)

    return render_template('suspendUserProfile.html', profile=profile_data, message=message)

#Search User Profile
@app.route('/searchUserProfile', methods=['GET', 'POST'])
def searchProfile():
    profiles_data = []
    if request.method == "POST":
        search_fields = {
            "profile": request.form.get("profile"),
            "description": request.form.get("description"),
            "profileState": request.form.get("profileState")
        }
        controller = SearchUserProfile()
        profiles_data = controller.search_profiles(search_fields)
    return render_template("searchUserProfile.html", profiles=profiles_data)


#Platform Management

#Create Categories
@app.route('/createCategory', methods=['GET', 'POST'])
def createCategory():
    controller = CreateCategory()
    message = None
    if request.method == 'POST':

        category = request.form['category']
        description = request.form['description']

        response = controller.create_category(category, description)
        message = response["message"]

    return render_template('createCategory.html', message=message)
#View Categories
@app.route('/viewCategories', methods=['GET', 'POST'])
def viewCategory():
    controller = ViewCategory()

    if request.method == 'POST':
        category = request.form.get('category')
        category_data = controller.view_category(category)
    return render_template("viewCategory.html", category=category_data)

#List of all User Profile
@app.route('/listCategories')
def listCategory():
    controller = ListCategory()
    categories = controller.list_category()
    return render_template("listCategories.html", categories=categories)

#Update Categories
@app.route('/updateCategory/<category>', methods=['GET', 'POST'])
def updateCategory(category):
    controller = UpdateCategory()
    message = None

    if request.method == 'POST':
        # Handle form submission to update user
        profile = request.form['category']
        description = request.form['description']

        response = controller.update_category(category, description)
        message = response.get("message", "Update failed")

    # Fetch user details to pre-fill the form
    category_data = controller.get_category(category)

    return render_template('updateCategory.html', category=category_data, message=message)

#Delete Categories
@app.route('/deleteCategory', methods=['POST'])
def deleteCategory():
    controller = DeleteCategory()
    category = request.args.get('category') or request.form.get('category')
    response = controller.delete_category(category)

    if response["success"]:
        flash(response["message"], "success")
    else:
        flash(response["message"], "error")

    return redirect(url_for('listCategory'))

#Search Categories
@app.route('/searchCategory', methods=['GET', 'POST'])
def searchCategory():
    categories_data = []
    if request.method == "POST":
        search_fields = {
            "category": request.form.get("category"),
            "description": request.form.get("description")
        }
        controller = SearchCategory()
        categories_data = controller.search_category(search_fields)
    return render_template("searchCategory.html", categories=categories_data)

#Generate Daily Reports
@app.route('/dailyReport', methods=['GET', 'POST'])
def daily_report():
    report_data = []
    controller = GenerateDailyReport()
    if request.method == 'POST':
        date = request.form['date']
        report_data = controller.generate_daily_report(date)
    return render_template('dailyReport.html', report=report_data)

#Generate Weekly Reports
@app.route('/weeklyReport', methods=['GET', 'POST'])
def weekly_report():
    report_data = []
    controller = GenerateWeeklyReport()
    if request.method == 'POST':
        week_start = request.form['week_start']  # YYYY-MM-DD (Monday)
        report_data = controller.generate_weekly_report(week_start)
    return render_template('weeklyReport.html', report=report_data)

#Generate Monthly Reports
@app.route('/monthlyReport', methods=['GET', 'POST'])
def monthly_report():
    report_data = []
    controller = GenerateMonthlyReport()
    if request.method == 'POST':
        date = request.form['date']
        report_data = controller.generate_monthly_report(date)
    return render_template('monthlyReport.html', report=report_data)


#Main
if __name__ == '__main__':
    app.run()
