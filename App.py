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


app = Flask(__name__)

app.secret_key = "change-me"
csr_search_new_cont = CSRSearchNewController()
csr_view_individual_cont = CSRViewIndividualController()
csr_view_cont = CSRViewNewController()
csr_shortlist_cont = CSRShortlistController()
csr_shortlist_status_cont = CSRShortlistStatusController()
csr_search_shortlisted_cont = CSRSearchShortlistController()
csr_view_shortlist_cont = CSRViewShortlistController()
csr_history_cont = CSRSearchHistoryController()
csr_view_history_cont = CSRViewHistoryController()

userID = "U001"

@app.route("/")
def home():
    return render_template("/PIN/home.html")

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

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

# Main
if __name__ == '__main__':
    app.run()
