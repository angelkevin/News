"""News URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from NewsWeb import views

urlpatterns = [

    path("", views.home),
    path("zhihu", views.zhihu),
    path("baidu", views.baidu),
    path("weibo", views.weibo),
    path("toutiao", views.toutiao),
    path("douyin", views.douyin),
    path("news", views.news),
    path("keji", views.keji),
    path("guoji", views.guoji),
    path("caijin", views.caijin),
    path("shehui", views.shehui),
    path("junshi", views.junshi),
    path("yule", views.yule),
    path("tiyu", views.tiyu),
    path("draw", views.drawyule),
    path("drawkeji", views.drawkeji),
    path("drawtiyu", views.drawtiyu),
    path("drawguoji", views.drawguoji),
    path("drawyule", views.drawyule),
    path("drawshehui", views.drawshehui),
    path("drawcaijin", views.drawcaijin),
    path("drawjunshi", views.drawjunshi),
path("home", views.home),

]
