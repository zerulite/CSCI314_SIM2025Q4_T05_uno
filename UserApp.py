from flask import Flask, render_template, redirect, request, url_for, flash, session
from CsrRepSearchNewCont import CSRSearchNewController
from CsrRepViewCont import CSRViewNewController
from CsrRepShortlistCont import CSRShortlistController
from CsrRepSearchShortlistCont import CSRSearchShortlistController
from CsrRepViewShortlistCont import CSRViewShortlistController
from CsrRepSearchHistoryCont import CSRSearchHistoryController
from CsrRepViewHistoryCont import CSRViewHistoryController
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-me"
csr_cont = CSRSearchNewController()
csr_view_cont = CSRViewNewController()
shortlist_cont = CSRShortlistController()
search_shortlisted_cont = CSRSearchShortlistController()
view_shortlist_cont = CSRViewShortlistController()
history_cont = CSRSearchHistoryController()
view_history = CSRViewHistoryController()

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
    for fmt in ("%I:%M %p", "%H:%M:%S", "%H:%M"):
        try:
            t = datetime.strptime(s.strip(), fmt).time()
            return t.strftime("%H:%M:%S")
        except ValueError:
            pass
    print("WARN: bad time format:", s)
    return None

@app.route("/dev/login/<user_id>")
def dev_login(user_id):
    session["userID"] = user_id
    flash(f"Logged in as {user_id}")
    return redirect(url_for("home"))

@app.route("/dev/logout")
def dev_logout():
    session.pop("userID", None)
    flash("Logged out")
    return redirect(url_for("home"))

@app.route("/CSR/Home")
def home():
    return render_template("home.html")

#Search New Request
@app.route("/CSR/Search", methods=["GET"])
def csr_search_new_requests():
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
        date=_parse_date(args.get("date")),
        time=_parse_time(args.get("time")),
        category=(args.get("category") or None),
        userID=(args.get("userID") or None),
        completed=completed,
        limit=int(args.get("limit", 50)),
        offset=int(args.get("offset", 0)),
    )

    print("INPUT ARGS:", dict(args))
    print("FILTERS:", filters)

    results = csr_cont.searchNewRequests(**filters) if clicked else []
    return render_template("csr_search.html", results=results, q=args)

#View All Requests
@app.route("/CSR/Requests", methods=["GET"])
def csr_list_all_requests():
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    rows = csr_view_cont.view_all_requests(limit=limit, offset=offset)
    return render_template("csr_requests_all.html", results=rows, limit=limit, offset=offset)

#Prompts if shortlisted success or already shortlisted
@app.route("/CSR/Shortlist/<request_id>", methods=["POST"])
def add_to_shortlist_status(request_id):
    csr_user_id = session.get("userID")
    added = shortlist_cont.add(request_id, csr_user_id)
    flash("Shortlisted successful." if added else "Already shortlisted.")
    referer = request.headers.get("Referer")
    return redirect(referer or url_for("csr_search_shortlisted"))

#Shortlist
@app.route("/CSR/SearchShortlist", methods=["GET"])
def csr_search_shortlist():
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    rows = csr_view_cont.view_all_requests(limit=limit, offset=offset)
    return render_template("csr_requests_all_shortlist.html", results=rows, limit=limit, offset=offset) 

#Search Shortlist
@app.route("/CSR/SearchShortlisted", methods=["GET"])
def csr_search_shortlisted():
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
        date=_parse_date(args.get("date")),
        time=_parse_time(args.get("time")),
        category=(args.get("category") or None),
        userID=(args.get("userID") or None),
        completed=completed,
        limit=int(args.get("limit", 50)),
        offset=int(args.get("offset", 0)),
    )

    results = search_shortlisted_cont.searchShortlisted(csr_user_id, **filters) if clicked else []
    return render_template("csr_search_shortlisted.html", results=results, q=args)

#View Shortlisted Requests
@app.route("/CSR/Shortlist/Requests", methods=["GET"])
def csr_view_shortlist_requests():
    csr_user_id = session.get("userID")
    if not csr_user_id:
        flash("Please log in as CSR to view your shortlist.")
        return redirect(url_for("home"))
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    rows = view_shortlist_cont.listShortlist(csr_user_id=csr_user_id, limit=limit, offset=offset)
    return render_template("csr_view_shortlist.html", results=rows, limit=limit, offset=offset)

#Search History
@app.route("/CSR/History", methods=["GET"])
def csr_search_history():
    args = request.args
    clicked = "Search" in args or len(args) > 0

    filters = dict(
        requestID=(args.get("requestID") or None),
        request=(args.get("request") if args.get("request") is not None else None),
        date=_parse_date(args.get("date")),
        time=_parse_time(args.get("time")),
        category=(args.get("category") or None),
        userID=(args.get("userID") or None),
        limit=int(args.get("limit", 50)),
        offset=int(args.get("offset", 0)),
    )

    results = history_cont.searchHistory(**filters) if clicked else []
    return render_template("csr_search_history.html", results=results, q=args)

#View History
@app.route("/CSR/Requests/Completed", methods=["GET"])
def csr_view_history():
    limit = int(request.args.get("limit", 100))
    offset = int(request.args.get("offset", 0))
    rows = view_history.historylist(limit=limit, offset=offset)
    return render_template("csr_view_history.html", results=rows, limit=limit, offset=offset)

if __name__ == "__main__":
    app.run()