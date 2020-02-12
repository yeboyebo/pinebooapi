import json

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

    def optionsFun(self, request, modulo, controlador=None, accion=None, pk=None):
        resp = HttpResponse("{}", status=200, content_type="application/json")
        resp["Access-Control-Allow-Origin"] = "*"
        resp["Access-Control-Allow-Headers"] = "Authorization"
        resp["Access-Control-Allow-Credentials"] = True
        resp["Access-Control-Allow-Methods"] = "GET,POST"

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

        params = None
        if request.method == "POST":
            try:
                if pk is not None:
                    params = {}
                    params['pk'] = pk
                    params['data'] = json.loads(request.body.decode("utf-8"))
                else:
                    params = json.loads(request.body.decode("utf-8"))

            except Exception:
                params = {}
                params['pk'] = pk
                params['data'] = filtersPagination._generaPostParam(request._data)["POST"]

        elif request.method == "GET":
            params = filtersPagination._generaGetParam(request.query_params)

        params = self.dame_params_from_request(request, params)

        try:
            if request.method == "GET":
                print(bcolors.OKBLUE + "llamando GET" + bcolors.ENDC)
                obj = APIQSA.entry_point('get', modulo, username, params, accion)
                result = HttpResponse(json.dumps(obj), status=200, content_type='application/json')
                # action = getattr(controller, "start", None)
                # result = action(pk, params, username)

            else:
                # action = getattr(controller, accion, None)
                with transaction.atomic():
                    # result = action(pk, params, username)
                    obj = APIQSA.entry_point('post', modulo, username, params, accion)
                    result = HttpResponse(json.dumps(obj), status=200, content_type='application/json')

            if not isinstance(result, (Response, HttpResponse)):
                raise Exception('La respuesta no es Response o HttpResponse')

            result['Access-Control-Allow-Origin'] = '*'
            return result

        except Exception as e:
            resp = HttpResponseServerError(str(e))
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
