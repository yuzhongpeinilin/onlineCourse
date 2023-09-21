import utils.mysqldb


class Teacher:

    def __int__(self):
        self.account = ''
        self.username = ''
        self.age = 0
        self.level = 0
        self.avatar = ''
        self.sex = 0
        self.password = ''

    # 添加教师
    def addTeacher(self):
        sql = 'insert into teacher(account,username,age,level,avatar,sex,password) values (%s,%s,%s,%s,%s,%s,%s)'
        v = (self.account, self.username, self.age, self.level, self.avatar, self.sex, self.password)
        try:
            utils.mysqldb.myCursor.execute(sql, v)
            utils.mysqldb.mydb.commit()
        except:
            return '添加错误'

        return 'ok'

    # 通过账号和密码获取教师信息
    def getTeacherInfoByAccountAndPassword(self):
        sql = 'select account,username,age,level,sex,avatar from teacher where account = %s and password = %s'
        v = (self.account, self.password)

        utils.mysqldb.myCursor.execute(sql, v)
        result = utils.mysqldb.myCursor.fetchall()
        if len(result) == 0:
            return '找不到结果'

        item = result[0]
        # 把item 元祖赋予 当前对象
        self.account = item[0]
        self.username = item[1]
        self.age = item[2]
        self.level = item[3]
        self.sex = item[4]
        self.avatar = item[5]
        return 'ok'


