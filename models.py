import datetime

from app import db


class Stuff(db.Model):
    __tablename__ = "stuff"
    SNo = db.Column(db.Integer(), primary_key=True)
    Name = db.Column(db.String(20))
    Department = db.Column(db.String(20))
    Phone = db.Column(db.String(20))

    def __init__(self, SNo, Name, Department, Phone):
        self.SNo = SNo
        self.Name = Name
        self.Department = Department
        self.Phone = Phone

    def __repr__(self):
        return '<Stuff %r>' % self.Name


class Equipment(db.Model):
    __tablename__ = "equipment"
    ENo = db.Column(db.Integer, primary_key=True)
    EName = db.Column(db.String(20))
    Norm = db.Column(db.String(20))
    Type = db.Column(db.String(20))
    Manufacture = db.Column(db.String(20))
    Status = db.Column(db.String(20))

    def __init__(self, ENo, EName, Norm, Type, Manufacture, status):
        self.ENo = ENo
        self.EName = EName
        self.Norm = Norm
        self.Type = Type
        self.Manufacture = Manufacture
        self.Status = status

    def __repr__(self):
        return '<Equipment %r>' % self.EName


class LendAndBcak(db.Model):
    __tablename__ = "lendandback"
    LdBkNo = db.Column(db.Integer, primary_key=True)
    ENo = db.Column(db.Integer())
    LdDate = db.Column(db.Date())
    ExpBkDate = db.Column(db.Date())
    LdSNo = db.Column(db.Integer())
    LdConfirm = db.Column(db.Integer())
    LdMng = db.Column(db.Integer())
    BkDate = db.Column(db.Integer())
    BkMng = db.Column(db.Integer())

    def __init__(self, LdBkNo, ENo, LdDate, ExpBkDate, LdSNo, LdConfirm, LdMng, BkDate, BkMng):
        self.LdBkNo = LdBkNo
        self.ENo = ENo
        self.LdDate = LdDate
        self.ExpBkDate = ExpBkDate
        self.LdSNo = LdSNo
        self.LdConfirm = LdConfirm
        self.LdMng = LdMng
        self.BkDate = BkDate
        self.BkMng = BkMng

    def __repr__(self):
        return '<LendAndBk %r>' % self.LdBkNo


class BuyIn(db.Model):
    __tablename__ = "buyin"
    InNo = db.Column(db.Integer(), primary_key=True)
    ENo = db.Column(db.Integer())
    BDepart = db.Column(db.String())
    SNoBuy = db.Column(db.Integer())
    InMng = db.Column(db.Integer())
    InDate = db.Column(db.Date())
    Fund = db.Column(db.String(20))
    BConfirm = db.Column(db.Integer())

    def __init__(self, InNo, ENo, BDepart, SNoBuy, InMng, InDate, Fund, BConfirm):
        self.InNo = InNo
        self.ENo = ENo
        self.BDepart = BDepart
        self.SNoBuy = SNoBuy
        self.InMng = InMng
        self.InDate = InDate
        self.Fund = Fund
        self.BConfirm = BConfirm

    def __repr__(self):
        return "<BuyIn %r>" % self.InNo


class ClearOut(db.Model):
    __tablename__ = "clearout"
    OutNo = db.Column(db.Integer, primary_key=True)
    ENo = db.Column(db.Integer, primary_key=True)
    EName = db.Column(db.String(20))
    Norm = db.Column(db.String(20))
    Type = db.Column(db.String(20))
    Manufacture = db.Column(db.String(20))
    ScrapDate = db.Column(db.Date())
    ScrapReason = db.Column(db.String(30))
    SConfirm = db.Column(db.Integer())
    OutMng = db.Column(db.Integer())

    def __init__(self, OutNo, ENo, EName, Norm, Type, Manufacture, ScrapDate, ScrapReason, SConfirm, OutMng):
        self.OutNo = OutNo
        self.ENo = ENo
        self.EName = EName
        self.Norm = Norm
        self.Type = Type
        self.Manufacture =Manufacture
        self.ScrapDate = ScrapDate
        self.ScrapReason = ScrapReason
        self.SConfirm = SConfirm
        self.OutMng = OutMng

    def __repr__(self):
        return "<Scrap %r>" % self.OutNo


if __name__ == '__main__':
    ls = BuyIn.query.filter().all()
    print(ls)
    # ls = LendAndBcak.query.filter().all()
    # newLd = LendAndBcak(None, 2, datetime.date.today(), datetime.date.today(), 5, 6, 7, None, None)
    # for i in ls:
    #     print(i.LdDate)
    #     print(type(i.LdDate))
    # print(ls)
    # print(datetime.date.today())
    # from sqlalchemy import update
    # u = update(Equipment).where(Equipment.ENo == 1)
    # u = u.values(Status=1)
    # print(u)
