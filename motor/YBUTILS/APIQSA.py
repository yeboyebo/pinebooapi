import sys
import traceback
try:
    from pineboolib.qsa import qsa
    from pineboolib import application
except:
    pass


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class APIQSA:

    def getuseracl(metodoHTTP, params, username):
        model = params["data"]["model"] if "model" in params["data"] else None
        method = params["data"]["method"] if "method" in params["data"] else None
        obj = qsa.from_project("formAPI").user_is_allowed(metodoHTTP, username, model, method)
        return obj

    def entry_point(metodoHTTP, modulo, username, params=None, accion=None):
        obj = qsa.from_project("formAPI").entry_point(metodoHTTP, modulo, username, params, accion)
        return obj

    def login(username, password):
        try:
            obj = qsa.from_project("formAPI").login(username, password)
        except Exception as e:
            print(bcolors.FAIL + "Excepcion " + str(e) + bcolors.ENDC)

            ex_type, ex_value, ex_traceback = sys.exc_info()

            # Extract unformatter stack traces as tuples
            trace_back = traceback.extract_tb(ex_traceback)

            # Format stacktrace
            stack_trace = list()

            for trace in trace_back:
                stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

            print(bcolors.WARNING)
            print("Exception type : %s " % ex_type.__name__)
            print("Exception message : %s" %ex_value)
            print("Stack trace : %s" %"\n".join(stack_trace))
            print(bcolors.ENDC)
            raise Exception(e)
        return obj
