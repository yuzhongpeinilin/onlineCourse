import utils.mysqldb


class Student:
    def __int__(self):
        self.account = ''
        self.username = ''
        self.phone = ''
        self.age = 0
        self.sex = 0
        self.avatar = ''
        self.password = ''

    # 通过学号获取用户详情
    def getUserInfoByStuNo(self):
        sql = 'select stu_no,username, phone,age,sex,avatar from student where stu_no = %s'
        v = (self.account,)
        utils.mysqldb.myCursor.execute(sql, v)
        result = utils.mysqldb.myCursor.fetchall()
        if len(result) == 0:
            return '找不到结果'

        item = result[0]
        # 把item 元祖赋予 当前对象
        self.account = item[0]
        self.username = item[1]
        self.phone = item[2]
        self.age = item[3]
        self.sex = item[4]
        self.avatar = item[5]
        return 'ok'

    # 填加用户
    def addUser(self):
        sql = 'insert into student(stu_no,username,phone,age,sex,avatar,password) values (%s,%s,%s,%s,%s,%s,%s)'
        v = (self.account, self.username, self.phone, self.age, self.sex, self.avatar, self.password)
        try:
            utils.mysqldb.myCursor.execute(sql, v)
            utils.mysqldb.mydb.commit()
        except:
            return '添加错误'

        return 'ok'

    # 通过学号和密码获取用户详情
    def getUserInfoByStuNoAndPassword(self):
        sql = 'select stu_no,username, phone,age,sex,avatar from student where stu_no = %s and password = %s'
        v = (self.account,self.password)
        utils.mysqldb.myCursor.execute(sql, v)
        result = utils.mysqldb.myCursor.fetchall()
        if len(result) == 0:
            return '找不到结果'

        item = result[0]
        # 把item 元祖赋予 当前对象
        self.account = item[0]
        self.username = item[1]
        self.phone = item[2]
        self.age = item[3]
        self.sex = item[4]
        self.avatar = item[5]
        return 'ok'
