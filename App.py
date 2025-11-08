from flask import *
from dateutil.parser import *

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

app = Flask(__name__)

userID = "U001"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/ViewCreateRequestPg", methods=['GET'])
def viewCreateReq():
    controller = GetCategoriesCont()
    categoryList = controller.getCategoriesCont()
    print(categoryList)

    return render_template("createRequest.html", categoryList=categoryList)


@app.route("/ViewUpdateReqPg")
def viewUpdateReq():
    requestID = request.args.get('requestID', '').strip()
    reqStatus = request.args.get('reqStatus', '').strip()

    controller = GetCategoriesCont()
    categoryList = controller.getCategoriesCont()

    return render_template("updateRequest.html",
                           requestID=requestID,
                           reqStatus=reqStatus,
                           categoryList=categoryList)

@app.route('/CreateReq', methods=['GET', 'POST'])
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

    return render_template('createRequestSuccess.html', result=result)

@app.route('/ViewReq', methods=['GET'])
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

    return render_template('viewRequest.html', results=result)

@app.route('/UpdateReq', methods=['GET', 'POST'])
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

    return render_template('createRequestSuccess.html', result=result)

@app.route('/DeleteReq', methods=['GET', 'POST'])
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

    return render_template('deleteRequest.html', result=result)

@app.route('/ViewAReq', methods=['GET'])
def viewAReq():
    controller = ViewAReqCont()
    result = None
    requestID = request.args.get('requestID', '').strip()

    
    # Get userID from session
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

    # requestID should be received when html button is pressed by user
    response = controller.viewAReqCont(requestID, userID)

    if response["type"] == "alert" or response["type"] == "error":
        # Receives a message (alert/error)
        result = response["message"]
    elif response["type"] == "data":
        result = response["rows"]

    return render_template('viewARequest.html', result=result)

@app.route('/SearchReq', methods=['GET', 'POST'])
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

    return render_template('searchRequest.html', results=result, q=searchParams)

@app.route('/ReqViewCount', methods=['GET'])
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

    return render_template('viewCount.html', result=result)

@app.route('/ReqShortlistCount', methods=['GET'])
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

    return render_template('shortlistCount.html', result=result)

@app.route('/ViewCompletedReq', methods=['GET'])
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

    return render_template('viewCompletedRequests.html', result=result)

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

    return render_template('searchRequest.html', results=result, q=searchParams)

# @app.route('/SearchCompletedReq', methods=['GET', 'POST'])
# def searchCompletedReq():
#     controller = SearchCompletedReqCont()
#     result = None

#     # Get userID from session
#     # userID = session.get('userID')
#     # if not userID:
#     #     return redirect(url_for('login'))

#     if request.method == 'POST':
#         requestID = request.form.get('requestID', '').strip()

#         response = controller.searchCompletedReqCont(requestID, userID)

#         if response["type"] == "alert" or response["type"] == "error":
#             # Receives a message (alert/error)
#             result = response["message"]
#         elif response["type"] == "data":
#             result = response["rows"]

#     return render_template('searchCompletedRequest.html', result=result)

#Main
if __name__ == '__main__':
    app.run()
