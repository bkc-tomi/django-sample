# docker上にdjango開発環境を作ってみる

1. ファイルを用意

    .
    ├── README.md
    ├── db
    │   └── Dockerfile
    ├── docker-compose.yml
    └── web
        ├── Dockerfile
        └── requirements.txt

2. コンテナのビルド

    docker-compose build

3. Djangoプロジェクトの作成

    docker-compose run web django-admin.py startproject django_app .

4. コンテナ立ち上げ
    docker-compose up

5. コンテナを開く
    docker-compose exec web bash

6. コンテナ内からDjangoを起動
    python3 manage.py runserver 0.0.0.0:8000
    必要に応じてdocker-compose.ymlに記述しても良い
