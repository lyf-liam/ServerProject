from .app import app
from .app import db
from flask import render_template, request, abort, redirect, session, url_for, jsonify
from .model import Person, Notice
import os, time

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload_cover', methods=['POST'])  # 添加路由
def upload():
    img = request.files['cover']
    if not img:
        return jsonify({"status": 'error', "msg": "数据不能为空"})
    if not (img and allowed_file(img.filename)):
        return jsonify({"status": 'error', "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
    img_id = str(int(time.time() * 1000))
    img.save(os.path.join(app.root_path, "static/img/staff_") + img_id + ".jpg")
    img_url = "http://101.37.31.180:8888/static/img/staff_" + img_id + ".jpg"
    u = Person.query.filter_by(jobNumber=session["jobNumber"]).first()
    u.iconUrl = img_url
    db.session.add(u)
    db.session.commit()
    return jsonify({"status": 'ok', "url": img_url})


@app.route("/userNoticeSee", methods=['GET'])
def userNoticeSee():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 1:
        return redirect('/managePerson')
    id = request.args.get("id")
    if not id:
        return redirect('/notice')
    u = Notice.query.filter_by(ID=id).first()
    return render_template('userNoticeSee.html', name=session["name"], notice=u)


@app.route("/notice", methods=['GET'])
def notice():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 1:
        return redirect('/managePerson')
    page = request.args.get("page")
    if not page:
        page = 1
    page = int(page)

    paginate = Notice.query.filter().paginate(
        page=page, per_page=3)
    return render_template('notice.html', name=session["name"], nav='notice'
                           , paginate=paginate)


@app.route("/", methods=['GET'])
def home():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 1:
        return redirect('/managePerson')
    u = Person.query.filter_by(jobNumber=session["jobNumber"]).first()
    return render_template('userInfo.html', u=u, jobNumber=session["jobNumber"], name=session["name"], nav='home')


@app.route("/searchPerson", methods=['GET'])
def searchPerson():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 1:
        return redirect('/managePerson')
    page = request.args.get("page")
    if not page:
        page = 1
    page = int(page)
    key_name = request.args.get("name")
    key_job_number = request.args.get("jobNumber")
    if not key_name:
        key_name = ''
    if not key_job_number:
        key_job_number = ''
    u = Person.query.filter_by(jobNumber=session["jobNumber"]).first()
    paginate = Person.query.filter(Person.name.like("%" + key_name + "%"),
                                   Person.jobNumber.like(
                                       "%" + key_job_number + "%")).paginate(
        page=page, per_page=3)
    return render_template('searchPerson.html', u=u, jobNumber=session["jobNumber"], name=session["name"],
                           nav='searchPerson'
                           , paginate=paginate, key_name=key_name, key_job_number=key_job_number)


@app.route("/updatePwd", methods=['GET', 'PosT'])
def update_pwd():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 1:
        return redirect('/managePerson')
    if request.method == 'GET':
        return render_template('updatePwd.html', jobNumber=session["jobNumber"], name=session["name"])
    else:
        mm = request.form.get("mm")
        xmm = request.form.get("xmm")
        qrmm = request.form.get("qrmm")
        tip = ''
        if not mm or not xmm or not qrmm:
            tip = "参数不能为空"
            return render_template('updatePwd.html', jobNumber=session["jobNumber"], name=session["name"], tip=tip)
        if qrmm != xmm:
            tip = "两次密码不一致"
            return render_template('updatePwd.html', jobNumber=session["jobNumber"], name=session["name"], tip=tip)
        u = Person.query.filter_by(jobNumber=session["jobNumber"]).first()
        if u.password == mm:
            u.password = xmm
            db.session.add(u)
            db.session.commit()
            session.pop("jobNumber")
            return redirect('/login')  # 重定向为登录页面
        else:
            tip = "旧密码错误"
        return render_template('updatePwd.html', jobNumber=session["jobNumber"], name=session["name"], tip=tip)


@app.route("/updateInfo", methods=['GET', 'PosT'])
def update_info():
    if "jobNumber" not in session:
        login_url = url_for('login')
        return redirect(login_url)  # 重定向为登录页面
    if session["root"] == 1:
        return redirect('/managePerson')
    positions = ['技术部长', '生产部长', '采购主管', '人事行政主管', '品质主管', '车间主任', '财务主管', '总经理', '销售经理']
    if request.method == 'GET':
        u = Person.query.filter_by(jobNumber=session["jobNumber"]).first()
        return render_template('updateInfo.html', u=u, jobNumber=session["jobNumber"], name=session["name"],
                               positions=positions)
    else:
        if "jobNumber" not in session:
            return redirect('/login')  # 重定向为登录页面
        # 工号
        # zh = request.form.get("zh")
        # 姓名
        # nc = request.form.get("nc")
        # 手机号
        phone = request.form.get("phone")
        # 性别
        gender = request.form.get("gender")
        # 职位
        position = request.form.get("position")
        # 地址
        address = request.form.get("address")
        # 邮箱
        email = request.form.get("email")
        u = Person.query.filter_by(jobNumber=session["jobNumber"]).first()
        if not phone or not address or not email:
            return render_template('updateInfo.html', u=u, jobNumber=session["jobNumber"], name=session["name"],
                                   positions=positions, tip='参数不能为空')

        u.phone = phone
        u.gender = gender

        u.position = position
        u.address = address
        u.email = email
        db.session.add(u)
        db.session.commit()

        return redirect('/')  # 重定向为主页
