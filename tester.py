x = "abcDEFhiJk"
y = ""

# print(y.isalpha())

# print(x)

# x = x.capitalize()

# print(x)

def test1():
    thislist = ["Alice", "Betty", "Cecil"]
    checker = False
    wordTest = "Ace"

    for name in thislist:
        if name == wordTest:
            checker = name
    
    return checker

def test2():
    x = test1()
    if x:
        print("TRUE")
    else:
        print("FALSE")

def test3():
    x = "Hello"
    if x:
        print("TRUE")
    else:
        print("FALSE")

def test4():
    thislist = ["Alice", "Betty", "Cecil", "Desmond"]
    thatlist = []
    thoselist = [("1", "Alice"), ("2", "Betty"), ("3", "Cecil")]

    print(len(thislist))
    print(len(thatlist))
    print(len(thoselist))

def test5():
    reqDescription = "desc"
    helpNeededDate = "dd"
    helpNeededTime = "ss"
    reqStatus = "Completed"
    category = ""

    updatesRaw = {"reqDescription": reqDescription, 
                   "helpNeededDate": helpNeededDate, 
                   "helpNeededTime": helpNeededTime, 
                   "reqStatus": reqStatus, 
                   "category": category}
    # updatesFiltered = {}
    # for key in updatesRaw:
    #     if len(updatesRaw.get(key)) != 0:
    #         updatesFiltered.update({f"{key}": updatesRaw.get(key)})

    updatesFiltered = {k: v for k, v in updatesRaw.items() if v != ""}

    print("--- Printing raw ---")
    for key in updatesRaw:
        print(f"{key} : {updatesRaw.get(key)}")
    print()
    print("--- Printing filtered ---")
    for key in updatesFiltered:
        print(f"{key} : {updatesFiltered.get(key)}")

    setClause = ", ".join([f"{k} = %s" for k in updatesFiltered])
    print(setClause)

def test6():
    xDict = {}
    yDict = {"1": "Alice", "2": "Betty", "3": "Cecil"}

    print(len(xDict))
    print(len(yDict))

test5()