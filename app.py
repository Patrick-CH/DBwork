from flask import Flask, redirect, abort, make_response, request, session, url_for, render_template, flash, Markup
from urllib.parse import urljoin, urlparse
import os, click, pymysql, wtforms, flask_wtf
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from Forms import BorrowForm

from DB_URI import DB_RUI

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
# set your db uri here like "mysql://<user>:<password>@localhost/<database>"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_RUI
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# print(app.config)
db = SQLAlchemy(app)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    """

    :param default: 获取信息失败时的返回值
    :param kwargs: 可选参数，作用同上
    :return: 重定向到上一个界面，如过无法获取上一个界面则返回default
    """
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.cli.command()
def initdb():
    # db.drop_all()
    db.create_all()
    click.echo("Initialized database")


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/stuff")
def stuffList():
    from models import Stuff
    ls = Stuff.query.all()
    return render_template("stuff.html", stuff_list=ls)


@app.route("/equipment_available")
def equipmentListAvailable():
    from models import Equipment
    search = request.args.get("search")
    ls = Equipment.query.filter(Equipment.Status == 0)
    if search == "true":
        name = request.args.get("name")
        norm = request.args.get("norm")
        eType = request.args.get("type")
        manufacture = request.args.get("manufacture")
        if name is not None:
            ls = ls.filter(Equipment.EName.like(f"%{name}%"))
        if norm is not None:
            ls = ls.filter(Equipment.Norm.like(f"%{norm}%"))
        if eType is not None:
            ls = ls.filter(Equipment.Type.like(f"%{eType}%"))
        if manufacture is not None:
            ls = ls.filter(Equipment.Manufacture.like(f"%{manufacture}%"))
    return render_template("equipment.html", equipment_list=ls, borrow=True)


@app.route("/equipment_out")
def equipmentListOut():
    from models import Equipment
    ls = Equipment.query.filter(Equipment.Status == 1)
    return render_template("equipment.html", equipment_list=ls, back=True)


@app.route("/borrow", methods=['GET', 'POST'])
def borrow():
    ENo = request.args.get("ENo")
    if ENo is None:
        flash("Invalid Path!")
        return redirect(url_for("index"))
    from models import Equipment, LendAndBcak
    e = Equipment.query.filter(Equipment.ENo == ENo).first()
    data = dict()
    data["ENo"] = ENo
    data["EName"] = e.EName
    data["Norm"] = e.Norm
    data["Type"] = e.Type
    form = BorrowForm()
    if form.submit.data and form.validate():
        # 借出设备
        LdDate = form.LdDate.data
        ExpBkDate = form.ExpBkDate.data
        LdSNo = form.LdSNo.data
        LdConfirm = form.LdConfirm.data
        LdMng = form.LdMng.data
        newLd = LendAndBcak(LdBkNo=None, ENo=ENo, LdDate=LdDate, ExpBkDate=ExpBkDate, LdSNo=LdSNo, LdConfirm=LdConfirm,
                            LdMng=LdMng, BkDate=None, BkMng=None)
        try:
            # 保存借出登记表
            db.session.add(newLd)
            db.session.commit()
            # 修改设备状态
            u = update(Equipment).where(Equipment.ENo == 1)
            u = u.values(Status=1)
            db.session.execute(u)
            flash("登记成功")
            return redirect(url_for('index'))
        except IntegrityError:
            flash("请检查员工号是否正确！")
    return render_template("borrow.html", borrowForm=form, data=data)


@app.route("/back", methods=['GET', 'POST'])
def back():
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
