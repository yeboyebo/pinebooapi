from rest_framework.routers import Route
from rest_framework.routers import SimpleRouter

from YBUTILS.viewREST import api_viewsets
from YBUTILS.viewREST import helpers

class apiRouter(SimpleRouter):
    """Router para API"""

    routes = [
        Route(
            url=r'(?P<modulo>\w+)/(?P<pk>\w+)/(?P<accion>\w+)',
            mapping={'get': 'ejecutaraccioncontrolador', 'post': 'ejecutaraccioncontrolador', 'options': 'optionsFun'},
            name='{basename}-accion-REST',
            initkwargs={},detail=True
        ),
        Route(
            url=r'(?P<modulo>\w+)/accion/(?P<accion>\w+)$',
            mapping={'get': 'ejecutaraccioncontrolador', 'post': 'ejecutaraccioncontrolador', 'options': 'optionsFun'},
            name='{basename}-accion-REST',
            initkwargs={},detail=True
        ),
        Route(
            url=r'(?P<modulo>\w+)/(?P<pk>\w+)',
            mapping={'get': 'ejecutaraccioncontrolador', 'post': 'ejecutaraccioncontrolador', 'options': 'optionsFun'},
            name='{basename}-accion-REST',
            initkwargs={},detail=True
        ),
        Route(
            url=r'(?P<modulo>\w+)',
            mapping={'get': 'ejecutaraccioncontrolador', 'post': 'ejecutaraccioncontrolador', 'options': 'optionsFun'},
            name='{basename}-accion-REST',
            initkwargs={},detail=True
        ),
    ]

    def __init__(self, aplicacion, *args, **kwargs):
        self._aplicacion = aplicacion
        super().__init__(*args, **kwargs)

    def get_default_base_name(self, viewset):
        return self._aplicacion + ":"

    def registerDynamicModel(self, aplicacion, classViewSets=api_viewsets.YBControllerViewSet):
        self._aplicacion = aplicacion

        dict = {
            '_aplicacion': aplicacion,
        }

        raiz = self._aplicacion
        miView = type(raiz + "ModelViewSet", (classViewSets,), dict)
        self.register(aplicacion, miView, basename="api")

