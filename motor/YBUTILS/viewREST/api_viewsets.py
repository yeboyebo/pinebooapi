import json
import sys
import traceback

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


from django.http import HttpResponse
from django.http import HttpResponseServerError

from django.db import transaction

from YBUTILS.viewREST import filtersPagination
from YBUTILS.APIQSA import APIQSA


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class YBControllerViewSet(viewsets.ViewSet, APIView):
    # permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dameuseracl(self, request):
        params = None
        if request.method in ["POST", "DELETE", "PUT"]:
            print("pasa")
            try:
                params = {}
                # print(request.body)
                params["data"] = json.loads(request.body.decode("utf-8"))
                # print("por")

            except Exception as e:
                print(e)
                params = {}
                print(request._data)
                params['data'] = filtersPagination._generaPostParam(request._data)["POST"]

        elif request.method == "GET":
            params = filtersPagination._generaGetParam(request.query_params)
        try:
            username = request.user.username
            print("____________")
            print(username)
            print(params)
            obj = APIQSA.getuseracl('post', params, username)
            result = HttpResponse(json.dumps(obj), status=200, content_type='application/json')
            result['Access-Control-Allow-Origin'] = '*'
            return result

        except Exception as e:
            print(bcolors.FAIL + "Excepcion " + str(e) + bcolors.ENDC)

            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" % ex_value)
            print("Stack trace : \n")
            for index, l in enumerate(stack_trace):
                if index < len(stack_trace) - 1:
                    print(l)
                else:
                    print(bcolors.WARNING + l + bcolors.ENDC)

            resp = HttpResponseServerError(str(e))
            resp['Access-Control-Allow-Origin'] = '*'
            return resp

    def optionsFun(self, request, modulo=None, controlador=None, accion=None, pk=None):
        resp = HttpResponse("{}", status=200, content_type="application/json")
        resp["Access-Control-Allow-Origin"] = "*"
        resp["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        resp["Access-Control-Allow-Credentials"] = True
        resp["Access-Control-Allow-Methods"] = "GET,POST,PATCH"

        return resp

    def dame_params_from_request(self, request, params):
        # Aqui añadimos parametros que queramos sacar de request como files
        # O parametros de HEADER tipo HTTP_KEY, HTTP_SOURCE, CONTENT_TYPE, REMOTE_ADDR, etc ...
        try:
            if request.FILES:
                params["FILES"] = request.FILES
        except Exception as e:
            print(e)
            pass
        return params

    def ejecutaraccioncontrolador(self, request, modulo, accion=None, pk=None):
        # current_user = request.user
        username = request.user.username

        print("USER: " + str(username))
        print("ejecutaraccioncontrolador!!", str(modulo), str(accion), str(pk))
        print(bcolors.OKBLUE + "METHOD: " + request.method + bcolors.ENDC)
        method = request.method.lower()

        params = {}
        if pk:
            params["pk"] = pk
        if method == "get":
            data = filtersPagination._generaGetParam(request.query_params)
            if data:
                params["params"] = data
        else:
            try:
                params["params"] = json.loads(request.body.decode("utf-8"))
            except json.decoder.JSONDecodeError:
                params["params"] = str(request.body.decode("utf-8"))

        params = self.dame_params_from_request(request, params)

        try:
            if method == "get":
                obj = APIQSA.entry_point(method, modulo, username, params, accion)
                result = HttpResponse(json.dumps(obj), status=200, content_type='application/json')

            else:
                with transaction.atomic():
                    obj = APIQSA.entry_point(method, modulo, username, params, accion)
                    result = HttpResponse(json.dumps(obj), status=200, content_type='application/json')

            if not isinstance(result, (Response, HttpResponse)):
                raise Exception('La respuesta no es Response o HttpResponse')

            result['Access-Control-Allow-Origin'] = '*'
            return result

        except Exception as e:
            print(bcolors.FAIL + "Excepcion " + str(e) + bcolors.ENDC)

            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : \n")
            for index, l in enumerate(stack_trace):
                if index < len(stack_trace) - 1:
                    print(l)
                else:
                    print(bcolors.WARNING + l + bcolors.ENDC)

            resp = HttpResponseServerError(str(e))
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
