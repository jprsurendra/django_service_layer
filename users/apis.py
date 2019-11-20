# //https://stackoverflow.com/questions/757022/how-do-you-serialize-a-model-instance-in-django

from rest_framework.response import Response
from rest_framework import status

from django.core import serializers
import json
from django.forms.models import model_to_dict

from common.base_controller import BaseController
from users.models import BaseUser, TestModel
from django.apps import apps

from users.services import create_user
from users.serializers import CreateUserSerializer, TestModelSerializer


class TestModelApi(BaseController):
    serializer_class = TestModelSerializer

    def __init__(self):
        super(TestModelApi, self).__init__('users', "TestModel")

    # def dispatch(self, request, *args, **kwargs):
    #     print request.body
    #     from django.http import QueryDict
    #     put = QueryDict(request.body)
    #     description = put.get('name')
    #     print "description: ", description
    #
    #     return super(TestModelApi, self).dispatch(request, *args, **kwargs)

    def service(self, request,  *args, **kwargs):
        raise NotImplemented()

    # def service_list(self, request,  *args, **kwargs):
    #     # objs = TestModel.objects.all()
    #     objs = self.Model.objects.all()
    #
    #     data1 = [model_to_dict(o) for o in objs]
    #
    #     # result = list(objs)
    #     # data1 = json.dumps(result)
    #
    #     # data1 = model_to_dict(objs)
    #
    #
    #     # data = serializers.serialize('json', objs)
    #     # data = [o.json for o in objs]
    #     # data1 = json.dumps(data)
    #
    #     # struct = json.loads(data)
    #     # data1 = json.dumps(struct[0])
    #
    #     # import simplejson
    #     # return simplejson.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
    #
    #
    #
    #     # return HttpResponse(json.dumps(data), content_type='application/json; charset=UTF-8', status=status)
    #
    #     return self.data_wrapper_response(result_data = data1, status_code=status.HTTP_202_ACCEPTED)

    # def service_create(self, request,  *args, **kwargs):
    #     service_data = self.get_serializer_data(request)
    #     obj = TestModel.objects.create(**service_data)
    #
    #
    #
    #     return self.data_wrapper_response(result_data=None, status_code=status.HTTP_202_ACCEPTED)

    def service_destroy(self, request,  *args, **kwargs):
        raise NotImplemented()

    # def service_update(self, request,  *args, **kwargs):
    #     raise NotImplemented()



class CreateUserApi(BaseController):
    serializer_class = CreateUserSerializer

    def dispatch(self, request, *args, **kwargs):
        return super(CreateUserApi, self).dispatch(request, *args, **kwargs)

    def service_list(self, request, *args, **kwargs):
        raise NotImplemented()

    def service_create(self, request, *args, **kwargs):
        service_data = self.get_serializer_data(request)
        # for data in service_data:
        #     o1.data.key() = o1.data.value()
        # o1.save()





        # o1(**service_data).save()
        # obj = BaseUser.objects.create(**service_data)


        # obj = BaseUser.objects.create(email=service_data['email'], password=service_data['password'])
        obj = BaseUser.objects.create(**service_data)

        return self.data_wrapper_response(data = None, status_code=status.HTTP_202_ACCEPTED )

    # service_create.__annotations__ = {'return': BaseUser}



    def service_destroy(self, request, *args, **kwargs):
        raise NotImplemented()

    def service_update(self, request, *args, **kwargs):
        raise NotImplemented()

    def get_service(self):
        print "/users/services.py --> class CreateUserApi --> get_service(...)"
        obj = create_user
        return obj

    def get_response(self, service_result):
        print "/users/services.py --> class CreateUserApi--> get_response(...)"
        return Response(status=status.HTTP_202_ACCEPTED)
