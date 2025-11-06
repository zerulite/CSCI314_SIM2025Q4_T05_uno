from Request import Database, Request

# Adds 3 valid rows into Request table
def testCreate():
    db = Database()
    request_entity= Request(db)

    # result = request_entity.createReq(reqDescription, helpNeededDate, helpNeededTime, category, userID)
    result = request_entity.createReq("Need help moving furniture", "2025-11-15", "14:30", "Financial", "U001")
    resultPrint(result)

    result = request_entity.createReq("Looking for tutoring help", "2025-11-16", "10:00", "Academic", "U001")
    resultPrint(result)

    result = request_entity.createReq("Need groceries delivered", "2025-11-17", "09:00", "Errand", "U001")
    resultPrint(result)

    db.close()

# Negative test - tests if alerts are returned when erroneous input/data is entered by user
def testCreateNeg():
    db = Database()
    request_entity = Request(db)

    result = request_entity.createReq("Negative test 1", "32/11/2025", "14:30", "NegTest", "U001")
    resultPrint(result)

    result = request_entity.createReq("Negative test 2", "30/11/2025", "25:30", "NegTest", "U001")
    resultPrint(result)

    result = request_entity.createReq("", "30/11/2025", "14:30", "NegTest", "U001")
    resultPrint(result)

    db.close()

# Receives the 3 valid rows made by testCreate()
def testView():
    db = Database()
    request_entity = Request(db)

    result = request_entity.viewReq("U001")
    resultPrint(result)

    db.close()

# Negative test - tests if alert is returned when user has no requests
def testViewNeg():
    db = Database()
    request_entity = Request(db)

    result = request_entity.viewReq("U002")
    resultPrint(result)

    db.close()

# Receives row according to requestID, userID
def testSearch():
    db = Database()
    request_entity = Request(db)

    result = request_entity.searchReq("1", "U001")
    resultPrint(result)

    db.close()

# Negative test - tests if alert is returned when erroneous inputs are entered by user
def testSearchNeg():
    db = Database()
    request_entity = Request(db)

    result = request_entity.searchReq("", "U001")
    resultPrint(result)

    result = request_entity.searchReq("a", "U001")
    resultPrint(result)

    result = request_entity.searchReq("100", "U001")
    resultPrint(result)

    db.close()

# Updates row(s) accordingly
def testUpdate():
    db = Database()
    request_entity = Request(db)

    # updateReq(requestID, reqDescription, helpNeededDate, helpNeededTime, reqStatus, category, userID)

    # Update test with blank inputs
    result = request_entity.updateReq("1", "", "11/11/2026", "", "", "", "U001")
    resultPrint(result)

    # Prints to check updated row
    result = request_entity.searchReq("1", "U001")
    resultPrint(result)

    # Changes back to original
    result = request_entity.updateReq("1", "", "15/11/2025", "", "", "", "U001")

    # Prints to check row has been reverted
    result = request_entity.searchReq("1", "U001")
    resultPrint(result)

    db.close()

# Negative test - tests if alert is returned when errorneous inputs are entered by user
def testUpdateNeg():
    db = Database()
    request_entity = Request(db)

    # Nothing to update - requestID still needed
    result = request_entity.updateReq("1", "", "", "", "", "", "U001")
    resultPrint(result)

    # Negative test - Non-existing requestID
    result = request_entity.updateReq("100", "Negative test", "", "", "", "", "U001")
    resultPrint(result)

    # Negative test - Errorneous date
    result = request_entity.updateReq("1", "Negative test", "32/11/2025", "", "", "", "U001")
    resultPrint(result)

    # Negative test - Errorneous time
    result = request_entity.updateReq("1", "Negative test", "", "25:30", "", "", "U001")
    resultPrint(result)

    # Negative test - Non-existing status
    # Negative test - Non-existing category

    db.close()

# !!! Not running this as the PK will change !!!
def testDelete():
    db = Database()
    request_entity = Request(db)

    # Adds a new row to test deletion
    result = request_entity.createReq("To test deleteReq", "15/11/2025", "14:30", "Financial", "U001")
    resultPrint(result)

    result = request_entity.deleteReq("4", "U001")
    resultPrint(result)

    db.close()

# Negative test - tests if alert is returned when errorneous inputs are entered by user
def testDeleteNeg():
    db = Database()
    request_entity = Request(db)

    result = request_entity.deleteReq("", "U001")
    resultPrint(result)

    result = request_entity.deleteReq("a", "U001")
    resultPrint(result)

    result = request_entity.deleteReq("100", "U001")
    resultPrint(result)

    db.close()

# Receives requestID, viewCount associated with this userID
def testViewCount():
    db = Database()
    request_entity = Request(db)

    result = request_entity.reqViewCount("U001")
    resultPrint(result)

    db.close()

# Negative test - tests if alert is returned when user has no requests
def testViewCountNeg():
    db = Database()
    request_entity = Request(db)

    result = request_entity.reqViewCount("U002")
    resultPrint(result)

    db.close()

# Receives requestID, shortlistCount associated with this userID
def testShortlistCount():
    db = Database()
    request_entity = Request(db)

    result = request_entity.reqShortlistCount("U001")
    resultPrint(result)

    db.close()

# Negative test - tests if alert is returned when user has no requests
def testShortlistCountNeg():
    db = Database()
    request_entity = Request(db)

    result = request_entity.reqShortlistCount("U002")
    resultPrint(result)

    db.close()

# Receives userID's request(s) WHERE reqStatus = 'Completed'
def testViewCompReq():
    db = Database()
    request_entity = Request(db)

    result = request_entity.viewCompletedReq("U001")
    resultPrint(result)
    
    db.close()

# Negative test - tests if alert is returned when user has no 'Completed' requests
def testViewCompReqNeg():
    db = Database()
    request_entity = Request(db)

    result = request_entity.viewCompletedReq("U002")
    resultPrint(result)

    db.close()

# Receives 'Completed' requests according to requestID, userID
def testSearchCompReq():
    db = Database()
    request_entity = Request(db)

    result = request_entity.searchCompletedReq("1", "U001")
    resultPrint(result)

    db.close()

def testSearchCompReqNeg():
    db = Database()
    request_entity = Request(db)

    result = request_entity.searchCompletedReq("", "U001")
    resultPrint(result)

    result = request_entity.searchCompletedReq("a", "U001")
    resultPrint(result)

    result = request_entity.searchCompletedReq("3", "U001")
    resultPrint(result)

    result = request_entity.searchCompletedReq("100", "U001")
    resultPrint(result)

    db.close()

def testIncViewCount():
    db = Database()
    request_entity = Request(db)

    request_entity.incViewCount("1", "U001")

    result = request_entity.searchReq("1", "U001")
    resultPrint(result)

    db.close()

def testIncShortlistCount():
    db = Database()
    request_entity = Request(db)

    request_entity.incShortlistCount("1", "U001")

    result = request_entity.searchReq("1", "U001")
    resultPrint(result)

    db.close()

def testIsCatValid():
    db = Database()
    request_entity = Request(db)

    result = request_entity.isCategoryValid("Academic")
    print(result)

    db.close()

# def testTemplate():
#     db = Database()
#     request_entity = Request(db)

#     result = request_entity.createReq()
#     resultPrint(result)

#     db.close()


def resultPrint(result):
    if isinstance(result, dict):
        print(result.get("message"))
    elif isinstance(result, list):
        for item in result:
            print(item)
    else:
        # General bug catch-all (should not be possible but just in case)
        print("BUG!! ERROR!!")

def main():
    testCreate()
    # testCreateNeg()

    # testView()
    # testViewNeg()

    # testSearch()
    # testSearchNeg()

    # testUpdate()
    # testUpdateNeg()

    # testDeleteNeg()

    # testViewCount()
    # testViewCountNeg()

    # testShortlistCount()
    # testShortlistCountNeg()

    # testViewCompReq()
    # testViewCompReqNeg()

    # testSearchCompReq()
    # testSearchCompReqNeg()

    # testIncViewCount()
    # testIncShortlistCount()

    # testIsCatValid()

    pass

if __name__ == "__main__":
    main()