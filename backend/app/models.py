from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    
    # product ilişkisi, CartItem'dan Product'e yönlendirme yapacak
    product = db.relationship('Product', backref='cart_items', lazy=True)

    def __repr__(self):
        return f'<CartItem {self.product}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)  # Kategori ilişkisi
    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    brand = db.Column(db.String(100), nullable=True)  # Marka
    image_url = db.Column(db.String(255), nullable=True)  # Ürün resmi URL'si
    color = db.Column(db.String(50))  # Ürün rengi
    size = db.Column(db.String(50))  # Ürün boyutu
    weight = db.Column(db.Float)  # Ürün ağırlığı
    is_active = db.Column(db.Boolean, default=True)  # Ürünün aktif/pasif durumu
    is_show = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_comment = db.Column(db.String(500), nullable=False)
    client_image = db.Column(db.String(255), nullable=True) 
    
class AboutFooter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    about = db.Column(db.String(100), nullable=False)
    about_text = db.Column(db.String(255), nullable=True)
    about_image = db.Column(db.String(255), nullable=True)
    adress = db.Column(db.String(255), nullable=True)
    call = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    footer = db.Column(db.String(255), nullable=True)
    google_maps = db.Column(db.String, nullable=True)
    facebook = db.Column(db.String(255), nullable=True)
    twitter = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    contactheader = db.Column(db.String(255), nullable=True)
    contacttext = db.Column(db.String(255), nullable=True)
    
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    
class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cart_total = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # İlişkiler
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # İlişkiler
    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))
    
    def __repr__(self):
        return 'Product {} - Price: {}'.format(self.product, self.product.price)