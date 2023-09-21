import datetime

import models.student
import utils.mysqldb
from models.course import Course


class SelectCourseLog:
    def __int__(self):
        self.id = 0
        self.stu_no = ''
        self.course_id = 0
        self.create_t = datetime.datetime.now()
        self.update_t = datetime.datetime.now()


    # 添加选课记录
    def addSelectCourseLog(self):
        sql = 'insert into select_course_log(stu_no,course_id) values (%s,%s)'
        v = (self.stu_no,self.course_id)
        try:
            utils.mysqldb.myCursor.execute(sql,v)
            utils.mysqldb.mydb.commit()
        except:
            return '添加错误'
        return 'ok'

    def deleteCourseLog(self):
        sql = 'delete from select_course_log where stu_no = %s and course_id = %s'
        v = (self.stu_no,self.course_id)
        try:
            utils.mysqldb.myCursor.execute(sql,v)
            utils.mysqldb.mydb.commit()
        except:
            return '删除错误'
        return 'ok'



# 通过学号查询自己选的课程信息
def getStudentSelectCourseList(stu_no):

    # 联合子查询，先查出这个学生选择的课程id，再从课程信息表中查询将这些id课程信息
    sql = 'select id,name,description,teacher_account,max_num,min_mun from course where id in (select course_id from select_course_log where stu_no = %s)'
    v = (stu_no,)
    utils.mysqldb.myCursor.execute(sql,v)

    result = utils.mysqldb.myCursor.fetchall()

    courseList = []

    for item in result:
        c = Course()
        c.id = item[0]
        c.name = item[1]
        c.description = item[2]
        c.teacher_account = item[3]
        c.max_num = item[4]
        c.min_num = item[5]
        courseList.append(c)

    return courseList

# 获取某个课程的学生列表
def getStudentListByCourseId(courseId):
    # 第一步 我们得先在选课记录表里查询选了这个课程的学生id select stu_no from select_course_log where course_id = %s
    # 从学生表里，通过学生id找出学生的详情 select stu_no,username,phone,age,sex,avatar from student where stu_no in (从第一步获取的学号列表)
    sql = 'select stu_no,username,phone,age,sex,avatar from student where stu_no in (select stu_no from select_course_log where course_id = %s)'
    v = (courseId,)
    utils.mysqldb.myCursor.execute(sql, v)

    result = utils.mysqldb.myCursor.fetchall()
    stuList = []
    for item in result:
        stu = models.student.Student()
        stu.account = item[0]
        stu.username = item[1]
        stu.phone = item[2]
        stu.age = item[3]
        stu.sex = item[4]
        stu.avatar = item[5]

        stuList.append(stu)

    return stuList


