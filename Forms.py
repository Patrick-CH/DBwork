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


class BackForm(FlaskForm):
    BkDate = DateField('归还日期', validators=[DataRequired()], render_kw={"type": "date"})
    BkMng = IntegerField('归还管理员', validators=[DataRequired()])
    submit = SubmitField("确认归库")


class BuyInForm(FlaskForm):
    BDepart = StringField('购入部门', validators=[DataRequired()])
    SNoBuy = StringField('采购人工号', validators=[DataRequired()])
    InMng = StringField('管理员工号', validators=[DataRequired()])
    InDate = DateField('购入日期', validators=[DataRequired()], render_kw={"type": "date"})
    Fund = StringField('资金来源', validators=[DataRequired()])
    BConfirm = StringField('采购批准人', validators=[DataRequired()])
    EName = StringField('设备名称', validators=[DataRequired()])
    Norm = StringField('设备标准', validators=[DataRequired()])
    Type = StringField('设备类型', validators=[DataRequired()])
    Manufacture = StringField('制造商', validators=[DataRequired()])
    submit = SubmitField('提交')


class RemoveForm(FlaskForm):
    ScrapDate = DateField('报废日期', validators=[DataRequired()], render_kw={"type": "date"})
    ScrapReason = StringField('报废原因', validators=[DataRequired()])
    SConfirm = IntegerField('报废批准人工号', validators=[DataRequired()])
    OutMng = IntegerField('报废管理员工号', validators=[DataRequired()])
    submit = SubmitField('确认报废', validators=[DataRequired()])
