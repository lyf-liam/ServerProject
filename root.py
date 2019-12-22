from .app import app
from .app import db
from flask import render_template, request, abort, redirect, session, url_for
from .model import Person


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        positions = ['技术部长', '生产部长', '采购主管', '人事行政主管', '品质主管', '车间主任', '财务主管', '总经理', '销售经理']
        return render_template('index.html', positions=positions)
    else:
        zh = request.form.get("zh")
        mm = request.form.get("mm")
        type = request.form.get("type")
        if not zh or not mm:
            return "工号、密码不能为空"
        print(zh)
        print(mm)
        print(type)
        u = Person.query.filter_by(jobNumber=zh).first()
        if u:
            if int(u.root) != int(type):
                return "该用户不存在"
            else:
                # 用户
                if u.password == mm:
                    session["jobNumber"] = zh
                    session["name"] = u.name
                    session["root"] = u.root
                    if u.root == 0:
                        return "用户"
                    else:
                        return '管理员'
                else:
                    return "密码错误"
        else:
            return "该账户不存在"


@app.route("/register", methods=['POST'])
def register():
    # 工号
    zh = request.form.get("zh")
    # 密码
    mm = request.form.get("mm")
    # 姓名
    nc = request.form.get("nc")
    # 手机号
    phone = request.form.get("phone")
    # 性别
    gender = request.form.get("gender")
    # 职位
    position = request.form.get("position")
    # 确认密码
    qrmm = request.form.get("qrmm")
    if not zh or not mm or not nc or not phone or not qrmm or not gender or not position:
        return "参数不能为空"
    if qrmm != mm:
        return "两次密码不一致"
    u = Person.query.filter_by(jobNumber=zh).first()
    if u:
        return "该工号已注册"
    else:
        u = Person(jobNumber=zh, phone=phone, position=position, password=mm, root=0,
                   name=nc, gender=int(gender))
        db.session.add(u)
        db.session.commit()
        return "注册成功"


@app.route("/logout", methods=['GET'])
def logout():
    if "jobNumber" in session:
        session.pop("jobNumber")
    login_url = url_for('login')
    return redirect(login_url)  # 重定向为登录页面
