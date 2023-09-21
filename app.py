from flask import Flask, request, render_template, make_response, redirect, Response

import models.course
import utils.jwt_token
from models.student import Student
from models.teacher import Teacher
from models.selectCousrseLog import  SelectCourseLog

app = Flask(__name__, static_url_path='')


@app.route('/')
def home():  # put application's code here
    # 鉴权
    token = request.cookies.get("token")
    account, type, errMsg = utils.jwt_token.pares_token(token)
    if errMsg != 'ok':
        return app.send_static_file('login.html')

    # 判断是否是学生，如果是学生则重定向（转到）获取学生首页的请求
    if type == 'student':
        return redirect("/student/home")

    return redirect('/teacher/home')


if __name__ == '__main__':
    app.run(debug=True)


# 执行学生注册表单提交
@app.route('/student/register', methods=["post"])
def student_register():
    # 将前端表单提交的内容付给学生对象
    stu = Student()
    stu.account = request.form.get('account')
    stu.username = request.form.get('username')
    stu.phone = request.form.get('phone')
    stu.sex = request.form.get('sex')
    stu.age = request.form.get('age')
    stu.password = request.form.get('password')
    stu.avatar = request.form.get("avatar")

    result = stu.addUser()
    if result == 'ok':
        return app.send_static_file('login.html')

    return render_template('errtoast.html', msg='注册出错，请重新输入')


# 执行教师注册提交
@app.route('/teacher/register', methods=["post"])
def teacher_register():
    # 将前端表单提交的内容付给教师对象
    teacher = Teacher()
    teacher.account = request.form.get('account')
    teacher.username = request.form.get('username')
    teacher.sex = request.form.get('sex')
    teacher.age = request.form.get('age')
    teacher.password = request.form.get('password')
    teacher.avatar = request.form.get("avatar")
    teacher.level = request.form.get("level")

    result = teacher.addTeacher()
    if result == 'ok':
        return app.send_static_file('login.html')

    return render_template('errtoast.html', msg='注册出错，请重新输入')


# 执行学生登录表单提交
@app.route("/student/login", methods=["post"])
def student_login():
    stu = Student()
    stu.account = request.form.get('account')
    stu.password = request.form.get('password')
    # 通过账号密码获取学生信息
    result = stu.getUserInfoByStuNoAndPassword()
    if result != 'ok':
        return render_template('errtoast.html', msg='账号密码出错，请重新输入')

    # 生成token
    token = utils.jwt_token.create_token(stu.account, 'student')

    # 创建一个response 对象，并将token写入到cookie
    rsp = redirect('/student/home')
    rsp.set_cookie("token", token)
    # 跳转下一个请求，学生首页的请求
    return rsp


# 进入首页之前，判断是否登录
@app.route("/student/home", methods=["get"])
def student_home():
    # 判断学生是否登录
    token = request.cookies.get("token")
    account, type, errMsg = utils.jwt_token.pares_token(token)
    if errMsg != 'ok':
        return app.send_static_file('login.html')

    # 获取待选课的课程列表
    c = models.course.Course()
    result = c.getCourseList(page=1, pageSize=10)
    return render_template('student_home.html', courseList=result)


# 教师登录
@app.route("/teacher/login", methods=["post"])
def teacher_login():
    teacher = Teacher()
    teacher.account = request.form.get('account')
    teacher.password = request.form.get('password')
    # 通过账号密码获取学生信息
    result = teacher.getTeacherInfoByAccountAndPassword()
    if result != 'ok':
        return render_template('errtoast.html', msg='账号密码出错，请重新输入')

    # 生成token
    token = utils.jwt_token.create_token(teacher.account, 'teacher')

    # 创建一个response 对象，并将token写入到cookie
    rsp = redirect('/teacher/home')
    rsp.set_cookie("token", token)
    # 跳转下一个请求，学生首页的请求
    return rsp


# 进入教师的首页之前要进行判断
@app.route("/teacher/home", methods=["get"])
def teacher_home():
    # 判断教师是否登录
    token = request.cookies.get("token")
    account, type, errMsg = utils.jwt_token.pares_token(token)
    if errMsg != 'ok':
        return app.send_static_file('login.html')

    # 获取待选课的课程列表
    c = models.course.Course()
    c.teacher_account = account
    result = c.getCourseListByTeacherAcount()
    return render_template('teacher_home.html', courseList=result)


# 退出登录
@app.route("/login/out")
def login_out():
    #  清楚cookie
    # request.cookies.clear()
    # 跳转到登录页面
    # 创建一个response 对象，并将token写入到cookie
    rsp = redirect('/')
    rsp.set_cookie("token", "")
    # 跳转下一个请求，学生首页的请求
    return rsp


# 实现创建课程的接口
@app.route("/course/add", methods=["post"])
def add_course():
    # 判断教师是否登录
    token = request.cookies.get("token")
    account, type, errMsg = utils.jwt_token.pares_token(token)
    if errMsg != 'ok':
        return app.send_static_file('login.html')
    # 判断是否是教师
    if type != 'teacher':
        return render_template("errtoast.html", msg='只有老师才能添加课程')

    c = models.course.Course()

    c.name = request.form.get("name")
    c.description = request.form.get("description")
    c.max_num = request.form.get("max_num")
    c.min_num = request.form.get("min_num")
    # 将token账号教师的值给 teacher_account
    c.teacher_account = account

    result = c.addCourse()

    if result != 0:
        return render_template("errtoast.html", msg=result)

    # 如果添加成功，则跳转到教师首页请求
    return redirect("/teacher/home")

# 选课接口
@app.route("/course/select",methods=["post"])
def select_course():
    # 鉴权
    token = request.cookies.get("token")
    account, type ,errMsg = utils.jwt_token.pares_token(token)
    if errMsg != 'ok' :
        return app.send_static_file('login.html')

    if type != 'student':
        return render_template('errtoast.html',msg='只有学生身份才能选课')

    sC = models.selectCousrseLog.SelectCourseLog()
    sC.course_id = request.form.get("cousrse_id")
    sC.stu_no = account
    result = sC.addSelectCourseLog()
    if result != "ok":
        return render_template('errtoast.html', msg=result)
    return redirect('/student/home')


# 选课接口
@app.route("/course/exit",methods=["post"])
def exit_course():
    # 鉴权
    token = request.cookies.get("token")
    account, type ,errMsg = utils.jwt_token.pares_token(token)
    if errMsg != 'ok' :
        return app.send_static_file('login.html')

    if type != 'student':
        return render_template('errtoast.html',msg='只有学生身份才能选课')

    sC = models.selectCousrseLog.SelectCourseLog()
    sC.course_id = request.form.get("cousrse_id")
    sC.stu_no = account
    result = sC.deleteCourseLog()
    if result != "ok":
        return render_template('errtoast.html', msg=result)
    return redirect('/student/home')


# 获取学生自己的选课列表
@app.route("/student/course/list")
def get_student_course_list():
    # 鉴权
    token = request.cookies.get("token")
    account, type, errMsg = utils.jwt_token.pares_token(token)
    if errMsg != 'ok':
        return app.send_static_file('login.html')

    if type != 'student':
        return render_template('errtoast.html', msg='只有学生身份才能查看自己的课程列表')

    result = models.selectCousrseLog.getStudentSelectCourseList(account)

    return render_template('student_course_list.html',courseList=result)


# 获取某个课程的学生列表
@app.route("/course/student/list")
def get_course_student_list():
    # 鉴权
    token = request.cookies.get("token")
    account, type, errMsg = utils.jwt_token.pares_token(token)
    if errMsg != 'ok':
        return app.send_static_file('login.html')
    # get 参数获取用 args
    courseID = request.args.get("course_id")
    result = models.selectCousrseLog.getStudentListByCourseId(courseID)

    return render_template('course_student_list.html',studentList=result)
