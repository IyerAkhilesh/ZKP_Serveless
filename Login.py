from flask import Flask, render_template, url_for, request
import pickle
app = Flask(__name__)

@app.route("/")
# Outputs an html login template via an html file
def home_template():
    return render_template("home.html")

@app.route("/after_login", methods=["POST"])
#Outputs the html file which should show up after login
def after_login_template():
    result = request.form
    username, password = result.items()
    print("Username and password\t",  result.items())
    print(username, password)
    # client.set_credentials(username, password)
    file = open("shared.pkl", "wb")
    credential_set = (username, password)
    pickle.dump(credential_set, file)
    return render_template("after_login.html", result=result)

if __name__ == "__main__":
    app.debug = True
    print(app.debug)
    app.run()
