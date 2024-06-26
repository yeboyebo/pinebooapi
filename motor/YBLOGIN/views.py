from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth.models import User

from django.http import HttpResponse
import json
from rest_framework.authtoken.models import Token
from YBUTILS.APIQSA import APIQSA
from YBUTILS.viewREST import filtersPagination


def forbiddenError(request):
    return render(request, "users/403.html")


@login_required(login_url="/login")
def index(request):
    error = ""
    return render(request, "login/index.html", {"error": error})


# def login(request, error=None):
#     if not error:
#         error = ''
#     return render(request, 'login/login.html', {'error': error})


def signup(request, error):
    return render(request, "login/signup.html", {"error": error})


def account(request, error):
    return render(request, "login/account.html", {"error": error, "usuario": request.user})


def is_admin(user):
    return user.is_superuser


def auth_login(request):
    if request.method == "POST":
        action = request.POST.get("action", None)
        username = request.POST.get("username", None).lower()
        password = request.POST.get("password", None)

        if action == "login":
            user = authenticate(username=username, password=password)
            if user is not None:
                login_auth(request, user)
            else:
                return login(request, "Error de autentificación")
            # Despues de logear guardamos en cache los permisos del usuario
            # Hay que revisar que ocurre cuando cierra el navegador
            # accessControl.accessControl.registraAC()
            return HttpResponseRedirect("/")
            # return index(request)
    # context = {}
    return login(request)


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def signup_request(request):
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
                    return signup(request, username + " Añadido")
                except Exception as exc:
                    print(exc)
                    return signup(request, "El usuario ya existe")
            else:
                return signup(request, "Las contraseñas no coinciden")
    return signup(request, "")


@login_required(login_url="/login")
def account_request(request):
    if request.method == "POST":
        action = request.POST.get("action", None)
        # username = request.POST.get('username', None)
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
                    return account(request, "Error inesperado consulte administrador")
            else:
                return account(request, "Las contraseñas no coinciden")
    return account(request, "")


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/login")
def deleteUser(request, user):
    User.objects.filter(username=user).delete()
    return HttpResponseRedirect("/users")


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def forgot_password(request):
    try:
        params = json.loads(request.body.decode("utf-8"))
        username = params["username"]
    except Exception:
        username = request.POST.get("username", None)

    try:
        APIQSA.forgot_password(username, params)
        result = HttpResponse(json.dumps({}), status=200)

    except Exception as e:
        result = HttpResponse(json.dumps({"error": str(e)}), status=404)
    result["Access-Control-Allow-Origin"] = "*"
    return result

@csrf_exempt
def create_user(request):
    try:
        params = json.loads(request.body.decode("utf-8"))
        username = params["username"]
    except Exception:
        username = request.POST.get("username", None)

    try:
        APIQSA.create_user(username, params)
        result = HttpResponse(json.dumps({}), status=200)

    except Exception as e:
        result = HttpResponse(json.dumps({"error": str(e)}), status=404)
    result["Access-Control-Allow-Origin"] = "*"
    return result


@csrf_exempt
def check_hashlink(request, hash=None, type=None):
    if request.method == "POST":
        try:
            request_params = json.loads(request.body.decode("utf-8"))
        except Exception:
            request_params = request.POST

        action = request_params.get("action", None)

        if action == "change_password":
            hashcode = request_params.get("hashcode", None)
            password = request_params.get("password", None)
            loginType = request_params.get("loginType", None)
            params = {"password": password, "loginType": loginType}
            try:
                APIQSA.use_hashlink(hashcode, action, params)
                result = HttpResponse(json.dumps({}), status=200)

            except Exception as e:
                result = HttpResponse(json.dumps({"error": str(e)}), status=404)
            result["Access-Control-Allow-Origin"] = "*"
            return result
        if action == "create_user_confirm":
            hashcode = request_params.get("hashcode", None)
            user_data = request_params.get("user_data", None)
            loginType = request_params.get("loginType", None)
            params = {"user_data": user_data, "loginType": loginType}
            try:
                APIQSA.use_hashlink(hashcode, action, params)
                result = HttpResponse(json.dumps({}), status=200)

            except Exception as e:
                result = HttpResponse(json.dumps({"error": str(e)}), status=404)
            result["Access-Control-Allow-Origin"] = "*"
            return result        
    else:
        try:
            params = json.loads(request.body.decode("utf-8"))
            username = params["username"]
        except Exception:
            username = request.POST.get("username", None)

        try:
            APIQSA.check_hashlink(username, hash, type)
            result = HttpResponse(json.dumps({}), status=200)

        except Exception as e:
            result = HttpResponse(json.dumps({"error": str(e)}), status=404)
        result["Access-Control-Allow-Origin"] = "*"
        return result


@csrf_exempt
def token_auth(request):
    try:
        params = json.loads(request.body.decode("utf-8"))
        username = params["username"]
        password = params["password"]

    except Exception:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

    # Comprobamos usuario con pineboo
    try:
        apiuser = APIQSA.login(username, password)
        if type(apiuser) is int or type(apiuser) is str:
            authusername = apiuser
        else:
            authusername = apiuser["user"]
        if authusername:
            user = User.objects.filter(username=str(authusername))
            if user.exists():
                authuser = authenticate(username=str(authusername), password=password)
                if authuser is None:
                    user = User.objects.get(username__exact=str(authusername))
                    user.set_password(password)
                    user.save()
                    authuser = authenticate(username=str(authusername), password=password)
            else:
                user = User.objects.create_user(username=str(authusername), password=password)
                user.is_staff = False
                user.save()
                authuser = authenticate(username=str(authusername), password=password)
            token, _ = Token.objects.get_or_create(user=authuser)
            resul = HttpResponse(json.dumps({"token": token.key}), status=200)
    except Exception as e:
        resul = HttpResponse(json.dumps({"error": str(e)}), status=404)
    resul["Access-Control-Allow-Origin"] = "*"
    return resul


@csrf_exempt
def login(request):
    try:
        params = json.loads(request.body.decode("utf-8"))
        username = params["username"]
        password = params["password"]

    except Exception:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

    # Comprobamos usuario con pineboo
    try:
        apiuser = APIQSA.login(username, password, params)
        responseUser = {}
        if type(apiuser) is int or type(apiuser) is str:
            authusername = apiuser
            responseUser["user"] = apiuser
        else:
            authusername = apiuser["user"]
            responseUser = apiuser
        if authusername:
            user = User.objects.filter(username=str(authusername))
            if user.exists():
                authuser = authenticate(username=str(authusername), password=password)
                if authuser is None:
                    user = User.objects.get(username__exact=str(authusername))
                    user.set_password(password)
                    user.save()
                    authuser = authenticate(username=str(authusername), password=password)
            else:
                user = User.objects.create_user(username=str(authusername), password=password)
                user.is_staff = False
                user.save()
                authuser = authenticate(username=str(authusername), password=password)
            token, _ = Token.objects.get_or_create(user=authuser)
            print(responseUser)
            responseUser["token"] = token.key
            resul = HttpResponse(json.dumps(responseUser), status=200)
    except Exception as e:
        print("-----------------------")
        print(e)
        resul = HttpResponse(json.dumps({"error": str(e)}), status=404)
    resul["Access-Control-Allow-Origin"] = "*"
    return resul


@csrf_exempt
def end_point(request, name=None, action=None):
    request_params = []
    try:
        if request.body:
            try:
                request_params = json.loads(request.body.decode("utf-8"))
            except Exception:
                if request.method == "POST":
                    request_params = request.POST

        if request_params:
            APIQSA.end_point(name, action, request_params)
            result = HttpResponse(json.dumps({}), status=200)
        else:
            raise Exception("No hay datos")

    except Exception as e:
        result = HttpResponse(json.dumps({"error": str(e)}), status=404)

    result["Access-Control-Allow-Origin"] = "*"
    return result

@csrf_exempt
def public(request, hash=None, action=None):
    # Faltaría funcionalidad para recpger los parámetros get
    method = request.method
    # print("ESTOY EN PUBLIC CON EL METODO: ", method)    
    if method not in ["GET","POST"]:
        raise Exception("Accion no permitida")
    try:
        request_params = json.loads(request.body.decode("utf-8"))
    except Exception:
        if method == "POST":
            request_params = request.POST
        if method == "GET":
            request_params = request.GET
    params = filtersPagination._generaGetParam(request_params)    
    try:
        obj = APIQSA.public(method, hash, action, params)
        result = HttpResponse(json.dumps(obj), status=200, content_type='application/json')
    except Exception as e:
        result = HttpResponse(json.dumps({"error": str(e)}), status=404)

    result['Access-Control-Allow-Origin'] = '*'  

    return result
