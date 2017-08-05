class Func_Type(object):
        form = int()
        param_cnt = int()
        param_types = []
        return_cnt = int()
        return_type = []


class Global_Type():
        content_type = int()
        mutability = int()


class Resizable_Limits():
        flags = int()
        initial = int()
        maximum = int()


class Table_Type():
        element_type = int()
        limit = Resizable_Limits()


class External_Kind(object):
    Function = 0
    Table = 1
    Memory = 2
    Global = 3


class Memory_Type():
        limits = [Resizable_Limits()]


# @DEVI-FIXME-
class Init_Expr(object):
    pass


class Type_Section(object):
        count = int()
        func_types = [Func_Type()]


class Import_Entry():
        module_len = int()
        module_str = []
        field_len = int()
        field_str = []
        kind = int()
        type = int()


class Import_Section():
        count = int()
        import_entry = [Import_Entry()]


class Function_Section():
        count = int()
        type_section_index = [int()]


class Table_Section():
        count = int()
        table_types = [Table_Type()]


class Memory_Section():
        count = int()
        memory_types = [Resizable_Limits()]


class Global_Variable():
        global_type = Global_Type()
        init_expr = []


class Global_Section():
        count = int()
        global_variables = [Global_Variable()]


class Export_Entry():
        field_len = int()
        field_str = []
        kind = int()
        index = int()


class Export_Section(object):
        count = int()
        export_entries = [Export_Entry()]


class Start_Section():
    function_section_index = int()


class Elem_Segment(object):
        index = int()
        offset = []
        num_elem = int()
        elems = []


class Element_Section(object):
        count = int()
        elem_segments = [Elem_Segment()]


class Local_Entry(object):
    def __init__(self, count, type):
        self.count = count
        self.type = type


class Func_Body(object):
    def __init__(self, body_size, local_count, locals, code, end):
        self.body_size = body_size
        self.local_count = local_count
        self.locals = []
        self.locals = local_entry
        self.code = code
        self.end = end


class Code_Section(object):
    def __init__(self, count, func_body):
        self.count = count
        self.func_body = func_body


class Data_Segment():
    index = int()
    offset = []
    size = int()
    data = []


class Data_Section():
    count = int()
    data_segments = [Data_Segment()]


class Name_Type():
    Module = 0
    Function = 1
    Local = 2


class Name_Section_Entry(object):
    def __init__(self, name_type, name_payload_len, name_payload_data):
        self.name_type = name_type
        self.name_payload_len = name_payload_len
        self.name_payload_data = name_payload_data


class Name_Section(object):
    def __init__(self, name_section_entry):
        self.name_section_entry = []
        self.name_section_entry = name_section_entry


class Module_Name(object):
    def __init__(self, name_len, name_str):
        self.name_len = name_len
        self.name_str = name_str


class Naming(object):
    def __init__(self, index, name_len, name_str):
        self.index = index
        self.name_len = name_len
        self.name_str = name_str


class Name_Map(object):
    def __init__(self, count, naming):
        self.count = count
        self.naming = []
        self.naming = naming
