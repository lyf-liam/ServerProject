from .app import app
from .app import db
from flask import render_template, request, abort, redirect, session, url_for, jsonify
from .model import Person, Notice
import time


@app.route("/manageNotice", methods=['GET'])
def manageNotice():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 0:
        return redirect('/')  # 重定向为登录页面
    page = request.args.get("page")
    if not page:
        page = 1
    page = int(page)
    key_title = request.args.get("title")
    if not key_title:
        key_title = ''
    paginate = Notice.query.filter(Notice.title.like("%" + key_title + "%")).paginate(
        page=page, per_page=3)
    return render_template('manageNotice.html', name=session["name"], nav='notice'
                           , paginate=paginate, key_title=key_title)


@app.route("/managePerson", methods=['GET'])
def managePerson():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 0:
        return redirect('/')  # 重定向为登录页面
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
    paginate = Person.query.filter(Person.name.like("%" + key_name + "%"),
                                   Person.jobNumber.like(
                                       "%" + key_job_number + "%")).paginate(
        page=page, per_page=3)
    return render_template('managePerson.html', name=session["name"], nav='home'
                           , paginate=paginate, key_name=key_name, key_job_number=key_job_number)


@app.route("/deletePerson", methods=['GET'])
def deletePerson():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 0:
        return redirect('/')  # 重定向为登录页面
    job_number = request.args.get("jobNumber")
    if job_number:
        u = Person.query.filter_by(jobNumber=job_number).first()
        db.session.delete(u)
        db.session.commit()

    return redirect('/managePerson')


@app.route("/managePwd", methods=['PosT'])
def manage_pwd():
    zh = request.form.get("zh")
    mm = request.form.get("password")
    if not mm:
        return "参数不能为空"
    u = Person.query.filter_by(jobNumber=zh).first()
    if not u:
        return '该工号不存在'
    u.password = mm
    db.session.add(u)
    db.session.commit()
    return 'ok'


@app.route("/rootNoticeSee", methods=['GET'])
def rootNoticeSee():
    if "jobNumber" not in session:
        return redirect('/login')  # 重定向为登录页面
    if session["root"] == 0:
        return redirect('/')
    id = request.args.get("id")
    if not id:
        return redirect('/manageNotice')
    u = Notice.query.filter_by(ID=id).first()
    return render_template('rootNoticeSee.html', name=session["name"], notice=u)


@app.route("/manageAddNotice", methods=['GET', 'PosT'])
def manage_add_notice():
    if "jobNumber" not in session:
        login_url = url_for('login')
        return redirect(login_url)  # 重定向为登录页面
    if session["root"] == 0:
        return redirect('/')  # 重定向为登录页面

    if request.method == 'GET':
        return render_template('manageAddNotice.html', jobNumber=session["jobNumber"], name=session["name"])
    else:
        # 标题
        title = request.form.get("title")
        # 内容
        content = request.form.get('ckeditor')

        if not title or not content:
            return render_template('manageAddNotice.html', jobNumber=session["jobNumber"], name=session["name"],
                                   tip='参数不能为空')
        p_id = 'notice' + str(int(time.time() * 1000))
        u = Notice(ID=p_id, title=title, content=content)
        db.session.add(u)
        db.session.commit()
        # 发布操作
        return render_template('manageAddNotice.html', jobNumber=session["jobNumber"], name=session["name"],
                               tip='发布成功')


@app.route("/managePersonInfo", methods=['GET', 'PosT'])
def manage_person_info():
    if "jobNumber" not in session:
        login_url = url_for('login')
        return redirect(login_url)  # 重定向为登录页面
    if session["root"] == 0:
        return redirect('/')  # 重定向为登录页面

    job_number = request.args.get("jobNumber")
    if not job_number:
        return redirect('/managePerson')
    positions = ['技术部长', '生产部长', '采购主管', '人事行政主管', '品质主管', '车间主任', '财务主管', '总经理', '销售经理']
    if request.method == 'GET':
        u = Person.query.filter_by(jobNumber=job_number).first()
        return render_template('managePersonInfo.html', u=u, jobNumber=session["jobNumber"], name=session["name"],
                               positions=positions)
    else:
        # 工号
        zh = request.form.get("zh")
        # 姓名
        nc = request.form.get("nc")
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
        u = Person.query.filter_by(jobNumber=zh).first()
        if not nc or not phone or not address or not email:
            return render_template('managePersonInfo.html', u=u, jobNumber=session["jobNumber"], name=session["name"],
                                   positions=positions, tip='参数不能为空')
        u.name = nc
        u.phone = phone
        u.gender = gender
        u.position = position
        u.address = address
        u.email = email
        db.session.add(u)
        db.session.commit()

        return redirect('/managePerson')  # 重定向为主页


@app.route("/manageAddPerson", methods=['GET', 'PosT'])
def manage_add_person():
    if "jobNumber" not in session:
        login_url = url_for('login')
        return redirect(login_url)  # 重定向为登录页面
    if session["root"] == 0:
        return redirect('/')  # 重定向为登录页面
    positions = ['技术部长', '生产部长', '采购主管', '人事行政主管', '品质主管', '车间主任', '财务主管', '总经理', '销售经理']
    if request.method == 'GET':

        return render_template('manageAddPerson.html', jobNumber=session["jobNumber"], name=session["name"],
                               positions=positions)
    else:
        # 工号
        zh = request.form.get("zh")
        # 姓名
        nc = request.form.get("nc")
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
        # 密码
        mm = request.form.get("mm")

        if not zh or not nc or not phone or not address or not email or not mm:
            return render_template('manageAddPerson.html', jobNumber=session["jobNumber"], name=session["name"],
                                   positions=positions, tip='参数不能为空')
        u = Person.query.filter_by(jobNumber=zh).first()
        if u:
            return render_template('manageAddPerson.html', jobNumber=session["jobNumber"], name=session["name"],
                                   positions=positions, tip='该员工号已存在')
        else:
            u = Person(jobNumber=zh, phone=phone, position=position, address=address, email=email, password=mm, root=0,
                       name=nc, gender=int(gender))
            db.session.add(u)
            db.session.commit()

        return render_template('manageAddPerson.html', jobNumber=session["jobNumber"], name=session["name"],
                               positions=positions, tip='注册成功：' + '工号' + zh + ',姓名：' + nc + ',密码：' + mm)
