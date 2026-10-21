"""Autenticación por token con registro opcional de fallos para diagnóstico.

Con LOG_AUTH_FAILURES=True se registra cada token rechazado (solo los 6 primeros
caracteres) y cada cabecera Authorization que no se reconoce, para averiguar qué
envían los clientes cuando falla la autenticación.
"""
import logging
import os

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

LOGGER = logging.getLogger("YBUTILS.auth")
LOG_FAILURES = os.environ.get("LOG_AUTH_FAILURES", "False").lower() in ("1", "true")


def _registra(evento, request, motivo):
    cabecera = request.META.get("HTTP_AUTHORIZATION", "")
    partes = cabecera.split()
    clave = partes[1] if len(partes) > 1 else ""
    LOGGER.warning(
        "%s path=%s motivo=%s esquema=%s token_prefijo=%s token_len=%s ip=%s ua=%s",
        evento,
        request.path,
        motivo,
        partes[0][:10] if partes else "",
        clave[:6],
        len(clave),
        request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR")),
        request.META.get("HTTP_USER_AGENT", "")[:120],
    )


class YBTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            resultado = super().authenticate(request)
        except exceptions.AuthenticationFailed as exc:
            if LOG_FAILURES:
                _registra("AUTH_FAIL", request, exc.detail)
            raise

        if resultado is None and LOG_FAILURES:
            cabecera = request.META.get("HTTP_AUTHORIZATION", "")
            if cabecera and cabecera.split()[0].lower() not in ("token", "basic"):
                _registra("AUTH_ANON", request, "cabecera no reconocida")
        return resultado
