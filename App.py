from flask import *

from CreateReqCont import *
from ViewReqCont import *
from UpdateReqCont import *
from DeleteReqCont import *
from SearchReqCont import *
from ReqViewCountCont import *
from ReqShortlistCountCont import *
from ViewCompletedReqCont import *
from SearchCompletedReqCont import *

app = Flask(__name__)

userID = "U001"

@app.route("/main")
def home():
    return render_template("helloworld.html")

@app.route("/ViewCreateRequestPg")
def viewCreateReq():
    return render_template("createRequest.html")

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
        
        response = controller.updateReqCont(requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, category, userID)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            # Should not reach here since no data should be returned
            result = response["rows"]

    return render_template('updateRequest.html', result=result)

@app.route('/DeleteReq', methods=['GET', 'POST'])
def deleteReq():
    controller = DeleteReqCont()
    result = None

    # Get userID from session
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

    if request.method == 'POST':
        requestID = request.form.get('requestID', '').strip()

        response = controller.deleteReqCont(requestID, userID)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            # Should not reach here since no data should be returned
            result = response["rows"]

    return render_template('deleteRequest.html', result=result)

@app.route('/SearchReq', methods=['GET', 'POST'])
def searchReq():
    controller = SearchReqCont()
    result = None

    # Get userID from session
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

    if request.method == 'POST':
        requestID = request.form.get('requestID', '').strip()

        response = controller.searchReqCont(requestID, userID)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            result = response["rows"]

    return render_template('searchRequest.html', result=result)

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

@app.route('/SearchCompletedReq', methods=['GET', 'POST'])
def searchCompletedReq():
    controller = SearchCompletedReqCont()
    result = None

    # Get userID from session
    # userID = session.get('userID')
    # if not userID:
    #     return redirect(url_for('login'))

    if request.method == 'POST':
        requestID = request.form.get('requestID', '').strip()

        response = controller.searchCompletedReqCont(requestID, userID)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            result = response["message"]
        elif response["type"] == "data":
            result = response["rows"]

    return render_template('searchCompletedRequest.html', result=result)

#Main
if __name__ == '__main__':
    app.run()
