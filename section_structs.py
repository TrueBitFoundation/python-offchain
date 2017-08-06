class Func_Type():
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


class External_Kind():
    Function = 0
    Table = 1
    Memory = 2
    Global = 3


class Memory_Type():
    limits = [Resizable_Limits()]


# @DEVI-FIXME-
class Init_Expr():
    pass


class Type_Section():
    count = []
    func_types = []


class Import_Entry():
    module_len = int()
    module_str = []
    field_len = int()
    field_str = []
    kind = int()
    type = int()


class Import_Section():
    count = []
    import_entry = []


class Function_Section():
    count = []
    type_section_index = [int()]


class Table_Section():
    count = []
    table_types = []


class Memory_Section():
    count = []
    #Resizable_Limits
    memory_types = []


class Global_Variable():
    global_type = Global_Type()
    init_expr = []


class Global_Section():
    count = []
    # Global_Variable
    global_variables = []


class Export_Entry():
    field_len = int()
    field_str = []
    kind = int()
    index = int()


class Export_Section():
    count = []
    # Export_Entry
    export_entries = []


class Start_Section():
    function_section_index = []


class Elem_Segment():
    index = int()
    offset = []
    num_elem = int()
    elems = []


class Element_Section():
    count = []
    # Elem_Segment
    elem_segments = []


class Local_Entry():
    count = int()
    type = int()


class WASM_Ins():
    opcode = int()
    operands = []


class Func_Body():
    body_size = int()
    local_count = int()
    # Local_Entry
    locals = []
    # WASM_Ins
    code = []
    end = int()


class Code_Section():
    count = []
    # Func_Body
    func_bodies = []


class Data_Segment():
    index = int()
    offset = []
    size = int()
    data = []


class Data_Section():
    count = []
    # Data_Segment
    data_segments = []


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


class Module():
    def __init__(self, type_section, import_section, function_section,
                 table_section, memory_section, global_section, export_section,
                 start_section, element_section, code_section, data_section):
        self.type_section = Type_Section()
        self.import_section = Import_Section()
        self.function_section = Function_Section()
        self.table_section = Table_Section()
        self.memory_section = Memory_Section()
        self.global_section = Global_Section()
        self.export_section = Export_Section()
        self.start_section = Start_Section()
        self.element_section = Element_Section()
        self.code_section = Code_Section()
        self.data_section = Data_Section()
