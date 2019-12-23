import json
import importlib
import sys
import traceback

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse
from django.http import HttpResponseServerError

from django.db import transaction
from django.contrib.sessions.models import Session

from YBUTILS.viewREST import filtersPagination
from YBUTILS.APIQSA import APIQSA


class YBControllerViewSet(viewsets.ViewSet, APIView):
    # permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionsFun(self, request, modulo, controlador=None, accion=None, pk=None):

        # TO DO: Ver si es posible conmprobar que se está usando la cookie de sesión

        resp = HttpResponse("{}", status=200, content_type="application/json")
        resp["Access-Control-Allow-Origin"] = "*"
        resp["Access-Control-Allow-Headers"] = "X-SessionID"
        resp["Access-Control-Allow-Credentials"] = True
        resp["Access-Control-Allow-Methods"] = "GET,POST"

        return resp

    def dame_controlador(self, modulo, controlador, accion):

        try:
            if controlador is None:
                # nombre_fichero = self.dame_nombre_fichero('GET', modulo)
                # print("nombre_fichero " + nombre_fichero)

                print(0)
                # spec = find_spec(nombre_fichero, path=self._aplicacion + "/" + modulo)
                print(str(self._aplicacion + "/" + modulo))                
                # controller = importlib.import_module(nombre_fichero, package=self._aplicacion + "/ot/" + modulo )
                controller = importlib.import_module(self._aplicacion + "." + modulo)
                print(str(controller))                
                # controller_class = getattr(controller, modulo, None)
                controller_class = getattr(controller, modulo, None)
                print("controller_class " + str(controller_class))
            else:
                controller = importlib.import_module(self._aplicacion + "." + modulo + "." + controlador + "." + accion)
                controller_class = getattr(controller, accion, None)

        except ImportError as e:
            raise NameError("No se pudo importar el controlador {}.{} porque no se encontró un módulo: {}".format(self._aplicacion, controlador, e))

        except SyntaxError as e:
            raise NameError("No se pudo importar el controlador {}.{} por un problema de sintaxis: {}".format(self._aplicacion, controlador, e))

        except Exception as e:
            raise NameError("No se pudo importar el controlador {}.{}: {}".format(self._aplicacion, controlador, e))

        return controller_class

    
    def dame_nombre_fichero(self, metodo, nombre_modelo):

        nombre_fichero = None
        if metodo in ('GET', 'POST'):
            nombre_fichero = metodo.lower() + '_' + nombre_modelo

        return nombre_fichero


    def ejecutaraccioncontrolador(self, request, modulo, controlador=None, accion=None, pk=None):
        current_user = request.user
        username = request.user.username
        # if username in ('AnonymousUser', ''):
        #     idSession = request.META.get("HTTP_X_SESSIONID")
        #     print("idSession", str(idSession))
        #     s = Session.objects.get(session_key=idSession)
        #     print("s", str(s))
        #     session_data = s.get_decoded()
        #     username = session_data.get('_auth_user_id')

        print("USER: " + str(username))
        print("ejecutaraccioncontrolador!!", str(modulo), str(controlador), str(accion), str(pk))
        
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
                params = filtersPagination._generaPostParam(request._data)["POST"]

        elif request.method == "GET":
            params = filtersPagination._generaGetParam(request.query_params)

        # controller = self.dame_controlador(modulo, controlador, accion)

        try:
            if request.method == "GET":
                print("llamando GET")
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
            print('Excepción ', str(e))

            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %"\n".join(stack_trace))

            resp = HttpResponseServerError(str(e))
            resp['Access-Control-Allow-Origin'] = '*'
            return resp
