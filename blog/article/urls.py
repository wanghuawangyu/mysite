from django.conf.urls import url
from article import views
urlpatterns=[
    url(r'article_list',views.article_list),
    url(r'article_edit',views.article_edit),
    url(r'article_add',views.article_add),
    url(r'article_delete',views.article_delete),
    url(r'article_detail',views.article_detail),
    url(r'',views.article_list)
]