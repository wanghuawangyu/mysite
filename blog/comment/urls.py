from django.conf.urls import url
from comment import views
urlpatterns=[
    url(r'comment_list',views.comment_list),
    url(r'comment_add',views.comment_add),
    url(r'comment_delete',views.comment_delete),
    url(r'comment_retry_add',views.comment_retry_add),
    url(r'comment_retry_me',views.comment_retry_me),
    url(r'',views.comment_list)
]