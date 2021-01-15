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

### プロジェクト
初めて Django を使うのなら、最初のセットアップを行う必要があります。通常は、 Django の プロジェクト (project) を構成するコードを自動生成します。プロジェクトとは、データベースの設定や Django 固有のオプション、アプリケーション固有の設定などといった、個々の Django インスタンスの設定を集めたものです。  
`django-admin startproject django_app`  
django_app -> プロジェクト  

###  アプリケーション
Django 内に追加する各アプリケーションは、所定の規約に従った Python パッケージで構成されます。 Django には基本的なディレクトリ構造を自動生成するユーティリティが含まれているので、ディレクトリを作ることではなくコードを書くことに集中できます。   
`python manage.py startapp polls`  
polls      -> アプリケーション  


### Djangoの構成

- モデル層  
    モデルは、データに関する唯一かつ決定的な情報源です。あなたが保持するデータが必要とするフィールドとその動作を定義します。一般的に、各モデルは単一のデータベースのテーブルに対応付けられます。 
    基本:  

    - モデルは各々 Python のクラスであり django.db.models.Model のサブクラスです。  
    - モデルの属性はそれぞれがデータベースのフィールドを表します。  
    - これら全てを用いて、Django はデータベースにアクセスする自動生成された API を提供します。 クエリを作成する を参照してください。  

    簡単な例  
    ```python   
    from django.db import models

    class Person(models.Model):
        first_name = models.CharField(max_length=30)
        last_name = models.CharField(max_length=30)
    ```

- ビュー層  
    Django には「ビュー (views)」と呼ばれる概念があります。ビューは、ユーザーリクエストを処理してレスポンスを返すロジックをカプセル化したものです。以下のリンクから、ビューの詳細を学びましょう。  

- テンプレート層  
    テンプレート層は、ユーザに表示される情報をレンダリングするための、デザイナーにも書きやすい構文を提供します。デザイナーによるテンプレートの構文の使い方や、プログラマーが構文を拡張する方法について学びましょう。  

    ```python
    {% extends "base_generic.html" %}

    {% block title %}{{ section.title }}{% endblock %}

    {% block content %}
    <h1>{{ section.title }}</h1>

    {% for story in story_list %}
    <h2>
    <a href="{{ story.get_absolute_url }}">
        {{ story.headline|upper }}
    </a>
    </h2>
    <p>{{ story.tease|truncatewords:"100" }}</p>
    {% endfor %}
    {% endblock %}
    ```

- フォーム  
    Django には、フォームを簡単に作成したり、フォームに入力されたデータを簡単に操作できるようにしてくれる、多機能なフレームワークがあります。  
    あなたの作ろうとしているウェブサイトやアプリケーションが、単にコンテンツを公開したり訪問者からのインプットを受け付けないサイトでない限り、フォームを理解し利用する必要があります。  

    Django はフォームの構築を助けるさまざまなツールやライブラリを提供しています。これらを利用することで、サイト訪問者からデータの入力を受け入れ、そのデータを処理したあと、入力に応じたレスポンスを返すことができるようになります。  


### マイグレーション
1. models.pyでテーブル構造を定義  
    ```python
    from django.db import models

    class Question(models.Model):
        quesiton_text = models.CharField(max_length = 200)
        pub_date      = models.DateTimeField('date_published')

    class Choice(models.Model):
        question    = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=200)
        votes       = models.IntegerField(default=0)
    ```
2. マイグレーションの作成  
    `python manage.py makemigrations polls`  
3. SQL文の作成  
    `python manage.py sqlmigrate polls 0001`  
4. マイグレーションの実行  
    `python manage.py migrate`  

