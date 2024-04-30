from tortoise.models import Model
from tortoise import fields

class Student(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50,description='姓名')
    sno = fields.IntField(description='学号')
    age = fields.IntField(description='年龄')

    # 一对多
    classs = fields.ForeignKeyField('models.Classs',related_name='stutents')

    # 多对多
    course = fields.ManyToManyField('models.Course',related_name='stutents')
    teacher = fields.ManyToManyField('models.Teacher',related_name='stutents')

class Classs(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20,description='班级名称')
    
class Course(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100,description='课程名称')
    teacher = fields.ForeignKeyField('models.Teacher')
    addr = fields.CharField(max_length=50,description='教室',default='')

class Teacher(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100,description='姓名')
    pwd = fields.CharField(max_length=100,description='密码')
    tno = fields.IntField(description='老师编号')