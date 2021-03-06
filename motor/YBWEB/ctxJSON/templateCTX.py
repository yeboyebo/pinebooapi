#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Libreria de funciones para el tratamiento especial en la carga de templates
 y el uso del contexto
"""
from django.template import loader
from django.template import RequestContext

from YBUTILS import mylogging as log
from YBWEB.ctxJSON import DICTJSON

milog = log.getLogger("YBWEB.templateCTX")

# --------------------CONSTANTES------------------------------------
# YB_DIR_DEFECTO_TEMPLATES='YBWEB'
# YB_DIR_COMPONENTS='componentes'
# directorio_base=settings.YB_DIR_DEFECTO_TEMPLATES +"/"+"basechain"
# directorio_componentes=settings.YB_DIR_COMPONENTS
# directorio_base_componentes=settings.YB_DIR_DEFECTO_TEMPLATES +"/"+directorio_componentes
# posfijoctx="_context"


# --------------------GENERALES------------------------------------
def dametipo(nombretemplate):
    try:
        return nombretemplate.split('_')[0]
    except Exception:
        return 'otro'


def controlTerminahtml(nombre):
    if nombre.endswith(".html"):
        return nombre
    else:
        return nombre + ".html"


def controlTerminaJson(nombre):
    if nombre.endswith(".json"):
        return nombre
    else:
        return nombre + ".json"


def separatemplateModif(sNomTemplate):
    sSep = sNomTemplate.split("__")
    if len(sSep) > 1:
        return sSep[0], sSep[1]
    else:
        return sNomTemplate, None


def separatemplatePREFIJO(sNomTemplate):
    sSep = sNomTemplate.split(".")
    if len(sSep) > 1:
        # comprobamos que no sea la terminacion html
        if sSep[1].lower() == "json":
            return sNomTemplate, None
        else:
            return sSep[1], sSep[0]
    else:
        return sNomTemplate, None


def dameAPLICPREFIXMODIF(context):
    try:
        return context["YB"]["IDENT"]["APLIC"], context["YB"]["IDENT"]["PREFIX"], context["YB"]["IDENT"]["MODIF"]
    except Exception:
        return context["YB"]["IDENT"]["APLIC"], context["YB"]["IDENT"]["PREFIX"], None


# --------------------GENERACIONCHAIN------------------------------------
def damechainTemplate(aplic, prefix, nombretemplate):
    listNombres = []
    listDirectorios = []
    milist = []
    if aplic == "system":
        listDirectorios.append('portal/plantillas')
        listDirectorios.append('YBSYSTEM/plantillas')
    if not nombretemplate or nombretemplate == "formRecord":
        nombretemplate = "formrecord"
        listNombres.append(controlTerminaJson(prefix))
        listNombres.append(controlTerminaJson(nombretemplate))
    else:
        listNombres.append(controlTerminaJson(nombretemplate))
        listNombres.append(controlTerminaJson(prefix))
    listDirectorios.append(aplic + '/plantillas')
    listDirectorios.append('YBWEB/plantillas')
    for nombre in listNombres:
        for dirr in listDirectorios:
            milist.append(dirr + '/' + nombre)
    return milist


def damechainMasterTemplate(aplic, prefix, nombretemplate):
    listNombres = []
    listDirectorios = []
    milist = []
    if aplic == "system":
        listDirectorios.append('portal/plantillas')
        listDirectorios.append('YBSYSTEM/plantillas')
    listNombres.append(controlTerminaJson(nombretemplate + prefix))
    listNombres.append(controlTerminaJson(nombretemplate))
    listDirectorios.append(aplic + '/plantillas')
    listDirectorios.append('YBWEB/plantillas')
    for nombre in listNombres:
        for dirr in listDirectorios:
            milist.append(dirr + '/' + nombre)
    return milist


# --------------------CARGATEMPLATE------------------------------------
def generaRequestcontext(request, aplic, dict):
    return RequestContext(request, dict, current_app=aplic)


def cargaString(templatechain, requestcontext=None):
    return loader.render_to_string(templatechain)


def cargaDictJSON(templatechain, requestcontext=None):
    # return DICTJSON.fromJSON("{" + cargaString(templatechain, requestcontext) + "}")
    return DICTJSON.fromJSON(cargaString(templatechain, requestcontext))


def cargaPlantillaJSON(templatechain):
    try:
        oJson = cargaDictJSON(templatechain)
    except Exception:
        return None
    return oJson


def cargaMenuJSON(templatechain):
    try:
        original_json = cargaDictJSON(templatechain)
        new_json = {}

        keys_enabled = ["format", "default", "actions", "title"]

        for key in keys_enabled:
            if key in original_json:
                new_json[key] = original_json[key]

        visible_items = [x for x in original_json["items"] if "VISIBLE" not in x or x["VISIBLE"] is not False]
        new_json["items"] = visible_items

        return new_json

        # formato = None
        # logo = None
        # acciones = None
        # if "format" in oJson:
        #     formato = oJson["format"]
        # if "default" in oJson:
        #     logo = oJson["default"]
        # if "actions" in oJson:
        #     acciones = oJson["actions"]
        # itemsVisibles = [x for x in oJson["items"] if 'VISIBLE' not in x or x['VISIBLE'] is not False]
        # oJson = {
        #     "items": itemsVisibles,
        #     "format": formato,
        #     "default": logo,
        #     "actions": acciones
        # }
    except ValueError:
        raise NameError("Se encontró el template pero falló el parseo. Templatechain: {}".format(templatechain))
    except Exception:
        raise NameError("No se encontró un template válido. Templatechain: {}".format(templatechain))
    # return oJson
