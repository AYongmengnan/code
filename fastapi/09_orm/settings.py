TORTOISE_ORM = {
        'connections':{
            'default':{
                'engine':'tortoise.backends.mysql',
                'credentials':{
                    "host": "localhost",
                    "port": 3306,
                    "user": "root",
                    "password": "likeyou",
                    "database": "fastapi",
                    # "timeout": 30,
                    # "pool_size": 10,
                    # "max_overflow": 10,
                    "minsize": 1,
                    "maxsize": 10,
                    "charset":"utf8mb4",
                    # "wait_timeout": 10,
                    "echo": True},
            },
        },
        "apps": {
            "models": {
                "models": ["models",'aerich.models'], # 具体models.py文件的位置 如： db.models
                "default_connection": "default",
            }
        },
        'use_tz':False,
        'timezone':'Asia/Shanghai'
    }