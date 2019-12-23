import importlib

from django.conf import settings


class accessControl:
    pass
    # @classmethod
    # def registraAC(cls):
    #     """
    #         Almacenamos las restringiones de acceso del usuario
    #         Para ello tomamos primero las restringiones del grupo y despues las del propio usuario
    #         de forma que las restringiones del usuario priman sobre las de su grupo.
    #         Tipo: app, tabla, accion, template, default
    #         permisos: --, r-, rw
    #     """
    #     # print("registramos acl")
    #     acl = {}

    #     modelos = None
    #     if settings.IS_SVN:
    #         modelos = importlib.import_module("YBSYSTEM.models.flsisppal.models")
    #     else:
    #         modelos = importlib.import_module("models.fllogin.models")

    #     sis_acl = getattr(modelos, "mtd_sis_acl", None)
    #     user = cacheController.getUser()

    #     # Registra acceso de grupos
    #     # usuario.groups.filter(name='xxx').exists()
    #     groups = user.groups.all()
    #     if sis_acl:
    #         for g in groups:
    #             acl_group = sis_acl.objects.filter(grupo=g)
    #             if acl_group:
    #                 for obj in acl_group:
    #                     # print(obj.valor, obj.tipo)
    #                     app = None
    #                     if obj.tipo == "tabla":
    #                         # Sacamos su app
    #                         app = clasesBase.getAplicFromTemplate(obj.valor)
    #                     else:
    #                         app = obj.valor
    #                     # print(app)
    #                     acl[obj.valor] = {"tipo": obj.tipo, "permiso": obj.permiso, "app": app}

    #     # Registra acceso de usuario
    #     try:
    #         acl_user = sis_acl.objects.filter(usuario=user)
    #         for obj in acl_user:
    #             # print(obj.valor, obj.tipo)
    #             app = None
    #             if obj.tipo == "tabla":
    #                 # Sacamos su app
    #                 app = clasesBase.getAplicFromTemplate(obj.valor)
    #             else:
    #                 app = obj.valor
    #             # print(app)
    #             acl[obj.valor] = {"tipo": obj.tipo, "permiso": obj.permiso, "app": app}
    #         cacheController.setSessionVariable("acl", acl)
    #     except Exception:
    #         pass
    #     return True

    # def getAcl(user, group):
    #     modelos = None
    #     if settings.IS_SVN:
    #         modelos = importlib.import_module("YBSYSTEM.models.flsisppal")
    #     else:
    #         modelos = importlib.import_module("models.fllogin")

    #     sis_acl = getattr(modelos, "mtd_sis_acl", None)
    #     acl = {}
    #     if group:
    #         acl_group = sis_acl.objects.filter(grupo=group)
    #         if acl_group:
    #             for obj in acl_group:
    #                 acl[obj.valor] = {"tipo": obj.tipo, "permiso": obj.permiso}

    #     if user:
    #         user = user[0]
    #         groups = user.groups.all()
    #         if sis_acl:
    #             for g in groups:
    #                 acl_group = sis_acl.objects.filter(grupo=g)
    #                 if acl_group:
    #                     for obj in acl_group:
    #                         acl[obj.valor] = {"tipo": obj.tipo, "permiso": obj.permiso}
    #             acl_user = sis_acl.objects.filter(usuario=user.username)
    #             for obj in acl_user:
    #                 acl[obj.valor] = {"tipo": obj.tipo, "permiso": obj.permiso}
    #     return acl

    # def dameTitle():
    #     title = settings.TITLE or "AQNext"
    #     return title

    # def dameDashboard(user, dashboardDICT):
    #     # print("aqui")
    #     acl = cacheController.getSessionVariable("acl")
    #     deleteItem = []
    #     # print(acl)
    #     if acl:
    #         for db in range(len(dashboardDICT)):
    #             if "default" in acl and acl['default']['tipo'] == "tabla":
    #                 if dashboardDICT[db]["NAME"] not in acl:
    #                     deleteItem.append(db)
    #             if dashboardDICT[db]["NAME"] in acl:
    #                 if acl[dashboardDICT[db]["NAME"]]["permiso"] == '--':
    #                     if not user.groups.filter(name__in=['clientes']).exists():
    #                         deleteItem.append(db)
    #         # print(deleteItem)
    #         if len(deleteItem) > 0:
    #             leng = len(deleteItem)
    #             fin = 0
    #             while fin != leng:
    #                 del(dashboardDICT[deleteItem[leng - (fin + 1)]])
    #                 fin = fin + 1

    #     return dashboardDICT

    # def checkAccess(request, name, *args, **kwargs):
    #     # usuario = request.request.user
    #     isloginmodel = False

    #     if not settings.IS_SVN:
    #         loginmodels = importlib.import_module("models.fllogin")
    #         isloginmodel = getattr(loginmodels, "mtd_" + request._prefix, None)

    #     sysmodels = importlib.import_module("YBSYSTEM.models.flsisppal")
    #     issysmodel = getattr(sysmodels, "mtd_" + request._prefix, None)
    #     if issysmodel or isloginmodel:
    #         # Solo superusuarios pueden acceder si es una tabla de flsisppal o fllogin.
    #         if not request.request.user.is_superuser:
    #             return False

    #     if not name == "invocaAQdashboard" and not name == "list":
    #         # print(kwargs, name, args, request._prefix)
    #         template = None
    #         if "template" in kwargs:
    #             template = kwargs["template"]
    #         acl = cacheController.getSessionVariable("acl")
    #         # print(acl)
    #         # Aqui hay que sacar le modelo y ver si hay funcion
    #         if not accessControl.checkModelAccess(request, name, acl, args, kwargs):
    #             return False
    #         if not acl:
    #             return True
    #         # print(acl, "______", request._prefix)
    #         if request._prefix in acl and acl[request._prefix]["tipo"] == "tabla":
    #             if acl[request._prefix]['permiso'] == '--':
    #                 return False
    #         elif template and template in acl and acl[template]["tipo"] == "template":
    #             if acl[template]['permiso'] == '--':
    #                 return False
    #         else:
    #             # Si ni prefix ni template estan en acl miramos si hay un default
    #             if "default" in acl and "accion" not in kwargs:
    #                 if acl["default"]["tipo"] in ["tabla", "template"] and acl["default"]['permiso'] == '--':
    #                     return False

    #     return True

    # def checkAction(request, name, *args, **kwargs):
    #     # accion = kwargs["accion"]
    #     acl = cacheController.getSessionVariable("acl")
    #     if not accessControl.checkModelAccess(request, name, acl, args, kwargs):
    #         return False
    #     if not acl:
    #         return True
    #     if request._prefix in acl:
    #         if acl[request._prefix]['permiso'][1] == '-':
    #             return False
    #     # if accion in ["update", "create"] and request._prefix in acl:
    #     #     if acl[request._prefix]['permiso'][1] == '-':
    #     #         return False
    #     # elif accion in acl:
    #     #     if acl[accion]['permiso'][1] == '-':
    #     #         return False
    #     return True

    # def checkModelAccess(request, name, acl, rest, otrosargs, *args, **kwargs):
    #     base_serializer, meta_model = factorias.FactoriaSerializadoresBase.getSerializer(request._prefix, None)
    #     pk = "master"
    #     name = "master"
    #     if "pk" in otrosargs:
    #         pk = otrosargs["pk"]
    #         name = "formRecord"
    #     if "template" in otrosargs:
    #         name = otrosargs["template"]
    #     accion = None
    #     if "accion" in otrosargs:
    #         accion = otrosargs["accion"]
    #         name = "accion"

    #     resul = meta_model.check_permissions(meta_model, request._prefix, pk, name, acl, accion)
    #     return resul
