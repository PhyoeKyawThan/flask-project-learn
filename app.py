from flask import Flask, render_template, request, session
import sqlite3
app = Flask(__name__)
app.config["SECRET_KEY"] = 'OMAKDKSK'
class Model:
    def __init__(self, db_name) -> None:
        self.connect = sqlite3.connect(db_name)
        self.cursor = self.connect.cursor()
        self.cursor.execute("""create table if not exists 
                            user(id integer primary key autoincrement, 
                            username varchar(20), 
                            email varchar(100), 
                            password varchar(100))""")
        self.connect.commit()
    def insert(self, username, email, password):
        self.cursor.execute(f"""insert into 
                            user(username, email, password) 
                            values('{username}', '{email}', '{password}')""")
        self.connect.commit()

    def getAllUser(self):
        return self.cursor.execute("select * from user").fetchall()
    
    def close(self):
        self.cursor.close()
        self.connect.close()

@app.route("/current_user") # http://127.0.0.1/home
def index():
    return render_template("index.html", current_user=session["current_user"])

@app.route("/signup")
def singup_view():
    return render_template("signup.html")

@app.route("/api/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        model = Model("test.db")
        model.insert(username, email, password)
        model.close()
        return "User created"

@app.route("/login")
def login_view():
    return render_template("login.html")

@app.route("/api/login", methods=["POST"])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        model = Model("test.db")
        if model.check_user(email, password):
            session["current_user"] = f"{model.getUser(email)}"
            model.close()
            return "User exist"
        model.close()
        return "Incorrect email or password"

@app.route("/view_user")
def view_user():
    model = Model("test.db")
    return render_template("view_user.html",
                            users=model.getAllUser())


