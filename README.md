配置文件在 `config.ini` 
接口路由在 `demo\urls.py`


启动命令：
```
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

启动后GET请求：`http://localhost:8000/api/device` 