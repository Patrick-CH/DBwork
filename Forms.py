from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL


class BorrowForm(FlaskForm):
    LdDate = DateField('借出日期', validators=[DataRequired()], render_kw={"type": "date"})
    ExpBkDate = DateField('预期归还日期', validators=[DataRequired()], render_kw={"type": "date"})
    LdSNo = IntegerField('借出人工号', validators=[DataRequired()])
    LdConfirm = IntegerField('借出批准人工号', validators=[DataRequired()])
    LdMng = IntegerField('借出管理员', validators=[DataRequired()])
    submit = SubmitField('登记')
