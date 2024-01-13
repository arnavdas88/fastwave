class Global(object):
    def __init__(self):
        global global_stack
        try:
            global_stack
        except:
            global_stack = {}

    def __call__(self, name):
        global global_stack
        return global_stack[name]

    def __setattr__(self, name, value):
        global global_stack
        global_stack[name] = value

    def __getattribute__(self, name):
        global global_stack
        # pprint(global_stack)
        # print("SIZE OF GLOBAL STACK : ", sys.getsizeof(global_stack))
        return global_stack.get(name, None)
