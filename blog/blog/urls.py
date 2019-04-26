# -*- coding: utf-8 -*-
"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
# from django.contrib import admin
import sys
sys.path.append('..')
from friend import urls as friend_urls
from category import urls as category_urls
from article import urls as article_urls
from comment import urls as comment_urls
from account import urls as account_urls
from main import urls as main_urls


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^category',include(category_urls)),
    url(r'^friend',include(friend_urls)),
    url(r'^article',include(article_urls)),
    url(r'^comment',include(comment_urls)),
    url(r'^account',include(account_urls)),
    url(r'',include(main_urls)),
]
