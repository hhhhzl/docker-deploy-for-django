# Docker-Deploy-for-Django
Docker delopyment for django-nginx-mysql-react-redius

# DESP-API

## Running

通过 docker-compose 运行此应用。

```
docker-compose up
```

docker-compose 将启动两个 docker 容器：容器`desp-api_backend`用于运行后端应用，容器`desp-api_db`用于运行数据库。可使用以下命令获取容器信息。

```
docker ps

# 输出样例
CONTAINER ID   IMAGE              COMMAND                  CREATED      STATUS             PORTS                                                    NAMES
156ab7a4ff38   desp-api_backend   "./docker/wait-for-i…"   5 days ago   Up About an hour   0.0.0.0:58000->8000/tcp, :::58000->8000/tcp              desp-api_backend_1
56a3a4666389   mysql:8.0.25       "docker-entrypoint.s…"   5 days ago   Up About an hour   33060/tcp, 0.0.0.0:53306->3306/tcp, :::53306->3306/tcp   desp-api_db_1
```

可通过以下命令开启容器终端，从而对后端应用或数据库直接进行操作。

```
docker exec -it <CONTAINER-ID> bash

# <CONTAINER-ID> 也可使用其任意长度的前缀。例：156ab7a4ff38 -> 156
```

如果想退出运行，可按一次`Ctrl + C`， 或者另开一个终端输入以下命令。请尽量避免按两次`Ctrl + C`强行退出运行。

```
docker-compose stop
```

### 首次运行前

首次运行前需要进行数据库迁移并加载已有数据。此操作需开启一个后端应用容器的终端进行操作。

```
# 迁移数据库
python manage.py makemigrations
python manage.py migrate

# 加载数据
python manage.py loaddata fixture.json
```

## 代码结构

```
- db                    数据库源文件（由docker-compose在首次运行时下载）
- DESP                  后端
    - DESP                  Django全局设置
        - asgi.py               ASGI设置（可忽略）
        - settings.py           全局设置
        - urls.py               全局URL映射关系
        - wsgi.py               WSGI设置（可忽略）
    - docker                后端用docker
    - media                 后端用户上传文件存储
    - platform_apps         Django应用
        - files                 文件
            - migrations            数据库迁移文件（Django自动生成）
            - admin.py              Django admin注册（可忽略）
            - apps.py               Django 应用注册
            - models.py             数据模型
            - serializers.py        Django REST Framework 序列化器
            - urls.py               URL映射关系
            - views.py              视图
        - junctions             多对多关系（参评机构、专家分配）
            - ...                   同上
        - organizations         机构
            - ...                   同上
        - projects              评估项目
            - ...                   同上
        - questionnaires        问卷
            - ...                   同上
        - questions             问题
            - ...                   同上
        - scores                打分
            - ...                   同上
        - submissions           填报内容
            - ...                   同上
        - users                 用户（含用户认证）
            - ...                   同上
        - utils.py              各应用共用工具函数
    - devutils.py           开发用工具函数
    - fixture.json          备份数据
    - manage.py             Django程序入口
- .gitattributes        git文件属性
- .gitignore            git忽略文件
- docker-compose.yml    docker-compose配置文件
- README.md             README文档
```

## URL 映射关系

每个 API 接口内的具体资源、请求方式、请求格式与返回格式请参考 API 文档。

```
- admin/                Django Admin页面
- api/                  API
    - admin/                Django REST Framework Admin页面
    - organizations/        机构
    - users/                用户（含用户认证）
    - projects/             评估项目
    - questionnaires/       问卷
    - questions/            问题
    - submissions/          填报内容
    - scores/               打分
    - junctions/            多对多关系（参评机构、专家分配）
    - files/                文件
- docs/                 API文档
    - swagger/              使用Swagger风格生成的页面
    - redoc/                使用Redoc风格生成的页面
    - swagger.yaml          使用Swagger风格生成的yaml文件
- media/                文件
    - uploads/              用户上传文件
```

## 常见问题

### 文件权限不足

`git clone`命令有可能移除 docker 运行依赖的`sh`文件的执行权限，导致容器启动失败。此时，使用以下命令重新赋予执行权限。

```
chmod +x ./DESP/docker/*.sh
```

### 数据库迁移 (`migration`) 时发生冲突

对数据模型进行改动有可能会造成迁移冲突。此时，可先将现有数据进行备份，删除现有迁移文件与数据库，重新进行迁移，最后将数据恢复。此方法较为危险，请谨慎使用。

```
# 进入应用目录
cd ./DESP

# 备份数据
python manage.py dumpdata -e auth -e contenttypes -e authtoken > fixture.json

# 删除迁移文件
python devutils.py remove_migrations

# 删除并重建数据库
DROP DATABASE desp;
CREATE DATABASE desp;

# 重新迁移数据库
python manage.py makemigrations
python manage.py migrate

# 重新加载数据
python manage.py loaddata fixture.json
```

