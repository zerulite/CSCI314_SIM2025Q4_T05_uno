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
                return redirect(url_for('CSRMain'))
            elif user["profile"] == "Platform Management":
                return redirect(url_for('PMHome'))
            elif user["profile"] == "User Admin":
                return redirect(url_for('adminHome'))
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
def CSRMain():
    # Optional: check session/profile
    if 'profile' not in session or session['profile'] != "CSR Representative":
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    return render_template('csr_main.html')


@app.route('/PMHome')
def PMHome():
    if 'profile' not in session or session['profile'] != "Platform Management":
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    return render_template('/PlatformManagement/PMHome.html')


@app.route('/adminHome')
def adminHome():
    if 'profile' not in session or session['profile'] != "User Admin":
        flash("Access denied.", "danger")
        return redirect(url_for('login'))
    return render_template('/UserAdmin/adminHome.html')


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

    return render_template('/UserAdmin/createUserAcct.html', message=message)

# View User Account details (supports GET and POST)
@app.route('/viewUserAcct', methods=['POST'])
@app.route('/viewUserAcct/<userID>', methods=['GET'])
def viewUserAcct(userID=None):
    # If POST, get userID from the hidden form field
    if request.method == 'POST':
        userID = request.form.get('userID')

    if not userID:
        flash("No user selected.")
        return redirect(url_for('/UserAdmin/listUsers'))

    controller = ViewUserAccount()
    user_data = controller.viewUserAccount(userID)

    if not user_data:
        flash("User not found.")
        return redirect(url_for('listUsers'))

    return render_template("/UserAdmin/viewUserAcct.html", user=user_data)


#List of all User Account
@app.route('/listUsers')
def listUsers():
    controller = ListUserAccount()
    users_data = controller.listAcct()  # This returns the list of users
    return render_template("/UserAdmin/listUsers.html", users=users_data)

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

    return render_template('/UserAdmin/updateUserAcct.html', user=user, message=message)


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

    return render_template('/UserAdmin/suspendUserAcct.html', user=user, message=message)

# Search User Account
@app.route('/SearchUserAcct', methods=['GET', 'POST'])
def searchUsers():
    # Initialize empty defaults
    users = []
    form_data = {
        "userID": "",
        "password": "",
        "name": "",
        "email": "",
        "profile": "",
        "userState": ""
    }

    if request.method == "POST":
        # Get form values
        for key in form_data.keys():
            form_data[key] = request.form.get(key, "")

        # Perform search
        controller = SearchUserAccount()
        users = controller.searchUsers(form_data)

    # Pass users and form_data to template
    return render_template("/UserAdmin/searchUserAcct.html",users=users,**form_data)


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

    return render_template('/UserAdmin/createUserProfile.html', message=message)

# View User Profile
@app.route('/viewUserProfile', methods=['GET', 'POST'])
def viewProfile():
    controller = ViewUserProfile()
    profile_data = None
    profile = request.args.get('profile') or request.form.get('profile')

    if profile:
        profile_data = controller.viewUserProfile(profile)
        if not profile_data:
            flash("Profile not found.")

    return render_template("/UserAdmin/viewUserProfile.html", profile=profile_data)

#List of all User Profile
@app.route('/listProfile')
def listProfiles():
    controller = ListUserProfile()
    profile_data = controller.listProfile() 
    return render_template("/UserAdmin/listProfiles.html", profiles=profile_data)

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

    return render_template('/UserAdmin/updateUserProfile.html', profile=profile_data, message=message)


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

    return render_template('/UserAdmin/suspendUserProfile.html', profile=profile_data, message=message)

# Search User Profile
@app.route('/searchUserProfile', methods=['GET', 'POST'])
def searchProfile():
    profiles_data = []
    form_data = {
        "profile": "",
        "description": "",
        "profileState": ""
    }

    if request.method == "POST":
        # Get form values and retain them
        for key in form_data.keys():
            form_data[key] = request.form.get(key, "")

        # Perform search
        controller = SearchUserProfile()
        profiles_data = controller.searchProfile(form_data)

    return render_template(
        "searchUserProfile.html",
        profiles=profiles_data,
        **form_data
    )


#Platform Management

#Create Categories
@app.route('/createCategory', methods=['GET', 'POST'])
def createCategory():
    controller = CreateCategory()
    message = None
    if request.method == 'POST':

        category = request.form['category']
        description = request.form['description']

        response = controller.createCategory(category, description)
        message = response["message"]

    return render_template('/PlatformManagement/createCategory.html', message=message)

# View Categories
@app.route('/viewCategories', methods=['GET', 'POST'])
def viewCategory():
    controller = ViewCategory()
    category_data = None

    # Get category from POST or GET
    category = request.form.get('category') or request.args.get('category')
    if category:
        category_data = controller.viewCategory(category)

    return render_template("/PlatformManagement/viewCategory.html", category=category_data)



#List of all User Profile
@app.route('/listCategories')
def listCategory():
    controller = ListCategory()
    categories = controller.listCategory()
    return render_template("/PlatformManagement/listCategories.html", categories=categories)

#Update Categories
@app.route('/updateCategory/<category>', methods=['GET', 'POST'])
def updateCategory(category):
    controller = UpdateCategory()
    message = None

    if request.method == 'POST':
        # Handle form submission to update user
        category = request.form['category']
        description = request.form['description']

        response = controller.updateCategory(category, description)
        message = response.get("message", "Update failed")

    # Fetch user details to pre-fill the form
    category_data = controller.getCategory(category)

    return render_template('/PlatformManagement/updateCategory.html', category=category_data, message=message)

#Delete Categories
@app.route('/deleteCategory', methods=['POST'])
def deleteCategory():
    controller = DeleteCategory()
    category = request.args.get('category') or request.form.get('category')
    response = controller.deleteCategory(category)

    if response["success"]:
        flash(response["message"], "success")
    else:
        flash(response["message"], "error")

    return redirect(url_for('/PlatformManagement/listCategory'))

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
        categories_data = controller.searchCategory(search_fields)
    return render_template("/PlatformManagement/searchCategory.html", categories=categories_data)

#Generate Daily Reports
@app.route('/dailyReport', methods=['GET', 'POST'])
def dailyReport():
    report_data = []
    controller = GenerateDailyReport()
    if request.method == 'POST':
        date = request.form['date']
        report_data = controller.generateDailyReport(date)
    return render_template('/PlatformManagement/dailyReport.html', report=report_data)

#Generate Weekly Reports
@app.route('/weeklyReport', methods=['GET', 'POST'])
def weeklyReport():
    report_data = []
    controller = GenerateWeeklyReport()
    if request.method == 'POST':
        week_start = request.form['week_start']  # YYYY-MM-DD (Monday)
        report_data = controller.generateWeeklyReport(week_start)
    return render_template('/PlatformManagement/weeklyReport.html', report=report_data)

#Generate Monthly Reports
@app.route('/monthlyReport', methods=['GET', 'POST'])
def monthlyReport():
    report_data = []
    controller = GenerateMonthlyReport()
    if request.method == 'POST':
        date = request.form['date']
        report_data = controller.generateMonthlyReport(date)
    return render_template('/PlatformManagement/monthlyReport.html', report=report_data)


#Main
if __name__ == '__main__':
    app.run()
