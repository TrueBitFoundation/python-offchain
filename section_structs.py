class func_type(object):
    def __init__(self, form, param_cnt, param_types, return_cnt, return_type):
        self.form = form
        self.param_cnt = param_cnt
        self.param_types = param_types
        self.return_cnt = return_cnt
        self.return_type = return_type


class global_type(object):
    def __init__(self, content_type, mutability):
        self.content_type = content_type
        self.mutability = mutability


class table_type(object):
    def __init__(self, element_type, limits):
        self.element_type = element_type
        self.limits = limits


class memory_type(object):
    def __init__(self, limits):
        self.limits = limits


class external_kind(object):
    Function = 0
    Table = 1
    Memory = 2
    Global = 3


class resizable_limits(object):
    def __init__(self, flags, initial, maximum):
        self.flags = flags
        self.initial = initial
        self.maximum = maximum


# @DEVI-FIXME-
class init_expr(object):
    pass


class type_section(object):
    def __init__(self, count, func_type):
        self.count = count
        self.func_type = []
        self.func_type = func_type


class import_section(object):
    def __init__(self, count, import_entry):
        self.count = count
        self.import_entry = []
        self.import_entry = import_entry


class import_entry(object):
    def __init__(self, module_len, module_str, field_len,
                 field_str, kind, type):
        self.module_len = module_len
        self.module_str = module_str
        self.field_len = field_len
        self.field_str = field_str
        self.kind = kind
        self.type = type


class function_section(object):
    def __init__(self, count, type_section_index):
        self.count = count
        self.type_section_index = type_section_index


class table_section(object):
    def __init__(self, count, table_type):
        self.count = count
        self.table_type = table_type


class memory_section(object):
    def __init__(self, count, memory_type):
        self.count = count
        self.memory_type = memory_type


class global_variable(object):
    def __init__(self, global_type, init_expr):
        self.global_type = global_type
        self.init_expr = init_expr


class global_section(object):
    def __init__(self, count, global_varaible):
        self.count = count
        self.global_variable = []
        self.global_varaible = global_varaible


class export_entry(object):
    def __init__(self, field_len, field_str, kind, index):
        self.field_len = field_len
        self.field_str = field_str
        self.kind = kind
        self.index = index


class export_section(object):
    def __init__(self, count, export_entry):
        self.count = count
        self.export_entry = []
        self.export_entry = export_entry


class start_section():
    def __init__(self, function_section_index):
        self.function_section_index = function_section_index


class elem_segment(object):
    def __init__(self, index, offset, num_elem, elems):
        self.index = index
        self.offset = offset
        self.num_elem = num_elem
        self.elems = []
        self.elems = elems


class element_section(object):
    def __init__(self, count, elem_segment):
        self.count = count
        self.elem_segment = []
        self.elem_segment = elem_segment


class local_entry(object):
    def __init__(self, count, type):
        self.count = count
        self.type = type


class func_body(object):
    def __init__(self, body_size, local_count, locals, code, end):
        self.body_size = body_size
        self.local_count = local_count
        self.locals = []
        self.locals = local_entry
        self.code = code
        self.end = end


class code_section(object):
    def __init__(self, count, func_body):
        self.count = count
        self.func_body = func_body


class data_segment(object):
    def __int__(self, index, offset, size, data):
        self.index = index
        self.offset = offset
        self.size = size
        self.data = data


class data_section(object):
    def __init__(self, count, data_segment):
        self.count = count
        self.data_segment = []
        self.data_segment = data_segment


class name_type():
    Module = 0
    Function = 1
    Local = 2


class name_section_entry(object):
    def __init__(self, name_type, name_payload_len, name_payload_data):
        self.name_type = name_type
        self.name_payload_len = name_payload_len
        self.name_payload_data = name_payload_data


class name_section(object):
    def __init__(self, name_section_entry):
        self.name_section_entry = []
        self.name_section_entry = name_section_entry


class module_name(object):
    def __init__(self, name_len, name_str):
        self.name_len = name_len
        self.name_str = name_str


class naming(object):
    def __init__(self, index, name_len, name_str):
        self.index = index
        self.name_len = name_len
        self.name_str = name_str


class name_map(object):
    def __init__(self, count, naming):
        self.count = count
        self.naming = []
        self.naming = naming
