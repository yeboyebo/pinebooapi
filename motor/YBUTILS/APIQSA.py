try:
    from pineboolib.qsa import qsa
    from pineboolib import application
except:
    pass

class APIQSA:

    def entry_point(metodoHTTP, modulo, username, params=None, accion=None):
        print("ejecutar controlador api")
        # obj = qsa.from_project("formAPI").hola()
        obj = qsa.from_project("formAPI").entry_point(metodoHTTP, modulo, username, params, accion)
        return obj

    def login(username, password):
        # obj = qsa.from_project("formAPI").hola()
        obj = qsa.from_project("formAPI").login(username, password)
        return obj