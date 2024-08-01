import os
import sys
from flask import Flask, flash, render_template, redirect, request
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from environs import Env

sys.path.append("src")

from models import Admin, Event, db


env = Env()
env.read_env()

ADMIN_EMAIL = env("ADMIN_EMAIL", "admin@localhost")
ADMIN_PASSWORD = env("ADMIN_PASSWORD", "admin")
SECRET_KEY = env("SECRET_KEY", os.urandom(24))
DATABASE_URI = 'sqlite:///site.db'
UPLOAD_FOLDER = 'src/static/img/events_page'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

db.create_all(app=app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Admin).get(user_id)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_static_files():
    css_files = []
    js_files = []

    for root, _, files in os.walk("src/static"):
        for file in files:
            if file.endswith(".css"):
                css_files.append(os.path.join(root, file))
            elif file.endswith(".js"):
                js_files.append(os.path.join(root, file))

    return css_files, js_files

def get_template_files():
    html_files = []

    for file in os.listdir("src/templates"):
        if file.endswith(".html"):
            html_files.append(os.path.join("templates", file))

    return html_files

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about_us")
def about():
    return render_template("about_us.html")

@app.route("/contacts")
def contact():
    return render_template("contacts.html")

@app.route("/events")
def events():
    events = db.session.query(Event).all()
    events = sorted(events, key=lambda x: x.id, reverse=True)
    return render_template("events.html", events=events)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

# AZ version

@app.route("/az")
@app.route("/index_az")
def index_az():
    return render_template("index_az.html")

@app.route("/about_us_az")
def about_az():
    return render_template("about_us_az.html")

@app.route("/contacts_az")
def contact_az():
    return render_template("contacts_az.html")

@app.route("/events_az")
def events_az():
    events = db.session.query(Event).all()
    events = sorted(events, key=lambda x: x.id, reverse=True)
    return render_template("events_az.html", events=events)

@app.route("/gallery_az")
def gallery_az():
    return render_template("gallery_az.html")

@app.route("/menu_az")
def menu_az():
    return render_template("menu_az.html")

# Admin panel

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/admin")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            admin = db.session.query(Admin).filter_by(email=email).first()
            if admin is None:
                admin = Admin(email=email, password=password)
                db.session.add(admin)
                try:
                    db.session.commit()
                except Exception as e:
                    print(f"Error creating admin: {e}")
            login_user(admin)

            return redirect("/admin")
        else:
            flash("Invalid email or password")

    return render_template("admin/login.html")
@app.route("/admin")
@login_required
def admin():
    css_files, js_files = get_static_files()
    html_files = get_template_files()

    return render_template("admin/admin.html", css_files=css_files, js_files=js_files, html_files=html_files)

@app.route("/admin-events")
@login_required
def admin_events():
    events = db.session.query(Event).all()
    return render_template("admin/events.html", events=events)

@app.route("/admin/event/add", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        title_en = request.form["title_en"]
        title_az = request.form["title_az"]
        content_en = request.form["content_en"]
        content_az = request.form["content_az"]
        image = request.files["image"]

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            event = Event(
                en_title=title_en,
                az_title=title_az,
                en_content=content_en,
                az_content=content_az,
                image=filename
            )
            db.session.add(event)
            db.session.commit()

            return redirect("/admin-events")

    return render_template("admin/event_add.html")

@app.route("/admin/event/delete/<int:event_id>", methods=["GET","POST"])
@login_required
def delete_event(event_id):
    if request.method == "GET":
        return render_template("admin/delete.html", url="/admin/event/delete/" + str(event_id))
    event = db.session.query(Event).get(event_id)
    db.session.delete(event)
    db.session.commit()

    return redirect("/admin-events")

@app.route("/admin/event/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    event = db.session.query(Event).get(event_id)

    if request.method == "POST":
        event.en_title = request.form["title_en"]
        event.az_title = request.form["title_az"]
        event.en_content = request.form["content_en"]
        event.az_content = request.form["content_az"]
        image = request.files["image"]

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            event.image = filename

        db.session.add(event)
        db.session.commit()

        return redirect("/admin-events")

    return render_template("admin/edit_event.html", event=event)

@app.route("/admin/file/edit", methods=["GET", "POST"])
@login_required
def edit_file():
    filename = request.args.get("filename")
    filename = os.path.join("src", filename)
    if request.method == "POST":
        content = request.form["file-text"]

        content = content.replace('\r\n', '\n').replace('\r', '\n')


        with open(filename, "w") as file:
            file.write(content)

        return redirect("/admin")

    with open(filename, "r") as file:
        content = file.read()

    return render_template("admin/edit_file.html", content=content, filename=filename, url="/admin/file/edit?filename=" + filename)

@app.route("/admin/create/initial")
@login_required
def create_initial():
    if db.session.query(Event).count() == 0:
        event1 = Event(
            en_title="DINING ROOMS", az_title="DINING ROOMS",
            az_content="İki lüks zalımız xüsusi tədbirlər keçirmək üçün mükəmməldir. Hər zal 16 qonağı qəbul edə bilər.",
            en_content="Our two luxurious dining rooms are perfect for hosting private events. Each room can accommodate up to 16 guests.",
            image="vip_lounge.png")
        event2 = Event("DRAGON LOUNGE","DRAGON LOUNGE",
                    "Böyük pilləkənləri ilə cəlb edən Dragon Lounge ikinci mərtəbədə yerləşir. 80 nəfərə qədər qonaq qəbul edə bilər.",
                    "Located on the mezzanine and accessed via its own grand staircase. The lounge can accommodate up to 80 guests for a seated dinner.",
                    "dragon_lounge.png")
        event3 = Event("PAN ASIAN DINING","PAN ASIAN DINING",
                    "PAN ASIAN DINING yerli üslubları Asiya təsirləri ilə birləşdirir və tədbirlər üçün mükəmməl məkandır. Burada geniş açıq mətbəx və zərif bambuk dekorları mövcuddur. Rahat atmosfer 102 nəfərdən çox qonağı qəbul edə bilər.",
                    "This area blends local styles with Asian influences, perfect for events. It features a spacious open kitchen and elegant bamboo décor. The inviting atmosphere can accommodate over 102 guests.",
                    "chinarDining_slider_bg.png")
        
        event4 = Event("BAMBOO BAR", "BAMBOO BAR",
                    "Bamboo Bar görüşlər və xüsusi tədbirlər üçün ideal yerdir. 48 nəfərə qədər qonaq qəbul edə bilən Bamboo Bar istənilən hadisə üçün mükəmməl məkandır.",
                    "The Bamboo Bar is an ideal spot for gatherings and special events. With the capacity to host up to 48 guests, it’s a perfect venue for any occasion.",
                    "bambooBar_slider_bg.png")
        
        event5 = Event("THE TERRACE", "THE TERRACE",
                    "Məkanımız açıq terras və çinar ağacları ilə parlaq və təravətli atmosfer təqdim edir. Terras 120 nəfərə qədər qonaq qəbul edə bilər və bu, istənilən tədbir üçün mükəmməl şərait yaradır.",
                        "Our venue offers a bright and fresh atmosphere with an open terrace and a chinar grove. The terrace can accommodate up to 120 guests, providing a perfect setting for any gathering",
                        "terrace_bg.png")
        db.session.add(event1)
        db.session.add(event2)
        db.session.add(event3)
        db.session.add(event4)
        db.session.add(event5)
        db.session.commit()
    return redirect("/admin")

@app.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
