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

@app.route('/CreateRequest', methods=['GET', 'POST'])
def createRequest():
    controller = CreateReqCont()

    # Get userID from session
    userID = session.get('userID')
    if not userID:
        return redirect(url_for('login'))

    alertMsg = None

    if request.method == 'POST':
        reqDescription = request.form.get('reqDescription', '').strip()
        helpNeededDate = request.form.get('helpNeededDate', '').strip()
        helpNeededTime = request.form.get('helpNeededTime', '').strip()
        category = request.form.get('category', '').strip()

        response = controller.createReqCont(reqDescription, helpNeededDate, helpNeededTime, category, userID)

        if response["type"] == "alert" or response["type"] == "error":
            # Receives a message (alert/error)
            alertMsg = response["message"]
        else:
            # Should not reach here since no data should be returned
            alertMsg = response["rows"]

    return render_template('createRequest.html', alertMsg=alertMsg)