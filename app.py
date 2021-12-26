import datetime

from flask import Flask, redirect, abort, make_response, request, session, url_for, render_template, flash, Markup
from urllib.parse import urljoin, urlparse
import os, click, pymysql, wtforms, flask_wtf
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from Forms import BorrowForm, BackForm, BuyInForm, RemoveForm

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
    search = request.args.get("search")
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
    form.LdDate.render_kw.update({"value": datetime.date.today()})
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
            u = update(Equipment).where(Equipment.ENo == ENo)
            u = u.values(Status=1)
            db.session.execute(u)
            flash("登记成功")
            return redirect(url_for('index'))
        except IntegrityError:
            flash("请检查员工号是否正确！")
    return render_template("borrow.html", borrowForm=form, data=data)


@app.route("/back", methods=['GET', 'POST'])
def back():
    ENo = request.args.get("ENo")
    if ENo is None:
        flash("Invalid Path!")
        return redirect(url_for("index"))
    from models import Equipment, LendAndBcak, Stuff
    e = Equipment.query.filter(Equipment.ENo == ENo).first()
    if e is None:
        flash("invalid path")
        return redirect(url_for("index"))
    record = LendAndBcak.query.filter(LendAndBcak.ENo == ENo, LendAndBcak.BkDate == None).first()
    if record is None:
        flash("invalid path")
        return redirect(url_for("index"))
    p = Stuff.query.filter(Stuff.SNo == record.LdSNo).first()
    LdBkNo = record.LdBkNo
    data = dict()
    data["ENo"] = ENo
    data["EName"] = e.EName
    data["Norm"] = e.Norm
    data["Type"] = e.Type
    data["LdDate"] = record.LdDate
    data["ExpBkDate"] = record.ExpBkDate
    data["LdSNo"] = record.ExpBkDate
    data["LdName"] = p.Name
    form = BackForm()
    form.BkDate.render_kw.update({"value": datetime.date.today()})
    if form.submit.data and form.validate():
        # 归还
        try:
            # 保存归还登记表
            BkDate = form.BkDate.data
            BkMng = form.BkMng.data
            u = update(LendAndBcak).where(LendAndBcak.LdBkNo == LdBkNo)
            u = u.values(BkDate=BkDate, BkMng=BkMng)
            print(u)
            db.session.execute(u)
            # 修改设备状态
            u = update(Equipment).where(Equipment.ENo == ENo)
            u = u.values(Status=0)
            db.session.execute(u)
            flash("登记成功")
            return redirect(url_for('index'))
        except IntegrityError:
            flash("请检查员工号是否正确！")
    return render_template("back.html", backForm=form, data=data)


@app.route("/new_equipment", methods=['GET', 'POST'])
def equipmentAdd():
    from models import Equipment, BuyIn
    form = BuyInForm()
    form.InDate.render_kw.update({"value": datetime.date.today()})
    if form.submit.data:
        try:
            # 新建设备
            EName = form.EName.data
            Norm = form.Norm.data
            EType = form.Type.data
            Manufacture = form.Manufacture.data
            sql = "SELECT MAX(ENo) FROM equipment"
            maxIndex = db.session.execute(sql).fetchone()  # 查找ENo的最大值
            ENo = maxIndex[0] + 1
            new_equipment = Equipment(ENo, EName, Norm, EType, Manufacture, 0)
            db.session.add(new_equipment)
            db.session.commit()
            # 保存购入记录
            BDepart = form.BDepart.data
            SNoBuy = form.SNoBuy.data
            InMng = form.InMng.data
            InDate = form.InDate.data
            Fund = form.Fund.data
            BConfirm = form.BConfirm.data
            new_buyIn = BuyIn(None, ENo, BDepart, SNoBuy, InMng, InDate, Fund, BConfirm)
            db.session.add(new_buyIn)
            db.session.commit()
            flash("入库登记成功")
            return redirect(url_for("index"))
        except IntegrityError:
            flash("请检查工号是否正确")
    return render_template("buy_in.html", buyInForm=form)


@app.route("/remove_equipment", methods=['GET', 'POST'])
def equipmentRemove():
    ENo = request.args.get("ENo")
    if ENo is None:
        flash("Invalid Path!")
        return redirect(url_for("index"))
    from models import Equipment, ClearOut
    e = Equipment.query.filter(Equipment.ENo == ENo).first()
    data = dict()
    data["ENo"] = ENo
    data["EName"] = e.EName
    data["Norm"] = e.Norm
    data["Type"] = e.Type
    form = RemoveForm()
    form.ScrapDate.render_kw.update({"value": datetime.date.today()})
    if form.submit.data:
        ScrapDate = form.ScrapDate.data
        ScrapReason = form.ScrapReason.data
        SConfirm = form.SConfirm.data
        OutMng = form.OutMng.data
        try:
            # 移除设备
            sql = "DELETE FROM equipment WHERE ENo = %r" % ENo
            db.session.execute(sql)
            # 添加报废记录
            out = ClearOut(None, ENo, e.EName, e.Norm, e.Type, e.Manufacture, ScrapDate, ScrapReason, SConfirm, OutMng)
            db.session.add(out)
            db.session.commit()
            flash("报废登记成功")
            return redirect(url_for("index"))
        except IntegrityError:
            flash("请检查工号是否正确!")
    return render_template("remove.html", removeForm=form, data=data)


@app.route("/in_record")
def equipmentInRecord():
    from models import Equipment, BuyIn, Stuff
    data = []
    buyIns = BuyIn.query.filter().all()
    for i in buyIns:
        e = Equipment.query.filter(Equipment.ENo == i.ENo).one()
        buyInP = Stuff.query.filter(Stuff.SNo == i.SNoBuy).one()
        buyInMngP = Stuff.query.filter(Stuff.SNo == i.InMng).one()
        bConfirmP = Stuff.query.filter(Stuff.SNo == i.BConfirm).one()
        data.append((e, buyInP, bConfirmP, buyInMngP, i))
    return render_template("buy_in_record.html", data=data)


@app.route("/remove_record")
def equipmentRemoveRecord():
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
