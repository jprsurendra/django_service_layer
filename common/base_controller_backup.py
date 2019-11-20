from django.core.exceptions import ValidationError
import json
from rest_framework.response import Response
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

    # def dispatch(self, request, *args, **kwargs):
    #     # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    #     service_method = None
    #     if request.method.lower() in self.http_method_names:
    #         if request.method.lower() == 'get':
    #             service_method = 'service_list'
    #         elif request.method.lower() == 'post':
    #             service_method = 'service_create'
    #         elif request.method.lower() == 'delete':
    #             service_method = 'service_destroy'
    #         elif request.method.lower() == 'put' or request.method.lower() == 'patch':
    #             service_method = 'service_update'
    #
    #         if request.method.lower() == 'post':
    #             service_method = request.POST.get("service_method", service_method)
    #         elif request.method.lower() == 'get':
    #             service_method = request.GET.get("service_method", service_method)
    #         # else:
    #         #     body_unicode = request.body.decode('utf-8')
    #         #     print "body_unicode: ", body_unicode
    #         #     body_json = json.loads(body_unicode)
    #         #     print "body_json: ", body_json
    #
    #         setattr(self, "service_method", service_method)
    #         # if service_method:
    #         #     service_method_name = "service_" + service_method.lower()
    #         #     handler = getattr(self, service_method_name, self.http_method_not_allowed)
    #         #     if handler == self.http_method_not_allowed:
    #         #         handler = getattr(self, "service", self.http_method_not_allowed)
    #         #         if handler == self.http_method_not_allowed:
    #         #             handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    #         # else:
    #         #     handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    #         handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    #     else:
    #         handler = self.http_method_not_allowed
    #
    #     return handler(request, *args, **kwargs)

    # def service(self, request, *args, **kwargs):
    #     pass




    def transform_serializer_data(self, serializer):
        print "/users/base_controller.py --> class GenericServiceApi --> transform_serializer_data(...)"
        return serializer.validated_data

    def call_service(self, **service_data):
        print "/users/base_controller.py --> class GenericServiceApi --> call_service(...) ==> service_data = ", service_data
        service = self.get_service()
        return service(**service_data)


    def get_service(self,request_data):
        raise NotImplemented()

    def get_response(self):
        raise NotImplemented()

    def service(self, request, request_data, *args, **kwargs):
        raise NotImplemented()

    def service_list(self, request, request_data, *args, **kwargs):
        raise NotImplemented()

    def service_create(self, request, request_data, *args, **kwargs):
        raise NotImplemented()

    def service_destroy(self, request, request_data, *args, **kwargs):
        raise NotImplemented()

    def service_update(self, request, request_data, *args, **kwargs):
        raise NotImplemented()

    # def service(self, request, *args, **kwargs):
    #     raise NotImplemented()
    #
    # def service_list(self, request, *args, **kwargs):
    #     raise NotImplemented()
    #
    # def service_create(self, request, *args, **kwargs):
    #     raise NotImplemented()
    #
    # def service_destroy(self, request, *args, **kwargs):
    #     raise NotImplemented()
    #
    # def service_update(self, request, *args, **kwargs):
    #     raise NotImplemented()

    def data_wrapper_response(data=None, status_code=None):
        if status_code and status_code in [200, 201, 202, 204]:
            status = True
        else:
            status = False

        data = {
            'status': status,
            'status_code': status_code,
            'data': data
        }

        return Response(data, status=status_code)

    def get_serializer_data(self, request, is_validated_data = True):
        request_data = request.data.copy()
        del request_data['service_method']

        serializer = self.get_serializer(data=request_data)

        if is_validated_data:
            serializer.is_valid(raise_exception=True)

        service_data = serializer.validated_data
        return service_data

    def validate_data(self, request, serializer = None, is_raise_exception = True):
        if serializer == None:
            serializer = self.get_serializer(data=request.data)
        return serializer.is_valid(raise_exception=is_raise_exception)

    def post(self, request, *args, **kwargs):
        print "/users/base_controller.py --> class GenericServiceApi --> post(...)"
        service_method = request.POST.get("service_method", 'service_create')
        setattr(self, "service_method", service_method)

        service_method_name = "service_" + service_method.lower()
        handler = getattr(self, service_method_name, self.http_method_not_allowed)
        if handler == self.http_method_not_allowed:
            handler = getattr(self, "service", self.http_method_not_allowed)

        # request_data = self.request_data(request)
        return handler(request, *args, **kwargs)

        #
        # # self.validate_data(self, request, is_raise_exception=True)
        #
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        #
        # service_data = self.transform_serializer_data(serializer)
        # service_call_result = self.call_service(**service_data)
        #
        # response = self.get_response(service_call_result)
        #
        # return response
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
