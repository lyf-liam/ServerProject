from .app import db
from datetime import datetime


class Person(db.Model):
    # 工号
    jobNumber = db.Column(db.String(40), primary_key=True)
    # 姓名
    name = db.Column(db.String(20))
    # 手机号
    phone = db.Column(db.String(20))
    # 性别 0男 1女
    gender = db.Column(db.Integer)
    # 职位
    position = db.Column(db.String(30))
    # 以上是注册信息

    # 联系地址
    address = db.Column(db.String(50), default='')
    # 邮箱
    email = db.Column(db.String(50), default='')
    # 头像链接
    iconUrl = db.Column(db.String(80), default='http://101.37.31.180:8888/static/img/icon.jpg')
    # 密码
    password = db.Column(db.String(20))
    # 是否管理员 0否 1是
    root = db.Column(db.Integer)


class Notice(db.Model):
    # 公告Id
    ID = db.Column(db.String(40), primary_key=True)
    # 公告标题
    title = db.Column(db.String(20))
    # 公告内容
    content = db.Column(db.UnicodeText)
    # 发布时间
    createdTime = db.Column(db.DateTime, default=datetime.now, nullable=False)
