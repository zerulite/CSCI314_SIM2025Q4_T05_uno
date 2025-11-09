from flask import *
from dateutil.parser import *

# PIN
from CreateReqCont import *
from ViewReqCont import *
from UpdateReqCont import *
from DeleteReqCont import *
from ViewAReqCont import *
from SearchReqCont import *
from ReqViewCountCont import *
from ReqShortlistCountCont import *
from ViewCompletedReqCont import *
from SearchCompletedReqCont import *
from GetCategoriesCont import *

# CSR
from CsrRepSearchNewCont import CSRSearchNewController
from CsrRepViewIndividualCont import CSRViewIndividualController
from CsrRepViewCont import CSRViewNewController
from CsrRepShortlistCont import CSRShortlistController
from CsrRepShortlistStatusCont import CSRShortlistStatusController
from CsrRepSearchShortlistCont import CSRSearchShortlistController
from CsrRepViewShortlistCont import CSRViewShortlistController
from CsrRepSearchHistoryCont import CSRSearchHistoryController
from CsrRepViewHistoryCont import CSRViewHistoryController
from datetime import datetime


# Main
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

csr_search_new_cont = CSRSearchNewController()
csr_view_individual_cont = CSRViewIndividualController()
csr_view_cont = CSRViewNewController()
csr_shortlist_cont = CSRShortlistController()
csr_shortlist_status_cont = CSRShortlistStatusController()
csr_search_shortlisted_cont = CSRSearchShortlistController()
csr_view_shortlist_cont = CSRViewShortlistController()
csr_history_cont = CSRSearchHistoryController()
csr_view_history_cont = CSRViewHistoryController()


@app.route('/')
def home():
    return render_template('login.html')

@app.route("/PIN/ViewCreateRequestPg", methods=['GET'])
def viewCreateReq():
    controller = GetCategoriesCont()
    categoryList = controller.getCategoriesCont()
    print(categoryList)

    return render_template("/PIN/createRequest.html", categoryList=categoryList)


@app.route("/PIN/ViewUpdateReqPg")
def viewUpdateReq():
    requestID = request.args.get('requestID', '').strip()
    reqStatus = request.args.get('reqStatus', '').strip()

    controller = GetCategoriesCont()
    categoryList = controller.getCategoriesCont()

    return render_template("/PIN/updateRequest.html",
                           requestID=requestID,
                           reqStatus=reqStatus,
                           categoryList=categoryList)

@app.route('/PIN/CreateReq', methods=['GET', 'POST'])
def createReq():
    controller = CreateReqCont()
    result = None

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    if request.method == 'POST':
        reqDescription = request.form.get('reqDescription', '').strip()
        helpNeededDate = request.form.get('helpNeededDate', '').strip()
        helpNeededTime = request.form.get('helpNeededTime', '').strip()
        category = request.form.get('category', '').strip()

        response = controller.createReqCont(reqDescription, helpNeededDate, helpNeededTime, category, userID)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            # Should not reach here since no data should be returned
            result = response["rows"]

    return render_template('/PIN/createRequestSuccess.html', result=result)

@app.route('/PIN/ViewReq', methods=['GET'])
def viewReq():
    controller = ViewReqCont()
    result = None
    
    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    response = controller.viewReqCont(userID)

    if response["type"] == "alert" or response["type"] == "error":
        # Receives a message (alert/error)
        result = response["message"]
    elif response["type"] == "data":
        result = response["rows"]

    return render_template('/PIN/viewRequest.html', results=result)

@app.route('/PIN/UpdateReq', methods=['GET', 'POST'])
def updateReq():
    controller = UpdateReqCont()
    result = None

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    if request.method == 'POST':
        requestID = request.form.get('requestID', '').strip()
        reqDescription = request.form.get('reqDescription', '').strip()
        helpNeededDate = request.form.get('helpNeededDate', '').strip()
        helpNeededTime = request.form.get('helpNeededTime', '').strip()
        reqStatus = request.form.get('reqStatus', '').strip()
        category = request.form.get('category', '').strip()

        print(requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, category)
        
        response = controller.updateReqCont(requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, category, userID)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            # Should not reach here since no data should be returned
            result = response["rows"]

    return render_template('/PIN/createRequestSuccess.html', result=result)

@app.route('/PIN/DeleteReq', methods=['GET', 'POST'])
def deleteReq():
    controller = DeleteReqCont()
    result = None

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    print("first")

    if request.method == 'POST':
        requestID = request.form.get('requestID', '').strip()
        print(requestID)

        response = controller.deleteReqCont(requestID, userID)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            # Should not reach here since no data should be returned
            result = response["rows"]
        
        print(result)

    return render_template('/PIN/deleteRequest.html', result=result)

@app.route('/PIN/ViewAReq', methods=['GET'])
def viewAReq():
    controller = ViewAReqCont()
    result = None
    requestID = request.args.get('requestID', '').strip()
    
    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    response = controller.viewAReqCont(requestID, userID)

    if response["type"] == "alert" or response["type"] == "error":
        # Receives a message (alert/error)
        result = response["message"]
    elif response["type"] == "data":
        result = response["rows"]

    return render_template('/PIN/viewARequest.html', result=result)

@app.route('/PIN/SearchReq', methods=['GET'])
def searchReq():
    controller = SearchReqCont()
    result = None

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    searchParams = {
        'requestID': request.args.get('requestID', '').strip(),
        'reqDescription': request.args.get('reqDescription', '').strip(),
        'helpNeededDate': request.args.get('helpNeededDate', '').strip(),
        'helpNeededTime': request.args.get('helpNeededTime', '').strip(),
        'category': request.args.get('category', '').strip(),
        'userID': userID
    }

    searchParams = {key: value for key, value in searchParams.items() if value}

    if searchParams:
        response = controller.searchReqCont(**searchParams)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            result = response["rows"]

    return render_template('/PIN/searchRequest.html', results=result, q=searchParams)

@app.route('/PIN/ReqViewCount', methods=['GET'])
def reqViewCount():
    controller = ReqViewCountCont()
    result = None

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    response = controller.reqViewCountCont(userID)

    if response["type"] == "alert" or response["type"] == "error":
        # Receives a message (alert/error)
        result = response["message"]
    elif response["type"] == "data":
        result = response["rows"]

    return render_template('/PIN/viewCount.html', result=result)

@app.route('/PIN/ReqShortlistCount', methods=['GET'])
def reqShortlistCount():
    controller = ReqShortlistCountCont()
    result = None

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    response = controller.reqShortlistCountCont(userID)

    if response["type"] == "alert" or response["type"] == "error":
        # Receives a message (alert/error)
        result = response["message"]
    elif response["type"] == "data":
        result = response["rows"]

    return render_template('/PIN/shortlistCount.html', result=result)

@app.route('/PIN/ViewCompletedReq', methods=['GET'])
def viewCompletedReq():
    controller = ViewCompletedReqCont()
    result = None

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    response = controller.viewCompletedReqCont(userID)

    if response["type"] == "alert" or response["type"] == "error":
        # Receives a message (alert/error)
        result = response["message"]
    elif response["type"] == "data":
        result = response["rows"]

    return render_template('/PIN/viewCompletedRequests.html', result=result)

@app.route('/PIN/SearchCompletedReq', methods=['GET'])
def searchCompletedReq():
    controller = SearchCompletedReqCont()
    result = None

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    searchParams = {
        'requestID': request.args.get('requestID', '').strip(),
        'reqDescription': request.args.get('reqDescription', '').strip(),
        'helpNeededDate': request.args.get('helpNeededDate', '').strip(),
        'helpNeededTime': request.args.get('helpNeededTime', '').strip(),
        'category': request.args.get('category', '').strip(),
        'userID': userID
    }

    searchParams = {key: value for key, value in searchParams.items() if value}

    if searchParams:
        response = controller.searchCompletedReqCont(**searchParams)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            result = response["rows"]

    return render_template('/PIN/searchCompletedRequest.html', results=result, q=searchParams)


def _parse_date(s):
    if not s:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    print("WARN: bad date format:", s)
    return None 

def _parse_time(s):
    if not s:
        return None
    for fmt in ("%I:%M %p", "%H:%M"):
        try:
            t = datetime.strptime(s.strip(), fmt).time()
            return t.strftime("%H:%M")
        except ValueError:
            pass
    print("WARN: bad time format:", s)
    return None

@app.route("/dev/login/<user_id>")
def dev_login(user_id):
    session["userID"] = user_id.strip()
    return redirect(url_for("home"))

@app.route("/dev/logout")
def dev_logout():
    session.pop("userID", None)
    flash("Logged out")
    return redirect(url_for("home"))

@app.route("/CSR/Home")
def csrhome():
    return render_template("/CSR/Csr_Home.html")

#Search New Request
@app.route("/CSR/Search", methods=["GET"])
def csrSearchNewRequests():
    args = request.args

    clicked = "Search" in args or len(args) > 0

    completed_raw = args.get("completed")
    if completed_raw in (None, "no_filter"):
        completed = None
    elif completed_raw == "empty":
        completed = ""  
    else:
        completed = completed_raw

    filters = dict(
        requestID=(args.get("requestID") or None),
        reqDescription=(args.get("request") if args.get("request") else None),
        volunteer=(args.get("volunteer") if args.get("volunteer") else None),
        helpNeededDate=_parse_date(args.get("date")),
        helpNeededTime=_parse_time(args.get("time")),
        category=(args.get("category") or None),
        userID=(args.get("userID") or None),
        completed=completed,
        limit=int(args.get("limit", 50)),
        offset=int(args.get("offset", 0)),
    )

    print("INPUT ARGS:", dict(args))
    print("FILTERS:", filters)

    results = csr_search_new_cont.searchNewRequests(**filters) if clicked else []
    return render_template("/CSR/Csr_Search.html", results=results, q=args)

#View Individual Request
@app.route("/CSR/Request/<request_id>", methods=["GET"])
def csrViewRequestIndividual(request_id):
    row = csr_view_individual_cont.viewIndividualRequest(request_id)
    if not row:
        from flask import flash, redirect, url_for
        flash("Request not found.")
        return redirect(url_for("csrListAllRequests"))
    return render_template("/CSR/Csr_View_Individual.html", row=row)

#View All Requests
@app.route("/CSR/Requests", methods=["GET"])
def csrListAllRequests():
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    rows = csr_view_cont.viewAllRequests(limit=limit, offset=offset)
    return render_template("/CSR/Csr_View.html", results=rows, limit=limit, offset=offset)

#Prompts if shortlisted success or already shortlisted
@app.route("/CSR/Shortlist/<request_id>", methods=["POST"])
def addToShortlistStatus(request_id):
    referer = request.headers.get("Referer")
    csr_user_id = session.get("userID")
    if not csr_user_id:
        flash("Please log in as CSR to shortlist.")
        return redirect(referer or url_for("home"))

    status = csr_shortlist_status_cont.addToShortlistStatus(request_id, csr_user_id)

    if status == "added":
        flash("Shortlisted successful.")
    elif status == "exists":
        flash("Already shortlisted.")
    else:
        flash("Shortlist failed. Please try again.")

    return redirect(referer or url_for("csrSearchShortlisted"))


#Shortlist
@app.route("/CSR/SearchShortlist", methods=["GET"])
def csrSearchShortlist():
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    rows = csr_view_cont.viewAllRequests(limit=limit, offset=offset)
    return render_template("/CSR/Csr_Save_Shortlisted.html", results=rows, limit=limit, offset=offset) 

#Search Shortlist
@app.route("/CSR/SearchShortlisted", methods=["GET"])
def csrSearchShortlisted():
    csr_user_id = session.get("userID")
    if not csr_user_id:
        flash("Please log in as CSR to view shortlisted.")
        return redirect(url_for("home"))

    args = request.args
    clicked = "Search" in args or len(args) > 0

    completed_raw = args.get("completed")
    if completed_raw in (None, "no_filter"):
        completed = None
    elif completed_raw == "empty":
        completed = ""
    else:
        completed = completed_raw

    filters = dict(
        requestID=(args.get("requestID") or None),
        request=(args.get("request") if args.get("request") is not None else None),
        volunteer=(args.get("volunteer") or None),
        date=_parse_date(args.get("date")),
        time=_parse_time(args.get("time")),
        category=(args.get("category") or None),
        userID=(args.get("userID") or None),
        completed=completed,
        limit=int(args.get("limit", 50)),
        offset=int(args.get("offset", 0)),
    )

    results = csr_search_shortlisted_cont.searchShortlisted(csr_user_id, **filters) if clicked else []
    return render_template("/CSR/Csr_Search_Shortlisted.html", results=results, q=args)

#View Shortlisted Requests
@app.route("/CSR/Shortlist/Requests", methods=["GET"])
def csrViewShortlistRequests():
    csr_user_id = session.get("userID")
    if not csr_user_id:
        flash("Please log in as CSR to view your shortlist.")
        return redirect(url_for("home"))
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    rows = csr_view_shortlist_cont.listShortlist(csr_user_id=csr_user_id, limit=limit, offset=offset)
    return render_template("/CSR/Csr_View_Shortlisted.html", results=rows, limit=limit, offset=offset)

#Search History
@app.route("/CSR/History", methods=["GET"])
def csrSearchHistory():
    args = request.args
    clicked = "Search" in args or len(args) > 0

    filters = dict(
        requestID=(args.get("requestID") or None),
        reqDescription=(args.get("request") if args.get("request") else None),
        volunteer=(args.get("volunteer") if args.get("volunteer") else None),
        helpNeededDate=_parse_date(args.get("date")),
        helpNeededTime=_parse_time(args.get("time")),
        category=(args.get("category") or None),
        userID=(args.get("userID") or None),
        limit=int(args.get("limit", 50)),
        offset=int(args.get("offset", 0)),
    )

    results = csr_history_cont.searchHistory(**filters) if clicked else []
    return render_template("/CSR/Csr_Search_History.html", results=results, q=args)

#View History
@app.route("/CSR/Requests/Completed", methods=["GET"])
def csrViewHistory():
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    rows = csr_view_history_cont.viewHistory(limit=limit, offset=offset)
    return render_template("/CSR/Csr_View_History.html", results=rows, limit=limit, offset=offset)



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
