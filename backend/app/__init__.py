from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from os import path
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS

# Uygulama ve Veritabanı Yapılandırması
app = Flask(__name__)
babel = Babel(app)
basedir = path.abspath(path.dirname(__file__))
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'site.db')
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"

# Uygulama Eklentileri
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)
csrf.init_app(app)
CORS(app, resources={r'/*' : {'origins': ['http://127.0.0.1:5000']}})
from app.my_admin.routes import MyAdminIndexView
admin = Admin(app, name='Admin' , template_mode='bootstrap3')
# index_view=MyAdminIndexView()
# Model ve View İçe Aktarmaları
from app.models import Product, Category, User, Comments, AboutFooter, CartItem, Cart, Contact, Newsletter, Order, OrderItem
from app.my_admin import ProductModelView, CategoryModelView, UserModelView, CommentsModelView, AboutFooterModelView, CartItemModelView, ContactFormModelView, NewsletterFormModelView, OrderItemModelView, OrderModelView
from app.auth import auth as auth_blueprint

# Admin Paneli
admin.add_view(UserModelView(User, db.session))
admin.add_view(ProductModelView(Product, db.session))
admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(CommentsModelView(Comments, db.session))
admin.add_view(AboutFooterModelView(AboutFooter, db.session))
admin.add_view(CartItemModelView(Cart, db.session))
admin.add_view(ContactFormModelView(Contact, db.session))
admin.add_view(NewsletterFormModelView(Newsletter, db.session))
admin.add_view(OrderModelView(Order, db.session))
admin.add_view(OrderItemModelView(OrderItem, db.session))

app.register_blueprint(auth_blueprint, url_prefix='/auth')
from app import views, models
from app.models import User

from app import app, db
from app.models import User

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    return csrf_token

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))