from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel

class User(Model):
    """用户表"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50,description='姓名')
    email = fields.CharField(max_length=20,description='电子邮件')
    phone = fields.CharField(max_length=20,description='电话号码')
    password = fields.CharField(max_length=200,description='密码')
    class Meta:
        table = "users"
    
class Anime(Model):
    """动漫表"""
    id = fields.IntField(pk=True, description='动漫ID')
    title = fields.CharField(max_length=255, description='标题')
    description = fields.TextField(description='描述',null=True)
    cover_image = fields.CharField(max_length=255, description='封面图片',null=True)
    rating = fields.FloatField(description='评分',null=True)
    release_date = fields.DateField(description='发布日期',null=True)
    genre = fields.CharField(max_length=100, description='类型',null=True)
    studio = fields.CharField(max_length=100, description='制作公司',null=True)
    director = fields.CharField(max_length=100, description='导演',null=True)
    characters = fields.TextField(description='人物角色',null=True)
    status = fields.CharField(max_length=50, description='播放状态',null=True)
    episodes = fields.IntField(description='集数')
    source = fields.CharField(max_length=100, description='来源',null=True)
    watch_link = fields.CharField(max_length=255, description='观看链接',null=True)
    tags = fields.TextField(description='标签',null=True)
    # directory = fields.CharField(max_length=100,description='动画储存路径',null=True)
    # video_id = fields.IntField(description='视频ID')
    # video = fields.ForeignKeyField('models.AnimeVideo',related_name='Animes',description='视频ID')

    class Meta:
        table = 'animes'

class AnimeVideo(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100,description='视频文件名')
    file_path = fields.CharField(max_length=255,description='视频存放路径')
    episode = fields.IntField(description='第几集')
    anime = fields.ForeignKeyField('models.Anime',related_name='animevideos',description='动漫id')
    class Meta:
        table = "anime_videos"

