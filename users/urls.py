from django.conf.urls import url

from .apis import CreateUserApi, TestModelApi

urlpatterns = [
    url(regex=r'^user_oprations/$', name='createaa', view=CreateUserApi.as_view()),
    url(regex=r'^test_oprations/$', name='create_test', view=TestModelApi.as_view())
    # url(regex=r'^list/$', name='list', view=CreateUserApi.as_view())
]
