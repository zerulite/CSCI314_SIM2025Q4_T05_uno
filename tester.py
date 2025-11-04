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
    themlist = [("1", "Alice")]

    print(len(thislist))
    print(len(thatlist))
    print(len(thoselist))
    print(len(themlist))

    if thatlist:
        print("TRUE so > 0")
    if not thatlist:
        print("FALSE so < 0")

    if themlist:
        print("TRUE so > 0")
    if not themlist:
        print("FALSE so < 0")

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

def test7():
    
    x = 12
    y = "02"
    z = "12"

    print(type(x))
    print(type(y))
    print(type(z))

    print(type(int(y)))
    print(type(int(z)))

    print(int(y))
    print(int(z))

    # print(x.isdigit())
    print(y.isdigit())
    print(z.isdigit())

    print(len(x))
    print(len(y))

def test8():
    x = 0

    if x:
        print("TRUE!")
    else:
        print("FALSE!")

test4()