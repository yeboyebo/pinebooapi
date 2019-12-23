from django.db.models import Field, Model
from django.http import HttpResponseRedirect

from rest_framework import serializers
from rest_framework.response import Response

from YBUTILS.viewREST.accessControl import accessControl


# ------------decoradores para indicar metodos accion en modelos, querySets o Manager------------
class decoradores:

    def checkSystemAuthentication(view_func):
        def decorador(request, *args, **kwargs):
            usuario = request.request.user

            if not usuario.is_authenticated:
                return HttpResponseRedirect("/")

            if not usuario.is_superuser:
                return HttpResponseRedirect("/403")

            response = view_func(request, *args, **kwargs)
            return response
        return decorador

    def check_system_authentication_iface(view_func):
        def decorador(iface, request, *args, **kwargs):
            usuario = request.user

            if not usuario.is_authenticated:
                return HttpResponseRedirect("/")

            if not usuario.is_superuser:
                return HttpResponseRedirect("/403")

            response = view_func(iface, request, *args, **kwargs)
            return response
        return decorador

    def checkAuthentication(view_func):
        def decorador(request, *args, **kwargs):
            usuario = request.request.user

            if not usuario.is_authenticated:
                return HttpResponseRedirect("/")

            if "accion" in kwargs:
                status = accessControl.checkAction(request, view_func.__name__, *args, **kwargs)
                print(status)
                if not status:
                    response = Response({"msg": "Error"}, status=401)
                    return response

            elif not accessControl.checkAccess(request, view_func.__name__, *args, **kwargs):
                return HttpResponseRedirect("/403")

            response = view_func(request, *args, **kwargs)
            return response
        return decorador

    def check_authentication_iface(view_func):
        def decorador(iface, request, *args, **kwargs):
            usuario = request.user

            if not usuario.is_authenticated and request.path:
                return HttpResponseRedirect("/login?next=" + request.path)
            if not usuario.is_authenticated:
                return HttpResponseRedirect("/login")

            response = view_func(iface, request, *args, **kwargs)
            return response
        return decorador

    @staticmethod
    def systemAccion(**kwargs):
        """
        Usado para marcar un metodo como accion de sistema.
        """
        def decorator(func):
            # TODO
            func.kwargs = kwargs
            return func
        return decorator

    @staticmethod
    def accion(verbose_name=None, miparam=None, aqparam=None, tipo="I", **kwargs):
        """
        Usado para marcar un metodo como accion.
        """
        def decorator(func):
            func.miparam = miparam
            func.aqparam = aqparam
            func.tipo = tipo
            func.isaccion = True
            func.verbose_name = func.__name__ if (verbose_name is None) else verbose_name
            func.kwargs = kwargs
            return func
        return decorator

    @staticmethod
    def csr(verbose_name=None, **kwargs):
        def decorator(func):
            func.iscsr = True
            func.verbose_name = func.__name__ if (verbose_name is None) else verbose_name
            func.kwargs = kwargs
            return func
        return decorator
