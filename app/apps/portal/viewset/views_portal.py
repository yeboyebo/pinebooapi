# @class_declaration interna #
from YBLEGACY import qsatype


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context

# @class_declaration yblogin #
from os import path

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User, Group

from YBUTILS.viewREST import accessControl, factorias, cacheController
from YBUTILS.viewREST.helpers import decoradores

from YBWEB.ctxJSON import DICTJSON, templateCTX


class yblogin(interna):

    def yblogin_forbiddenError(self, request):
        return render(request, "portal/403.html")

    def yblogin_index(self, request):
        if request.GET:
            next_url = request.GET.get("next", None)
            if next_url:
                return HttpResponseRedirect(next_url)
        return HttpResponseRedirect("/dashboard")

        # history = cacheController.addHistory(request, None, None)
        # history = history["list"][history["pos"] - 1] if history["pos"] > 0 else history["list"][history["pos"]]
        # usuario = request.user.username
        # superuser = request.user.is_superuser

        # dctMenu = templateCTX.cargaMenuJSON("portal/menu_portal.json")
        # dctMenu = dctMenu["items"]
        # miMenu = accessControl.accessControl.dameDashboard(request.user, dctMenu)

        # # TODO
        # if len(miMenu) == 1:
        #     return HttpResponseRedirect(miMenu[0]["NAME"])
        # return render(request, "portal/index.html", {"aplic": "portal", "menuJson": miMenu, "usuario": usuario, "superuser": superuser, "history": history, "next": "/"})

    def yblogin_login(self, request, error=None):
        if not error:
            error = ""
        return render(request, "portal/login.html", {"error": error})

    def yblogin_signup(self, request, error):
        return render(request, "portal/signup.html", {"error": error})

    def yblogin_account(self, request, error):
        url = "/system/aqn_user/" + request.user.username
        return HttpResponseRedirect(url)
        # return render(request, "portal/account.html", {"error": error, "usuario": request.user})

    def yblogin_auth_login(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            username = request.POST.get("username", None).lower()
            password = request.POST.get("password", None)

            if action == "login":
                user = authenticate(username=username, password=password)
                if user is not None:
                    login_auth(request, user)
                else:
                    return self.iface.login(request, "Error de autentificación")
                accessControl.accessControl.registraAC()
                return HttpResponseRedirect("/")
        return self.iface.login(request)

    def yblogin_signup_request(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            password2 = request.POST.get("password2", None)

            if action == "signup":
                if password == password2:
                    try:
                        user = User.objects.create_user(username=username, password=password)
                        user.save()
                        return self.iface.signup(request, username + " Añadido")
                    except Exception as exc:
                        print(exc)
                        return self.iface.signup(request, "El usuario ya existe")
                else:
                    return self.iface.signup(request, "Las contraseñas no coinciden")
        return self.iface.signup(request, "")

    def yblogin_account_request(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            # username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            password2 = request.POST.get("password2", None)

            if action == "account":
                if password == password2:
                    try:
                        usuario = str(request.user.username)
                        user = User.objects.get(username=usuario)
                        user.set_password(str(password))
                        user.save()
                        return HttpResponseRedirect("/login")
                    except Exception as exc:
                        print(exc)
                        return self.iface.changePassword(request, "Error inesperado consulte administrador")
                else:
                    return self.iface.changePassword(request, "Las contraseñas no coinciden")
        return self.iface.changePassword(request, "")

    def yblogin_deleteUser(self, request, user):
        User.objects.filter(username=user).delete()
        return HttpResponseRedirect("/system/auth_user/master")

    def yblogin_logout(self, *args, **kwargs):
        return auth_views.logout(*args, **kwargs)

    def yblogin_system(self, request):
        history = cacheController.addHistory(request, None, None)
        history = history["list"][history["pos"] - 1] if history["pos"] > 0 else history["list"][history["pos"]]
        usuario = request.user.username
        nombreUsuario = request.user.first_name
        superuser = request.user.is_superuser
        dct_menu = templateCTX.cargaMenuJSON("portal/menu_system.json")
        # dct_menu = dct_menu["items"]
        if len(dct_menu["items"]) == 1:
            url = dct_menu["items"][0]["URL"]
            return HttpResponseRedirect("/" + url)
        mi_menu = accessControl.accessControl.dameDashboard(request.user, dct_menu["items"])

        return render(request, "YBWEB/dashboard.html", {"aplic": "portal", "menuJson": mi_menu, "usuario": usuario, "nombreUsuario": nombreUsuario, "superuser": superuser, "history": history, "next": "/"})

    def yblogin_newgroup(self, request, error):
        return render(request, "portal/newgroup.html", {"error": error})

    def yblogin_addgroup_request(self, request, username, error):
        groups = Group.objects.all()
        user = User.objects.get(username=username)
        groupobj = {}
        for g in groups:
            groupobj[g.name] = user.groups.filter(name=g.name).exists()
        return render(request, "portal/addgroup.html", {"error": error, "username": username, "groups": groupobj})

    def yblogin_newgroup_request(self, request):
        if request.method == "POST":
            action = request.POST.get("action", None)
            group = request.POST.get("group", None)
            if action == "newgroup":
                try:
                    Group.objects.create(name=group)
                    return self.iface.newgroup(request, " Añadido")
                except Exception as exc:
                    print(exc)
                    return self.iface.newgroup(request, "El grupo ya existe")
        return self.iface.newgroup(request, "")

    def yblogin_userTable(self, request, po=1):
        users = User.objects.exclude(is_staff=True).order_by("-date_joined")
        count = int(users.count() / 10)
        filtrado = False
        if request.method == "POST":
            search = request.POST.get("searchuser", None)
            users = users.filter(username__icontains=search)
            if search:
                filtrado = True
            print(users)

        pageSize = 10
        # users = User.objects.all()
        usersData = Paginator(users, pageSize).page(po)
        # print(users[0].__dict__)
        return render(request, "portal/users.html", {"users": usersData, "po": po, "pc": count, "filtrado": filtrado})

    def yblogin_groupTable(self, request, po=1):
        groups = Group.objects.all()
        count = int(groups.count() / 10)
        filtrado = False
        if request.method == "POST":
            search = request.POST.get("searchuser", None)
            groups = groups.filter(username__icontains=search)
            if search:
                filtrado = True
            print(groups)

        pageSize = 10
        groupsData = Paginator(groups, pageSize).page(po)
        return render(request, "portal/groups.html", {"groups": groupsData, "po": po, "pc": count, "filtrado": filtrado})

    def yblogin_deleteUserGroup(self, request, user, groupname):
        user = User.objects.filter(username=user)
        for g in user[0].groups.all():
            print(g)
        return HttpResponseRedirect("/userGroups/" + groupname)

    def yblogin_addGroup(self, request, username):
        if request.method == "POST":
            action = request.POST.get("action", None)
            group = request.POST.getlist("group")
            if action == "addGroup":
                try:
                    user = User.objects.get(username=username)
                    print(user)
                    user.groups.clear()
                    for g in group:
                        user.groups.add(Group.objects.get(name=g))
                    user.save()
                except Exception as e:
                    print(e)
        return self.iface.addgroup_request(request, username, '')

    def yblogin_userGroups(self, request, groupname, po=1):
        users = User.objects.filter(groups__name=groupname)
        count = int(users.count() / 10)
        filtrado = False
        if request.method == "POST":
            search = request.POST.get("searchuser", None)
            users = users.filter(username__icontains=search)
            if search:
                filtrado = True
            print(users)

        pageSize = 10
        # users = User.objects.all()
        usersData = Paginator(users, pageSize).page(po)
        return render(request, "portal/usergroups.html", {"users": usersData, "po": po, "pc": count, "filtrado": filtrado, "groupname": groupname})

    def yblogin_permissions_request(self, request):
        if request.method == "POST":
            return HttpResponseRedirect("/")

        reg = open(path.join(settings.PROJECT_ROOT, "config/urls.json")).read()
        oReg = DICTJSON.fromJSON(reg)
        models = {}

        for mod in oReg["models"]:
            for modelName in oReg["models"][mod]:
                acciones = factorias.FactoriaAccion.getAcciones(modelName, "I")
                models[modelName] = []
                for a in acciones:
                    models[modelName].append(a)
        # miaccion = factorias.FactoriaAccion.getAcciones("telsac", 'I')

        return render(request, "portal/permissions.html", {"models": models})

    def yblogin_acusers(self, request):
        return True

    def yblogin_acgroups(self, request):
        return True

    def yblogin_controlUser(self, request):
        return True

    def yblogin_controlGroup(self, request):
        return True

    def yblogin_changePassword(self, request, error):
        return render(request, "portal/account.html", {"error": error, "usuario": request.user})

    def __init__(self, context=None):
        super().__init__(context)

    def forbiddenError(self, request):
        return self.iface.yblogin_forbiddenError(request)

    @decoradores.check_authentication_iface
    def index(self, request):
        return self.iface.yblogin_index(request)

    def login(self, request, error=None):
        return self.iface.yblogin_login(request, error)

    def signup(self, request, error):
        return self.iface.yblogin_signup(request, error)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def account(self, request, error):
        return self.iface.yblogin_account(request, error)

    def auth_login(self, request):
        return self.iface.yblogin_auth_login(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def signup_request(self, request):
        return self.iface.yblogin_signup_request(request)

    @decoradores.check_authentication_iface
    def account_request(self, request):
        return self.iface.yblogin_account_request(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def deleteUser(self, request, user):
        return self.iface.yblogin_deleteUser(request, user)

    def logout(self, *args, **kwargs):
        return self.iface.yblogin_logout(*args, **kwargs)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def system(self, request):
        return self.iface.yblogin_system(request)

    def newgroup(self, request, error):
        return self.iface.yblogin_newgroup(request, error)

    def addgroup_request(self, request, username, error):
        return self.iface.yblogin_addgroup_request(request, username, error)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def newgroup_request(self, request):
        return self.iface.yblogin_newgroup_request(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def userTable(self, request, po=1):
        return self.iface.yblogin_userTable(request, po)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def groupTable(self, request, po=1):
        return self.iface.yblogin_groupTable(request, po)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def deleteUserGroup(self, request, user, groupname):
        return self.iface.yblogin_deleteUserGroup(request, user, groupname)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def addGroup(self, request, username):
        return self.iface.yblogin_addGroup(request, username)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def userGroups(self, request, groupname, po=1):
        return self.iface.yblogin_userGroups(request, groupname, po)

    @decoradores.check_system_authentication_iface
    def permissions_request(self, request):
        return self.iface.yblogin_permissions_request(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def acusers(self, request):
        return self.iface.yblogin_acusers(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def acgroups(self, request):
        return self.iface.yblogin_acgroups(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def controlUser(self, request):
        return self.iface.yblogin_controlUser(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def controlGroup(self, request):
        return self.iface.yblogin_controlGroup(request)

    @decoradores.check_authentication_iface
    @decoradores.check_system_authentication_iface
    def changePassword(self, request, error):
        return self.iface.yblogin_changePassword(request, error)

# @class_declaration head #
class head(yblogin):

    def __init__(self, context=None):
        super().__init__(context)

# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super().__init__(context)

# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)

