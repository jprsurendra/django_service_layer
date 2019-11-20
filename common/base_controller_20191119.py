from django.core.exceptions import ValidationError
from django.apps import apps
from django.forms.models import model_to_dict
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from rest_framework.exceptions import ValidationError as DrfValidationError
from rest_framework.exceptions import PermissionDenied as DrfPermissionDenied


def get_first_matching_attr(obj, default=None, *attrs):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc):
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg


class BaseController(GenericAPIView):

    def __init__(self, app_name, model_name):
        # super(TestModelApi, self).__init__('users', "TestModel")
        self.Model = apps.get_model(app_name, model_name)


    expected_exceptions = {
        # Python errors here:PermissionError
        ValueError: DrfValidationError,
        # Django errors here:
        ValidationError: DrfValidationError,
        # PermissionError: DrfPermissionDenied
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))
            return super(BaseController, self).handle_exception(drf_exception)
            # return super().handle_exception(drf_exception)

        return super(BaseController, self).handle_exception(exc)
        # return super().handle_exception(exc)

    def dispatch(self, request, *args, **kwargs):
        return super(BaseController, self).dispatch(request, *args, **kwargs)

    def service(self, request,  *args, **kwargs):
        raise NotImplemented()

    def service_list(self, request,  *args, **kwargs):
        # raise NotImplemented()a.pk.name
        print "PK Name: ", self.Model._met
        data  = [model_to_dict(o) for o in self.Model.objects.all()]
        # return HttpResponse(json.dumps(data), content_type='application/json; charset=UTF-8', status=status)
        return self.data_wrapper_response(result_data=data , status_code=status.HTTP_202_ACCEPTED)

    def service_save(self, request,  *args, **kwargs):
        # raise NotImplemented()
        pk_field_name =  self.Model._meta.pk.name
        pk_field_vlaue = request.data.get(pk_field_name, None)
        if pk_field_vlaue:
            instance = self.Model.objects.get(pk=pk_field_vlaue)
            service_data = self.get_serializer_data(request, instance=instance, partial=True)
            updated_rows = self.Model.objects.filter(pk=pk_field_vlaue).update(**service_data)
            obj = self.Model.objects.get(pk=pk_field_vlaue)
            result_data = model_to_dict(obj)
            result_data['response_message'] ="%s rows updated"%(updated_rows)
        else:
            service_data = self.get_serializer_data(request)
            obj = self.Model.objects.create(**service_data)
            result_data = model_to_dict(obj)

        return self.data_wrapper_response(result_data=result_data, status_code=status.HTTP_202_ACCEPTED)

    def service_create(self, request, *args, **kwargs):
        service_data = self.get_serializer_data(request)
        obj = self.Model.objects.create(**service_data)
        result_data = model_to_dict(obj)
        return self.data_wrapper_response(result_data=result_data, status_code=status.HTTP_202_ACCEPTED)

    def service_destroy(self, request,  *args, **kwargs):
        raise NotImplemented()

    def service_update(self, request,  *args, **kwargs):
        # raise NotImplemented()
        pk_field_name = self.Model._meta.pk.name
        pk_field_vlaue = request.data.get(pk_field_name, None)

        instance = self.Model.objects.get(pk=pk_field_vlaue)
        service_data = self.get_serializer_data(request, instance=instance, partial=True)
        updated_rows = self.Model.objects.filter(pk=pk_field_vlaue).update(**service_data)
        obj = self.Model.objects.get(pk=pk_field_vlaue)
        result_data = model_to_dict(obj)
        result_data['response_message'] = "%s rows updated" % (updated_rows)

        return self.data_wrapper_response(result_data=result_data, status_code=status.HTTP_202_ACCEPTED)


    def data_wrapper_response(self, result_data=None, status_code=None):
        if status_code and status_code in [200, 201, 202, 204]:
            status = True
        else:
            status = False

        data = {
            'status': status,
            'status_code': status_code,
            'data': {'result' : result_data}
        }
        # data = None, status = None
        return Response(data, status=status_code)

    def get_serializer_data(self, request, instance=None, partial=False, is_validated_data = True):
        request_data = request.data.copy()
        print request_data

        model_fields =[]
        for field in self.Model._meta.fields:
            model_fields.append(field.name)

        for key in request_data.keys():
            if not str(key) in model_fields:
                del request_data['service_method']

        if instance:
            serializer = self.get_serializer(instance = instance, data=request_data)
        else:
            serializer = self.get_serializer(data=request_data)

        if is_validated_data:
            serializer.is_valid(raise_exception=True)

        service_data = serializer.validated_data
        return service_data

    def validate_data(self, request, serializer = None, is_raise_exception = True):
        if serializer == None:
            serializer = self.get_serializer(data=request.data)
        return serializer.is_valid(raise_exception=is_raise_exception)

    def common_method(self, request, service_method, *args, **kwargs):
        service_method_name = "service_" + service_method.lower()
        handler = getattr(self, service_method_name, self.http_method_not_allowed)
        if handler == self.http_method_not_allowed:
            handler = getattr(self, "service", self.http_method_not_allowed)
        # request_data = self.request_data(request)
        return handler(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        service_method = request.GET.get("service_method", 'list')
        return self.common_method(request, service_method, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        service_method = request.POST.get("service_method", 'create')
        return self.common_method(request, service_method, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        service_method = request.POST.get("service_method", 'update')
        return self.common_method(request, service_method, *args, **kwargs)

    #
    # def get(self, request, *args, **kwargs):
    #     print "/users/base_controller.py --> class GenericServiceApi --> get(...)"
    #     print "kwargs: ", kwargs
    #     print "args: ", args
    #     print "request.method: ", request.method
    #     print "request.data: ", request.data
    #     self.list(request, *args, **kwargs)

    # def list(request, *args, **kwargs):
    #     pass
    # def retrieve(request, *args, **kwargs):
    #     pass
    # def destroy(request, *args, **kwargs):
    #     pass
    # def update(request, *args, **kwargs):
    #     pass
    # def partial_update(request, *args, **kwargs):
    #     pass
    # def patch(self, request, *args, **kwargs):
    #     pass
    #
    # def get(self, request, *args, **kwargs):
    #     pass
    #
    # def post(self, request, *args, **kwargs):
    #     pass
    #
    # def delete(self, request, *args, **kwargs):
    #     pass
    #
    # def put(self, request, *args, **kwargs):
    #     pass
    #
    # def patch(self, request, *args, **kwargs):
    #     pass
