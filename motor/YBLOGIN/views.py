from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth.models import User

from django.http import HttpResponse
import json
from rest_framework.authtoken.models import Token


def forbiddenError(request):
    return render(request, 'users/403.html')


@login_required(login_url='/login')
def index(request):
    error = ''
    return render(request, 'login/index.html', {'error': error})

def login(request, error=None):
    if not error:
        error = ''
    return render(request, 'login/login.html', {'error': error})


def signup(request, error):
    return render(request, 'login/signup.html', {'error': error})


def account(request, error):
    return render(request, 'login/account.html', {'error': error, 'usuario': request.user})


def is_admin(user):
    return user.is_superuser


def auth_login(request):
    if request.method == 'POST':
        action = request.POST.get('action', None)
        username = request.POST.get('username', None).lower()
        password = request.POST.get('password', None)

        if action == 'login':
            user = authenticate(username=username, password=password)
            if user is not None:
                login_auth(request, user)
            else:
                return login(request, 'Error de autentificación')
            # Despues de logear guardamos en cache los permisos del usuario
            # Hay que revisar que ocurre cuando cierra el navegador
            # accessControl.accessControl.registraAC()
            return HttpResponseRedirect("/")
            # return index(request)
    # context = {}
    return login(request)


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def signup_request(request):
    if request.method == 'POST':
        action = request.POST.get('action', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if action == 'signup':
            if password == password2:
                try:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    return signup(request, username + ' Añadido')
                except Exception as exc:
                    print(exc)
                    return signup(request, 'El usuario ya existe')
            else:
                return signup(request, 'Las contraseñas no coinciden')
    return signup(request, '')


@login_required(login_url='/login')
def account_request(request):
    if request.method == 'POST':
        action = request.POST.get('action', None)
        # username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if action == 'account':
            if password == password2:
                try:
                    usuario = str(request.user.username)
                    user = User.objects.get(username=usuario)
                    user.set_password(str(password))
                    user.save()
                    return HttpResponseRedirect("/login")
                except Exception as exc:
                    print(exc)
                    return account(request, 'Error inesperado consulte administrador')
            else:
                return account(request, 'Las contraseñas no coinciden')
    return account(request, '')


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def deleteUser(request, user):
    User.objects.filter(username=user).delete()
    return HttpResponseRedirect('/users')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def token_auth(request):
    print(request.POST)
    try:
        params = json.loads(request.body.decode("utf-8"))
        username = params["username"]
        password = params["password"]

    except Exception:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
    print(username,"________", password)

    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
    else:
        return HttpResponse(json.dumps({'error': 'Usuario y contraseña no coinciden'}),
                        status=404)
    resul = HttpResponse(json.dumps({'token': token.key}), status=200)
    resul['Access-Control-Allow-Origin'] = '*'
    return resul

