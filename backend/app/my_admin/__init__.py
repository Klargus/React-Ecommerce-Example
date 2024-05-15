from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, form
from app.models import Product, Category
from flask_login import current_user
from wtforms import validators
from flask import redirect, url_for, request
from werkzeug.datastructures import FileStorage
from flask_admin.form import rules
from flask_admin import expose
from app import app,db
from app.models import Cart, CartItem
from flask import jsonify

class MyModelView(ModelView):
    def is_accessible(self):
        # Yetkilendirme kontrolü yapılıyor
        # Örneğin, current_user.is_admin, kullanıcının yönetici olup olmadığını kontrol eden bir özellik olmalıdır
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

    def inaccessible_callback(self, name, **kwargs):
        # Erişim reddedildiğinde ne yapılacağını belirleyin
        # Örneğin, kullanıcıyı giriş sayfasına yönlendirin
        return redirect(url_for('auth.login', next=request.url))
    
class UserModelView(MyModelView):
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash"]
    column_searchable_list = ["username", "email"]

class ProductModelView(MyModelView):
    
    column_list = ('name', 'price', 'stock', 'category', 'brand', 'is_show')  # Gösterilecek sütunlar
    form_columns = ('name', 'description', 'price', 'stock', 'category', 'brand', 'image_url', 'color', 'size', 'weight', 'is_active', 'is_show')  # Düzenlenebilir sütunlar
    column_searchable_list = ('name', 'brand')  # Aranabilir sütunlar
    column_filters = ('category.name', 'brand')  # Filtrelenebilir sütunlar
    form_args = {
        'name': {
            'validators': [validators.DataRequired()]
        },
        'price': {
            'label': 'Price ($)',
            'validators': [validators.NumberRange(min=0)]
        },
        'stock': {
            'validators': [validators.NumberRange(min=0)]
        }
    }
    
    column_formatters ={
        'price': lambda view, context, model, name: "${:,.2f}".format(float(model.price)) if model.price is not None else None
    }
    
    form_extra_fields = {
        'image_url': form.ImageUploadField('Image', base_path='app/static/images', url_relative_path='app/static/images/')
    }
    
    def on_model_change(self, form, model, is_created):
        if form.image_url.data and isinstance(form.image_url.data, FileStorage):
            # Dosyanın tam statik yolu
            static_path = f"images/{form.image_url.data.filename}"
            model.image_url = static_path
        elif form.image_url.raw_data and isinstance(form.image_url.raw_data[0], FileStorage) and model.image_url is not None:
            # ImageUploadField boşsa ve veritabanında mevcut bir image_url varsa,
            # mevcut değeri kullan
            model.image_url = model.image_url
        else:
            # Eğer ImageUploadField boş değilse ve bir dosya varsa, image_url'i güncelle
            if isinstance(form.image_url.object_data, FileStorage):
                model.image_url = form.image_url.object_data.filename
            

class CategoryModelView(MyModelView):
    column_list = ('name',)  # Gösterilecek sütunlar
    form_columns = ('name',)  # Düzenlenebilir sütunlar
    column_searchable_list = ('name',)  # Aranabilir sütunlar
    form_args = {
        'name': {
            'validators': [validators.DataRequired()]
        }
    }
    
class CommentsModelView(MyModelView):
    column_list = ('client_name', 'client_comment', 'client_image')  # Gösterilecek sütunlar
    form_columns = ('client_name', 'client_comment', 'client_image')  # Düzenlenebilir sütunlar
    column_searchable_list = ('client_name',)  # Aranabilir sütunlar
    form_args = {
        'client_name': {
            'validators': [validators.DataRequired()]
        },
        'client_comment': {
            'validators': [validators.DataRequired()]
        }
    }
    
    form_extra_fields = {
        'client_image': form.ImageUploadField('Image', base_path='app/static/clients', url_relative_path='app/static/clients/')
    }
    
    def on_model_change(self, form, model, is_created):
        if form.client_image.data and isinstance(form.client_image.data, FileStorage):
            # Dosyanın tam statik yolu
            static_path = f"clients/{form.client_image.data.filename}"
            model.client_image = static_path
        elif form.client_image.raw_data and isinstance(form.client_image.raw_data[0], FileStorage) and model.client_image is not None:
            # ImageUploadField boşsa ve veritabanında mevcut bir client_image varsa,
            # mevcut değeri kullan
            model.client_image = model.client_image
        else:
            # Eğer ImageUploadField boş değilse ve bir dosya varsa, client_image'i güncelle
            if isinstance(form.client_image.object_data, FileStorage):
                model.client_image = form.client_image.object_data.filename
            
class BannerModelView(MyModelView):
    column_list = ('name', 'price', 'stock', 'category', 'brand')  # Gösterilecek sütunlar
    form_columns = ('name', 'description', 'price', 'stock', 'category', 'brand', 'image_url', 'color', 'size', 'weight', 'is_active')  # Düzenlenebilir sütunlar
    column_searchable_list = ('name', 'brand')  # Aranabilir sütunlar
    column_filters = ('category.name', 'brand')  # Filtrelenebilir sütunlar
    form_args = {
        'name': {
            'validators': [validators.DataRequired()]
        },
        'price': {
            'label': 'Price ($)',
            'validators': [validators.NumberRange(min=0)]
        },
        'stock': {
            'validators': [validators.NumberRange(min=0)]
        }
    }
    
    column_formatters ={
        'price': lambda view, context, model, name: "${:,.2f}".format(float(model.price)) if model.price is not None else None
    }
    
    form_extra_fields = {
        'image_url': form.ImageUploadField('Image', base_path='app/static/images', url_relative_path='app/static/images/')
    }
    
    def on_model_change(self, form, model, is_created):
        if form.image_url.data and isinstance(form.image_url.data, FileStorage):
            # Dosyanın tam statik yolu
            static_path = f"images/{form.image_url.data.filename}"
            model.image_url = static_path
        elif form.image_url.raw_data and isinstance(form.image_url.raw_data[0], FileStorage) and model.image_url is not None:
            # ImageUploadField boşsa ve veritabanında mevcut bir image_url varsa,
            # mevcut değeri kullan
            model.image_url = model.image_url
        else:
            # Eğer ImageUploadField boş değilse ve bir dosya varsa, image_url'i güncelle
            if isinstance(form.image_url.object_data, FileStorage):
                model.image_url = form.image_url.object_data.filename
                
class AboutFooterModelView(MyModelView):
    column_list = ('about', 'about_text', 'adress', 'call', 'email', 'footer', 'facebook', 'twitter', 'linkedin', 'instagram', 'contactheader', 'contacttext', 'google_maps')  # Gösterilecek sütunlar
    form_columns = ('about','about_text', 'about_image', 'adress', 'call', 'email', 'footer', 'facebook', 'twitter', 'linkedin', 'instagram', 'contactheader', 'contacttext', 'google_maps')  # Düzenlenebilir sütunlar
    column_searchable_list = ('about','about_text', 'adress', 'call', 'email', 'footer', 'facebook', 'twitter', 'linkedin', 'instagram', 'contactheader', 'contacttext')  # Aranabilir sütunlar
    
    form_args = {
    'about': {
        'validators': [validators.DataRequired()]
    },
    'about_text': {
        'validators': [validators.DataRequired()]
    },
    'adress': {
        'validators': [validators.DataRequired()]
    },
    'call': {
        'validators': [validators.DataRequired(), validators.Regexp(r'^\d{10}$')]
    },
    'email': {
        'validators': [validators.DataRequired(), validators.Email()]
    },
    'footer': {
        'validators': [validators.DataRequired()]
    },
    'facebook': {
        'validators': [validators.DataRequired(), validators.URL()]
    },
    'twitter': {
        'validators': [validators.DataRequired(), validators.URL()]
    },
    'linkedin': {
        'validators': [validators.DataRequired(), validators.URL()]
    },
    'instagram': {
        'validators': [validators.DataRequired(), validators.URL()]
    },
    'contactheader': {
        'validators': [validators.DataRequired()]
    },
    'contacttext': {
        'validators': [validators.DataRequired()]
    },
    'google_maps':{
        'validators': [validators.DataRequired()]
    }
}

    
    form_extra_fields = {
        'about_image': form.ImageUploadField('About Image', base_path='app/static/images', url_relative_path='app/static/images/')
        # Diğer form_extra_fields ayarlarını buraya ekleyebilirsiniz
    }
    
    def on_model_change(self, form, model, is_created):
        if form.about_image.data and isinstance(form.about_image.data, FileStorage):
            # Dosyanın tam statik yolu
            static_path = f"images/{form.about_image.data.filename}"
            model.about_image = static_path
        elif form.about_image.raw_data and isinstance(form.about_image.raw_data[0], FileStorage) and model.about_image is not None:
            # ImageUploadField boşsa ve veritabanında mevcut bir about_image varsa,
            # mevcut değeri kullan
            model.about_image = model.about_image
        else:
            # Eğer ImageUploadField boş değilse ve bir dosya varsa, about_image'i güncelle
            if isinstance(form.about_image.object_data, FileStorage):
                model.about_image = form.about_image.object_data.filename
                
class CartItemModelView(MyModelView):
    # CartItem modeli için bir görünüm (view) oluşturuyoruz
    # Bu sınıfı özelleştirerek admin panelinde nasıl görüneceğini belirleyebiliriz
    column_list = ('id', 'user_id','username', 'cart.items')  # Gösterilecek sütunlar
    column_searchable_list = ('user_id')  # Aranabilir sütunlar

    def init_search(self):
        return False
    
class ContactFormModelView(MyModelView):
    column_list = ('id','name','email', 'message')
    column_searchable_list = ('email')
    
    def init_search(self):
        return False
    
class NewsletterFormModelView(MyModelView):
    column_list = ('id','email')
    def init_search(self):
        return False
    
class OrderItemModelView(MyModelView):
    # OrderItem modeli için bir görünüm (view) oluşturuyoruz
    # Bu sınıfı özelleştirerek admin panelinde nasıl görüneceğini belirleyebiliriz
    column_list = ('id', 'order_id', 'product.name', 'quantity')  # Gösterilecek sütunlar

class OrderModelView(MyModelView):
    # Order modeli için bir görünüm (view) oluşturuyoruz
    # Bu sınıfı özelleştirerek admin panelinde nasıl görüneceğini belirleyebiliriz
    column_list = ('id', 'user_id', 'cart_total')  # Gösterilecek sütunlar
    column_searchable_list = ('user_id')  # Aranabilir sütunlar

    # İlişkili OrderItem'ları göstermek için ilişki sütunu ekleyin
    column_details_list = ('items', 'items.product.name', 'items.quantity')

    column_formatters = {
        'cart_total': lambda view, context, model, name: "${:,.2f}".format(model.cart_total / 100) if model.cart_total is not None else None 
    }

    def init_search(self):
        return False