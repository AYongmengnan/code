from typing import List
from fastapi import APIRouter, Request
from pydantic import BaseModel
from models import Course, Student
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
student = APIRouter()


# # 查看所有学生数据
# @student.get('/')
# async def get_all_student():
#     # 查询所有 all
#     # students = await Student.all() # QuerySet: [Student(),Student(),Student(),Student(),Student()···] QuerySet是一个数据类型，类似list
#     # # print(students)
#     # for stu in students:
#     #     print(stu.name,stu.sno)
    
#     # 过滤查询 filter
#     # students = await Student.filter(sno__gt=2001) #[<Student: 2>, <Student: 3>, <Student: 4>, <Student: 5>] 
#     # students = await Student.filter(sno__in=[2001,2002]) # [<Student: 1>, <Student: 2>]

#     # values 
#     students = await Student.all().values('id','name','sno','age','classs_id')
#     print(students)
#     return {
#         'students':students}

# # 查看一个学生的数据
# @student.get('/{student_id}')
# async def get_student(student_id:int):

#     return {
#         f'result':f'{student_id}student info'
#     }

# # 创建一个学生
# @student.post('/')
# async def post_student():

#     return {
#         'result':'create student'
#     }

# # 修改学生信息
# @student.put('/{student_id}')
# async def update_student(student_id:int):

#     return {
#         'result':f'update student {student_id}'
#     }

# # 删除学生
# @student.delete('/{student_id}')
# async def delete_student(student_id:int):
#     return {
#         'result':f'delete {student_id} student'
#     }

@student.get('/index')
async def get_student1(request:Request):
    templates = Jinja2Templates(directory='fastapi/09_orm/templates')
    students = await Student.all()
    return {'message':students}
    # return templates.TemplateResponse(
    #     'index.html',
    #     {
    #         'request':request,
    #         'students':students
    #     }
    # )

class create_student(BaseModel):
    name:str
    # pwd:str
    sno:int
    age:int
    classs_id:int
    course:List[int]=[]

@student.post('/')
async def create(student_in:create_student):
    # 插入数据
    # 方式1
    # stu = Student(name=student_in.name,
    #             #   pwd=create_student.pwd,
    #               sno=student_in.sno,
    #               age=student_in.age,
    #               classs_id=student_in.classs_id
    #               )
    # await stu.save()
    stu = await Student.create(name=student_in.name,
                                sno=student_in.sno,
                                age=student_in.age,
                                classs_id=student_in.classs_id)
    return {
        'message':stu
    }

@student.get('/')
async def get_student():
    # 一对多查询
        # 单个对象查询
    # xianzun = await Student.get(name='星宿仙尊')
    # print(xianzun.age)
    # print(await xianzun.classs.values())
    # return xianzun
    
        # 多个对象查询
    # students = await Student.all().values('name','classs__name')
    # print(students)
    # return students


    # 多对多查询 
        # 单个对象查询
    # xianzun = await Student.get(name='星宿仙尊')
    # res = await xianzun.course.all().values('name','teacher__name')
    # print(res)
    # return res
        # 多个对象查询
    students = await Student.all().values('name','course__name')
    print(students)
    return students

@student.get('/{student_id}')
async def get_student(student_id:int):
    result = await Student.get(id=student_id)
    return result


@student.put('/{student_id}')
async def update_student(student_id:int,student_in:create_student):
    data = student_in.dict()
    course = data.pop('course')
    new_course = await Course.filter(id__in=course)
    result = await Student.filter(id=student_id).update(**data)
    # 设置多对多的课程
    edit_stu = await Student.get(id=student_id)
    await edit_stu.course.clear() # 删除多对多原课程关系
    await edit_stu.course.add(*new_course) # 新增多对多课程关系
    return result

@student.delete('/{student_id}')
async def delete_student(student_id:int):
    result = await Student.filter(id=student_id).delete()
    if not result:
        raise HTTPException(status_code=404,detail=f'ID为:{student_id}的学生不存在。')
    return {"message":'delete sucesse'}