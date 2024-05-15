from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductForm(FlaskForm):
    """
    Form for admin to add or edit a product.
    """
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    category_id = IntegerField('Category ID', validators=[Optional()])
    brand = StringField('Brand', validators=[Length(max=100)])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    color = StringField('Color', validators=[Length(max=50)])
    size = StringField('Size', validators=[Length(max=50)])
    weight = FloatField('Weight', validators=[Optional(), NumberRange(min=0)])
    is_active = BooleanField('Is Active')
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    """
    Form for users to search for products.
    """
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')