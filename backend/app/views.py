from flask import render_template, redirect, url_for, request, flash, jsonify
from sqlalchemy import or_
from app import app, db
from flask_login import current_user, login_required
from app.models import Product, Comments, AboutFooter, Cart, CartItem, Contact, Newsletter, Order, OrderItem
from app.forms import ContactForm, NewsletterForm, ChangePasswordForm
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

"""@app.route('/')
def index():
    products = Product.query.all()
    product_len = len(products)
    clients = Comments.query.all()
    about = AboutFooter.query.all()
    return render_template('index.html', products=products, clients = clients,product_len=product_len, about=about)"""

# TAMAMLANDI.
@app.route('/about')  # API endpoint'i
def about():
    about_data = AboutFooter.query.first()  # İlk about verisini alıyoruz, varsayılan olarak
    if about_data:  # Veri varsa
        # JSON formatında veriyi döndürüyoruz
        return jsonify({
            'about': about_data.about,
            'about_text': about_data.about_text,
            'about_image': about_data.about_image,
            'adress': about_data.adress,
            'call': about_data.call,
            'email': about_data.email,
            'footer': about_data.footer,
            'google_maps': about_data.google_maps,
            'facebook': about_data.facebook,
            'twitter': about_data.twitter,
            'linkedin': about_data.linkedin,
            'instagram': about_data.instagram,
            'contactheader': about_data.contactheader,
            'contacttext': about_data.contacttext
        })
    else:  # Veri yoksa
        # Hata durumunu JSON formatında döndürüyoruz
        return jsonify({'error': 'About data not found'}), 404  # 404 Not Found status kodu ile

# TAMAMLANDI
@app.route('/api/contact', methods=["POST"])
def add_contact():
    if request.method == "POST":
        data = request.json
        new_contact = Contact(name=data['name'], email=data['email'], message=data['message'])
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "Contact added successfully"}), 201

# TAMAMLANDI
@app.route('/api/newsletter', methods=["POST"])
def add_newsletter():
    if request.method == "POST":
        data = request.json
        new_subscriber = Newsletter(email=data['email'])
        db.session.add(new_subscriber)
        db.session.commit()
        return jsonify({"message": "Subscriber added successfully"}), 201

# TAMAMLANDI
@app.route('/client')
def client():
    clients = Comments.query.all()
    client_data = []
    for client in clients:
        client_data.append({
            'client_name': client.client_name,
            'client_comment': client.client_comment,
            'client_image': client.client_image
        })
    return jsonify(client_data)

# TAMAMLANDI
@app.route('/products')
def products():
    products = Product.query.all()
    product_data = [{'id': product.id, 'name': product.name, 'description': product.description, 'image_url': product.image_url, 'price': product.price,'is_show': product.is_show, 'active': product.is_active} for product in products]
    return jsonify({'products': product_data})

# TAMAMLANDI.
@app.route('/api/purchase/<int:id>', methods=['POST'])
@login_required
def purchase_product(id):
    user_id = current_user.get_id()
    username = current_user.username

    # Sepet işlemleri
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        new_cart = Cart(user_id=user_id, username=username)
        db.session.add(new_cart)
        db.session.commit()

    product = Product.query.get_or_404(id)

    cart_item = CartItem.query.filter_by(cart_id=user_id, product_id=product.id).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = CartItem(cart_id=user_id, product_id=product.id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()

    return jsonify({"message": "Product added to cart successfully"}), 200

# TAMAMLANDI.
@app.route("/api/remove_from_cart/<int:id>", methods=['POST'])
@login_required
def remove_from_cart(id):
    # Kullanıcı girişi kontrolü yapılıyor
    user_id = current_user.get_id()

    # Kullanıcının sepetini al
    cart = Cart.query.filter_by(user_id=user_id).first()

    # Sepet öğesini bul
    cart_item = CartItem.query.filter_by(cart_id=user_id, product_id=id).first()

    if cart_item:
        # Sepet öğesini veritabanından kaldır
        db.session.delete(cart_item)
        db.session.commit()

    return redirect(url_for('cart'))

# TAMAMLANDI.
@app.route("/api/cart")
@login_required
def cart():
    # Kullanıcı girişi kontrolü yapılıyor
    user_id = current_user.get_id()

    # Kullanıcının sepet içeriğini al
    cart_items = CartItem.query.filter_by(cart_id=user_id).all()

    # Sepet toplamını hesaplamak için başlangıç değeri
    cart_total = 0
    cart_list = []

    for cart in cart_items:
        product_price = cart.product.price
        quantity = cart.quantity
        
        item_total = product_price * quantity
        
        cart_total += item_total

        # Her ürünün detaylarını JSON uyumlu bir şekilde oluştur
        cart_item_json = {
            "product_id": cart.product.id,
            "product_name": cart.product.name,
            "quantity": quantity,
            "price": product_price,
            "item_total": item_total
        }
        
        cart_list.append(cart_item_json)
        
    # Sepet toplamını cent cinsinden al
    cart_total_cents = int(cart_total * 100)

    # Dolar ve cent olarak böl
    dollars = cart_total_cents // 100
    cents = cart_total_cents % 100
    
    # JSON olarak sepet bilgilerini döndür
    return jsonify({
        "cart_items": cart_list,
        "total_dollars": dollars,
        "total_cents": cents
    })

@app.route('/api/search')
def search():
    query = request.args.get('query', '')
    
    # Ürünleri filtrele ve sonuçları al
    products = Product.query.filter(or_(Product.name.ilike(f'%{query}%'), Product.description.ilike(f'%{query}%'))).all()
    
    # JSON formatında sonuçları hazırla
    product_list = [{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "image_url": product.image_url,
        "price": product.price
    } for product in products]
    
    return jsonify({
        "query": query,
        "products": product_list,
        "product_len": len(product_list)
    })

# TAMAMLANDI.
@app.route("/api/order", methods=['POST'])
@login_required
def place_order():
    # Kullanıcı girişi kontrolü yapılıyor
    user_id = current_user.get_id()

    # Kullanıcının sepet içeriğini al
    cart_items = CartItem.query.filter_by(cart_id=user_id).all()

    cart_total = 0
    order_items = []

    # Sepetteki her ürün için sipariş öğesi oluştur
    for cart_item in cart_items:
        product_price = cart_item.product.price
        quantity = cart_item.quantity
        item_total = product_price * quantity
        cart_total += item_total

        order_item = {
            "product_id": cart_item.product.id,
            "quantity": quantity
        }
        order_items.append(order_item)

    # Yeni bir sipariş oluştur
    new_order = Order(user_id=user_id, cart_total=int(cart_total * 100), order_date=datetime.utcnow())
    db.session.add(new_order)
    db.session.commit()

    # Sepetteki her ürün için sipariş öğesi oluştur
    for cart_item in cart_items:
        product_id = cart_item.product.id
        quantity = cart_item.quantity

        new_order_item = OrderItem(order_id=new_order.id, product_id=product_id, quantity=quantity)
        db.session.add(new_order_item)

    # Sepeti temizle
    CartItem.query.filter_by(cart_id=user_id).delete()
    db.session.commit()

    # JSON olarak sipariş bilgilerini döndür
    return jsonify({
        "success": True,
        "message": "Order placed successfully",
        "order_items": order_items,
        "total_dollars": cart_total // 100,
        "total_cents": cart_total % 100
    })

# TAMAMLANDI.
@app.route('/api/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()

    if not all(key in data for key in ['old_password', 'new_password']):
        return jsonify({"error": "Missing data"}), 400

    old_password = data['old_password']
    new_password = data['new_password']

    # current_user'dan kullanıcının bilgilerini alıyoruz
    user = current_user

    if not user.check_password(old_password):
        return jsonify({"error": "Invalid old password"}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({"message": "Password changed successfully"}), 200