import sqlite3
from flask import Flask
from flask import redirect,make_response, abort, render_template, request,session,flash,url_for
import config
import db
import items
import re
import users
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def forbidden_access():
    abort(403)  

def not_found():
    abort(404)

def check_csrf():
    
    if "csrf_token" not in request.form:
        abort(403)     

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items = all_items)

#Shows user page
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        not_found()
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user,items=items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query=""
        results = []
    return render_template("find_item.html", query=query,results=results)

#Shows specific item's page
@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    
    if not item:
        not_found()
    classes = items.get_classes(item_id)
    vaihteisto = items.get_specific_class(item_id, 'vaihteisto')
    tyyppi = items.get_specific_class(item_id, 'tyyppi')
    bids = items.get_bids(item_id)
    minimum_bid = items.get_minimum_bid(item_id)
    images = items.get_images(item_id)
    return render_template("show_item.html", item=item, classes=classes, bids=bids, minimum_bid = minimum_bid, vaihteisto = vaihteisto,
                           tyyppi = tyyppi, images=images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = items.get_image(image_id)
    if not image:
        not_found()

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response


@app.route("/images/<int:item_id>")
def edit_images(item_id):
    require_login()
    item = items.get_item(item_id)
    
    if not item:
        not_found()
    if item["user_id"] != session["user_id"]:
        forbidden_access()
    
    images = items.get_images(item_id)    
        
    return render_template("images.html", item=item, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    
    if not item:
        not_found()
    if item["user_id"] != session["user_id"]:
        forbidden_access()
    
    file = request.files["image"]
    if not file.filename.endswith(".jpg"):
            return "VIRHE: väärä tiedostomuoto"

    image = file.read()
    if len(image) > 100 * 1024:
            return "VIRHE: liian suuri kuva"

    
    items.add_image(item_id, image)
    return redirect("/images/" + str(item_id))


@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    
    if not item:
        not_found()
    if item["user_id"] != session["user_id"]:
        forbidden_access()
    
    for image_id in request.form.getlist("image_id"):
        items.remove_image(item_id, image_id)
        
    return redirect("/images/" + str(item_id))


    
@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html",classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()
    title = request.form["title"]
    if not title or len(title) > 60:
        forbidden_access()    
    price = request.form["price"]
    if not re.search("^[1-9][0-9]{0,9}$", price):
        forbidden_access()
    description = request.form["description"]
    if not description or len(description) > 1000:
        forbidden_access()
    user_id = session["user_id"]
    
    all_classes = items.get_all_classes()
    
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                forbidden_access()
            if class_value not in all_classes[class_title]:
                forbidden_access()   
            classes.append((class_title, class_value))

    items.add_item(title,description,price,user_id, classes)
    item_id = db.last_insert_id()
    return redirect("/item/" + str(item_id))

@app.route("/create_bid", methods=["POST"])
def create_bid():
    require_login()
    check_csrf()
    price = request.form["price"]
    if not re.search("^[1-9][0-9]{0,9}$", price):
        forbidden_access()
    price = int(price)    
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    
    if not item:
        not_found()    
        
    user_id = session["user_id"]
    minimum_bid = items.get_minimum_bid(item_id)
    if price < minimum_bid:
        return "VIRHE: Suurempi tarjous on jo olemassa"
    items.add_bid(item_id, user_id, price)
    
    return redirect("/item/" + str(item_id))

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()
    
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        forbidden_access()
    if not item:
        not_found()
        
    title = request.form["title"]
    if not title or len(title) > 60:
        forbidden_access()
    price = request.form["price"]
    if not re.search("^[1-9][0-9]{0,9}$", price):
        forbidden_access()    
    description = request.form["description"]
    if not description or len(description) > 1000:
        forbidden_access()
        
    all_classes = items.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                forbidden_access()
            if class_value not in all_classes[class_title]:
                forbidden_access()    
            classes.append((class_title, class_value))

    items.update_item(item_id, title, description, price, classes)
    
    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    
    if not item:
        not_found()
    if item["user_id"] != session["user_id"]:
        forbidden_access()
    
    all_classes = items.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]
        
       
    return render_template("edit_item.html",item=item ,classes=classes ,all_classes=all_classes)

@app.route("/remove_item/<int:item_id>", methods=["GET","POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        forbidden_access()
    if not item:
        not_found()
    if request.method == "GET":
        item = items.get_item(item_id)
        return render_template("remove_item.html", item=item)
    
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
             
         

#If theres no user throws index out of range error
@app.route("/login", methods=["GET","POST"])
def login():
    
    if request.method == "GET":
        return render_template("login.html")
        
    if request.method== "POST":
        
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        
        if user_id:
            session["user_id"] = user_id 
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            
            return render_template("login.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")



@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät täsmää"
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "Virhe: Tunnus on jo olemassa" 
               

    return "Tunnus luotu"
                
            


      
