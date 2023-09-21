import datetime

import utils.mysqldb



class Course:
    def __int__(self):
        self.id = 0
        self.name = ''
        self.description = ''
        self.teacher_account = ''
        self.max_num = 0
        self.min_num = 0
        self.create_t = datetime.datetime.now()
        self.update_t = datetime.datetime.now()

    # 添加课程
    def addCourse(self):
        sql = 'insert into course(name,description,teacher_account,max_num,min_mun) values (%s,%s,%s,%s,%s)'
        v = (self.name,self.description,self.teacher_account,self.max_num,self.min_num)

        try:
            utils.mysqldb.myCursor.execute(sql,v)
            utils.mysqldb.mydb.commit()
        except:
            return '添加课程错误'

        return 'ok'

    # 分页获取课程列表
    def getCourseList(self,page=0,pageSize=0):
        sql = 'select id ,name,description,teacher_account,max_num,min_mun, create_t,update_t from course order by create_t desc limit %s,%s'
        start = (page-1)*pageSize
        v = (start,pageSize)
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
            c.create_t = item[6]
            c.update_t = item[7]
            courseList.append(c)

        return courseList

    # 通过课程id获取课程详情的方法
    def getCourseInfoById(self):

        sql = 'select id,name,description,teacher_account,max_num,min_mun,create_t,update_t from course where id = %s'

        v = (self.id,)
        utils.mysqldb.myCursor.execute(sql,v)

        result = utils.mysqldb.myCursor.fetchall()

        if len(result) == 0:
            return '不存在'

        item = result[0]
        self.id = item[0]
        self.name = item[1]
        self.description = item[2]
        self.teacher_account = item[3]
        self.max_num = item[4]
        self.min_num = item[5]
        self.create_t = item[6]
        self.update_t = item[7]

        return 'ok'

    # 通过教师账号获取课程列表
    def getCourseListByTeacherAcount(self):
        sql = 'select id ,name,description,teacher_account,max_num,min_mun, create_t,update_t from course where teacher_account = %s order by create_t desc'
        v = (self.teacher_account,)
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
            c.create_t = item[6]
            c.update_t = item[7]
            courseList.append(c)

        return courseList


# 类：对有某些共同特征的事物抽象概括
# {
#     第一：属性：
#     第二：活动（方法）
# }


# 对象：给某类赋予特定值后产生的结果
#  类的实例化就是对象的生









