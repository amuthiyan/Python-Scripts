from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(Form):
    userid = StringField('openid',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember_me',default=False)

class Register(Form):
    userid = StringField('openid',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired(),
                                                    EqualTo('confirm',message='Passwords must match')])
    confirm = PasswordField('password',validators=[DataRequired()])
