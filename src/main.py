import os
import sys
from flask import Flask, flash, render_template, redirect, jsonify, send_file, request, abort
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from environs import Env

sys.path.append("src")

from models import Admin, Event, FormSubmission, GalleryImage, Menu, db
from utils import send_email

env = Env()
env.read_env()


ADMIN_EMAIL = env("ADMIN_EMAIL", "admin@localhost")
ADMIN_PASSWORD = env("ADMIN_PASSWORD", "admin")
SECRET_KEY = env("SECRET_KEY", os.urandom(24))
DATABASE_URI = f"postgresql+psycopg2://{env('DB_USER', 'postgres')}:{env('DB_PASSWORD', 'postgres')}@{env('DB_HOST', 'localhost')}:{env('DB_PORT', '5432')}/{env('DB_NAME', 'postgres')}"
UPLOAD_FOLDER = env("UPLOAD_FOLDER", "/chinarv/")
OWNER_EMAIL = env("OWNER_EMAIL", "owner@localhost")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, user_id)

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

    menu = db.session.query(Menu).first()

    menu1 = menu.data["menu1"]
    menu2_1 = menu.data["menu2"]["exclusive_left"]
    menu2_2 = menu.data["menu2"]["exclusive_right"]
    menu3_1 = menu.data["menu3"]["dessert_left"]
    menu3_2 = menu.data["menu3"]["dessert_right"]
    menu4 = menu.data["menu4"]

    return render_template("menu.html",
                            menu1=menu1,
                            menu2_first_half=menu2_1,
                            menu2_second_half=menu2_2,
                            menu3_first_half=menu3_1,
                            menu3_second_half=menu3_2,
                            menu4=menu4)

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

    menu = db.session.query(Menu).first()

    menu1 = menu.data["menu1"]
    menu2_1 = menu.data["menu2"]["exclusive_left"]
    menu2_2 = menu.data["menu2"]["exclusive_right"]
    menu3_1 = menu.data["menu3"]["dessert_left"]
    menu3_2 = menu.data["menu3"]["dessert_right"]
    menu4 = menu.data["menu4"]


    return render_template("menu_az.html",
                            menu1=menu1,
                            menu2_first_half=menu2_1,
                            menu2_second_half=menu2_2,
                            menu3_first_half=menu3_1,
                            menu3_second_half=menu3_2,
                            menu4=menu4)

# Admin panel

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/admin")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        admin = db.session.query(Admin).filter_by(email=email).first()

        if email == ADMIN_EMAIL and password == admin.password:
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
            az_content="İki lüks zalımız tədbirlər keçirmək üçün mükəmməldir. Hər zal 16 qonağı qəbul edə bilər.",
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
                    "Bamboo Bar görüşlər və tədbirlər üçün ideal yerdir. 48 nəfərə qədər qonaq qəbul edə bilən Bamboo Bar istənilən hadisə üçün mükəmməl məkandır.",
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

@app.get("/event/<int:event_id>")
def get_event(event_id):
    img_url = db.session.query(Event).get(event_id).image
    if img_url is None:
        abort(404)
    if event_id > 5:
        return send_file(os.path.join(UPLOAD_FOLDER, img_url), mimetype='image')
    return send_file("static/img/events_page/" + img_url, mimetype='image')

@app.route("/admin/change/password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            flash("Passwords do not match")
            return render_template("admin/change_password.html")

        admin = db.session.query(Admin).get(current_user.id)
        if admin.password != old_password:
            flash("Old password is incorrect")
            return render_template("admin/change_password.html")

        admin.password = new_password
        db.session.add(admin)
        db.session.commit()

        return redirect("/admin")
    
    return render_template("admin/change_password.html")

@app.post("/voucher")
def register_voucher():
    form_data = request.form

    submission = FormSubmission(data=form_data)

    db.session.add(submission)
    db.session.commit()

    message = f"Hello, Client {form_data['name']} {form_data['surname']} has requested {form_data['voucherCount']} vouchers, each for {form_data['voucherPrice']} AZN. The total price is {int(form_data['voucherCount']) * int(form_data['voucherPrice'])} AZN. The client's email address is {form_data['email']} and phone number is {form_data['phone']}."
    send_email(OWNER_EMAIL, 
                message, 
                "Voucher Request", 
                "Voucher Request")
    return redirect("/about_us")

@app.post("/voucher_az")
def register_voucher_az():
    form_data = request.form

    submission = FormSubmission(data=form_data)

    db.session.add(submission)
    db.session.commit()

    message = f"Hello, Client {form_data['name']} {form_data['surname']} has requested {form_data['voucherCount']} vouchers, each for {form_data['voucherPrice']} AZN. The total price is {int(form_data['voucherCount']) * int(form_data['voucherPrice'])} AZN. The client's email address is {form_data['email']} and phone number is {form_data['phone']}."
    send_email(OWNER_EMAIL,
                message, 
                "Voucher Request", 
                "Voucher Request")
    return redirect("/about_us_az")

@app.post("/form/submission")
def submit_form():
    data = request.form
    form_submission = FormSubmission(data)
    db.session.add(form_submission)
    db.session.commit()

    return redirect("/")

@app.get("/admin/form/submissions")
@login_required
def form_submissions():
    submissions = db.session.query(FormSubmission).all()
    return render_template("admin/form_submissions.html", submissions=submissions)

@app.post("/admin/form/submissions/delete")
@login_required
def delete_submissions():
    db.session.query(FormSubmission).delete()
    db.session.commit()

    return redirect("/admin/form/submissions")

@app.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.get("/admin/gallery")
def admin_galley():
    images = db.session.query(GalleryImage).all()
    return render_template("admin/gallery.html", images=images)

@app.post("/admin/gallery/delete/<int:image_id>")
def delete_gallery_image(image_id):
    image = db.session.query(GalleryImage).get(image_id)
    if image is None:
        abort(404)

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.image_url)

    if os.path.exists(image_path):
        os.remove(image_path)
    else:
        print(f"File not found: {image_path}")

    db.session.delete(image)
    db.session.commit()

    return redirect("/admin/gallery")

@app.post("/admin/gallery/add")
def add_gallery_image():
    images = request.files.getlist("images")

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    for image in images:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'] + filename))

        gallery_image = GalleryImage(image_url=filename)

        db.session.add(gallery_image)

        db.session.commit()

    return redirect("/admin/gallery")

@app.get("/gallery/images")
def get_gallery_images():
    images = db.session.query(GalleryImage).all()

    images = [image.id for image in images]

    return jsonify(images)

@app.get("/gallery/image/<int:image_id>")
def get_gallery_image(image_id):
    image = db.session.query(GalleryImage).get(image_id)
    if image is None:
        abort(404)
    image_path = os.path.join(UPLOAD_FOLDER, image.image_url)
    if not os.path.exists(image_path):
        abort(404)
    return send_file(image_path, mimetype='image')

@app.get("/admin/menu")
def admin_menu():
    return render_template("admin/menu.html")

@app.get('/api/menu')
def get_menu():
    menu = db.session.query(Menu).first()
    return jsonify(menu.data)

@app.post('/api/menu')
def add_item_to_menu():
    menu = db.session.query(Menu).first()
    new_item = request.json
    menu.data[new_item['menu']][new_item['section']] = new_item['item']

    db.session.commit()

    return jsonify(menu.data)

@app.put('/api/menu')
def update_menu():
    new_menu_data = request.json
    menu = db.session.query(Menu).first()
    menu.data = new_menu_data
    db.session.commit()
    return jsonify({"message": "Menu updated successfully"})

@app.route("/robots.txt")
def robots():
    return send_file("/static/robots.txt", mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
