    profs = Professor.query.all()
    assts = Assistant.query.all()

    if request.method == "POST":
        account_id = request.form.get("account_id")
