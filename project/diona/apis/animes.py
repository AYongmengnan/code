import hashlib
import os
import time
from fastapi import APIRouter, HTTPException, status, Depends,Request,UploadFile, File,Query
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import HTTPNotFoundError
from models import Anime,AnimeVideo
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
from typing import Optional
from datetime import date
import datetime
from pathlib import Path
from tortoise import transactions
# Anime_Pydantic = pydantic_model_creator(Anime,exclude=['id'])
anime = APIRouter()
# print(Anime_Pydantic)
class anime_pydantic(BaseModel):
    title: Optional[str]
    description: Optional[str] = None
    cover_image: Optional[str] = None
    rating: Optional[int] = 0
    release_date: Optional[date] = datetime.datetime.now().date()
    genre: Optional[str] = None
    studio: Optional[str] = None
    director: Optional[str] = None
    characters: Optional[str] = None
    status: Optional[str] = None
    episodes: Optional[int] = 0
    source: Optional[str] = None
    watch_link: Optional[str] = None

class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 10

# 创建动漫
# @anime.post("/", response_model=anime_pydantic)
# async def create_anime(anime: anime_pydantic):
#     return await Anime.create(**anime.model_dump(exclude_unset=True))

# 获取所有动漫
# @anime.get("/")
# async def get_all_anime():
#     return await Anime.all()
@anime.get("/")
async def get_all_anime(page: int = Query(default=1, ge=1), page_size: int = Query(default=10, ge=1)):
    skip = (page - 1) * page_size
    anime = await Anime.all().offset(skip).limit(page_size)
    print(anime)
    return anime


# 获取单个动漫
@anime.get("/{anime_id}", responses={404: {"model": HTTPNotFoundError}})
async def get_anime(anime_id: int,request:Request):
    animes = await Anime.filter(id=anime_id).first()
    videos = await AnimeVideo.filter(anime_id=anime_id)
    result = animes.__dict__
    result['anime_video_count']= len(videos)
    return result
    # return {'request':Request}

# 更新动漫信息
@anime.put("/{anime_id}", response_model=anime_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_anime(anime_id: int, anime: anime_pydantic):
    await Anime.filter(id=anime_id).update(**anime.model_dump(exclude_unset=True))
    return await Anime.get(id=anime_id)

# # 删除动漫
# @anime.delete("/{anime_id}", response_model=dict, responses={404: {"model": HTTPNotFoundError}})
# async def delete_anime(anime_id: int):
#     deleted_count = await Anime.filter(id=anime_id).delete()
#     if not deleted_count:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Anime with id={anime_id} not found")
#     return {"message": "Anime deleted successfully"}

# 上传动漫视频路由
@anime.post("/")
# async def upload_video(anime: anime_pydantic, file: UploadFile = File(...)):
async def upload_video(title: str,
                       description: Optional[str] = None,
                       cover_image: Optional[str] = None,
                       rating: Optional[int] = 0,
                       release_date: Optional[date] = datetime.datetime.now().date(),
                       genre: Optional[str] = None,
                       studio: Optional[str] = None,
                       director: Optional[str] = None,
                       characters: Optional[str] = None,
                       status: Optional[str] = None,
                       episode: Optional[int] = 1,
                       episodes: Optional[int] = 12,
                       source: Optional[str] = None,
                       watch_link: Optional[str] = None,
                    #    tags: Optional[dict] = {},
                       file: UploadFile = File(...)
                      ):
    # 指定视频存储目录
    hash_value = hashlib.sha1(title.encode()).hexdigest()
    upload_folder = Path(f"/code/project/diona/videos/{hash_value}")
    directory = upload_folder
    os.makedirs(upload_folder, exist_ok=True)
    # 检查文件后缀
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in (".mp4", ".avi", ".mkv",".mov"):
        raise HTTPException(status_code=400, detail="只允许上传 MP4、AVI、MKV 或 MOV格式的视频文件")

    # 将视频保存到指定目录
    file_name = title + '_' + str(int(time.time() * 1000)) + file_extension.lower()
    file_path = os.path.join(upload_folder, file_name)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    data = await Anime.filter(title=title).first()
    
    if data:
        anime_id = data.id
    # async with transactions.atomic():
    else:
        anime_info = await Anime.create(
                                    title=title,
                                    description=description,
                                    cover_image=cover_image,
                                    rating=rating,
                                    release_date=release_date,
                                    genre=genre,
                                    studio=studio,
                                    director=director,
                                    characters=characters,
                                    status=status,
                                    episodes=episodes,
                                    source=source,
                                    watch_link=watch_link,
                                    # tags=tags,
                                )
        anime_id = anime_info.id
    video_file = await AnimeVideo.create(name=file_name,
                                    file_path=directory,
                                    anime_id=anime_id,
                                    episode=episode
                                    )

    # 将视频文件路径保存到数据库中
    

    return {"message": "视频上传成功", "video_file_id": video_file.id,"anime_info_id":anime_id}

# 删除全部动漫
@anime.delete('/')
async def delete_anime(anime_id: int):
    # 查询动漫信息
    age = await Anime.get_or_none(id=anime_id)
    if not age:
        raise HTTPException(status_code=404, detail="动漫信息不存在")
    
    # 查询关联的视频信息
    videos = await AnimeVideo.filter(id=anime_id)
    
    # 删除动漫信息
    await age.delete()
    
    if videos:
        for video in videos:
            # 删除数据库中的视频信息
            await video.delete()
            
            # 删除视频文件
            try:
                file_path = os.path.join(video.file_path, video.name)
                os.remove(file_path)
            except FileNotFoundError:
                pass

    return {"message": "动漫信息及关联的视频文件删除成功"}

# 删除动漫的第几集
@anime.delete('/video')
async def delete_anime_video(anime_id:int,video_id:int):
    videos = await AnimeVideo.filter(anime_id=anime_id,id=video_id).first()
    print(videos)
    await videos.delete()
    return {"message": "视频文件删除成功"}