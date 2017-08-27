from OpCodes import *
from utils import Colors


# takes the machinestate, opcode and operand to run. updates the machinestate
class Execute():
    def __init__(self, machinestate):
        self.machinestate = machinestate
        self.opcodeint = ''
        self.immediates = []

    def getInstruction(self, opcodeint, immediates):
        self.opcodeint = opcodeint
        self.immediates = immediates

    def callExecuteMethod(self):
        runmethod = self.instructionUnwinder(self.opcodeint, self.immediates, self.machinestate)
        #print (self.opcodeint + ' ' + self.immediates)
        try:
            runmethod(self.opcodeint, self.immediates)
        except IndexError:
            # trap
            print(Colors.red + 'bad stack access.' + Colors.ENDC)

    def instructionUnwinder(self, opcodeint, immediates, machinestate):
        if opcodeint == 0:
            return(self.run_unreachable)
        elif opcodeint == 1:
            return(self.run_nop)
        elif opcodeint == 2:
            return(self.run_block)
        elif opcodeint == 3:
            return(self.run_loop)
        elif opcodeint == 4:
            return(self.run_if)
        elif opcodeint == 5:
            return(self.run_else)
        elif opcodeint == 11:
            return(self.run_end)
        elif opcodeint == 12:
            return(self.run_br)
        elif opcodeint == 13:
            return(self.run_br_if)
        elif opcodeint == 14:
            return(self.run_br_table)
        elif opcodeint == 15:
            return(self.run_return)
        elif opcodeint == 16:
            return(self.run_call)
        elif opcodeint == 17:
            return(self.run_call_indirect)
        elif opcodeint == 26:
            return(self.run_drop)
        elif opcodeint == 27:
            return(self.run_select)
        elif opcodeint == 32:
            return(self.run_getlocal)
        elif opcodeint == 33:
            return(self.run_setlocal)
        elif opcodeint == 34:
            return(self.run_teelocal)
        elif opcodeint == 35:
            return(self.run_getglobal)
        elif opcodeint == 36:
            return(self.run_setglobal)
        elif opcodeint >= 40 and opcodeint <= 53:
            return(self.run_load)
        elif opcodeint >= 54 and opcodeint <= 62:
            return(self.run_store)
        elif opcodeint == 63:
            return(self.run_current_memory)
        elif opcodeint == 64:
            return(self.run_grow_memory)
        elif opcodeint >= 65 and opcodeint <= 68:
            return(self.run_const)
        elif opcodeint == 69 or opcodeint == 80:
            return(self.run_eqz)
        elif opcodeint == 70 or opcodeint == 81 or opcodeint == 91 or opcodeint == 97:
            return(self.run_eq)
        elif opcodeint == 71 or opcodeint == 82 or opcodeint == 92 or opcodeint == 98:
            return(self.run_ne)
        elif opcodeint == 72 or opcodeint == 83:
            return(self.run_lt_s)
        elif opcodeint == 73 or opcodeint == 84:
            return(self.run_lt_u)
        elif opcodeint == 74 or opcodeint == 85:
            return(self.run_gt_s)
        elif opcodeint == 75 or opcodeint == 86:
            return(self.run_gt_u)
        elif opcodeint == 76 or opcodeint == 87:
            return(self.run_le_s)
        elif opcodeint == 77 or opcodeint == 88:
            return(self.run_le_u)
        elif opcodeint == 78 or opcodeint == 89:
            return(self.run_ge_s)
        elif opcodeint == 79 or opcodeint == 90:
            return(self.run_ge_u)
        elif opcodeint == 93 or opcodeint == 99:
            return(self.run_lt)
        elif opcodeint == 94 or opcodeint == 100:
            return(self.run_gt)
        elif opcodeint == 95 or opcodeint == 101:
            return(self.run_le)
        elif opcodeint == 96 or opcodeint == 102:
            return(self.run_ge)
        elif opcodeint == 103 or opcodeint == 121:
            return(self.run_clz)
        elif opcodeint == 104 or opcodeint == 122:
            return(self.run_ctz)
        elif opcodeint == 105 or opcodeint == 123:
            return(self.run_popcnt)
        elif opcodeint == 106 or opcodeint == 124 or opcodeint == 146 or opcodeint == 160:
            return(self.run_add)
        elif opcodeint == 107 or opcodeint == 125 or opcodeint == 147 or opcodeint == 161:
            return(self.run_sub)
        elif opcodeint == 108 or opcodeint == 126 or opcodeint == 148 or opcodeint == 162:
            return(self.run_mul)
        elif opcodeint == 109 or opcodeint == 127:
            return(self.run_div_s)
        elif opcodeint == 110 or opcodeint == 128:
            return(self.run_div_u)
        elif opcodeint == 111 or opcodeint == 129:
            return(self.run_rem_s)
        elif opcodeint == 112 or opcodeint == 130:
            return(self.run_rem_u)
        elif opcodeint == 113 or opcodeint == 131:
            return(self.run_and)
        elif opcodeint == 114 or opcodeint == 132:
            return(self.run_or)
        elif opcodeint == 115 or opcodeint == 133:
            return(self.run_xor)
        elif opcodeint == 116 or opcodeint == 134:
            return(self.run_shl)
        elif opcodeint == 117 or opcodeint == 135:
            return(self.run_shr_s)
        elif opcodeint == 118 or opcodeint == 136:
            return(self.run_shr_u)
        elif opcodeint == 119 or opcodeint == 137:
            return(self.run_rotl)
        elif opcodeint == 120 or opcodeint == 138:
            return(self.run_rotr)
        elif opcodeint == 139 or opcodeint == 153:
            return(self.run_abs)
        elif opcodeint == 140 or opcodeint == 154:
            return(self.run_neg)
        elif opcodeint == 141 or opcodeint == 155:
            return(self.run_ceil)
        elif opcodeint == 142 or opcodeint == 156:
            return(self.run_floor)
        elif opcodeint == 143 or opcodeint == 157:
            return(self.run_trunc)
        elif opcodeint == 144 or opcodeint == 158:
            return(self.run_nearest)
        elif opcodeint == 145 or opcodeint == 159:
            return(self.run_sqrt)
        elif opcodeint == 149 or opcodeint == 163:
            return(self.run_div)
        elif opcodeint == 150 or opcodeint == 164:
            return(self.run_min)
        elif opcodeint == 151 or opcodeint == 165:
            return(self.run_max)
        elif opcodeint == 152 or opcodeint == 166:
            return(self.run_copysign)
        elif opcodeint == 167:
            return(self.run_i32wrapi64)
        elif opcodeint == 168:
            return(self.run_i32trunc_sf32)
        elif opcodeint == 169:
            return(self.run_i32trunc_uf32)
        elif opcodeint == 170:
            return(self.run_i32trunc_sf64)
        elif opcodeint == 171:
            return(self.run_i32trunc_uf64)
        elif opcodeint == 172:
            return(self.run_i64extend_si32)
        elif opcodeint == 173:
            return(self.run_i64extend_ui3o)
        elif opcodeint == 174:
            return(self.run_i64trunc_sf32)
        elif opcodeint == 175:
            return(self.run_i64trunc_uf32)
        elif opcodeint == 176:
            return(self.run_i64trunc_sf64)
        elif opcodeint == 177:
            return(self.run_i64trunc_uf64)
        elif opcodeint == 178:
            return(self.run_f32convert_si32)
        elif opcodeint == 179:
            return(self.run_f32convert_ui32)
        elif opcodeint == 180:
            return(self.run_f32convert_si64)
        elif opcodeint == 181:
            return(self.run_f32convert_ui64)
        elif opcodeint == 182:
            return(self.run_f32demotef64)
        elif opcodeint == 183:
            return(self.run_f64convert_si32)
        elif opcodeint == 184:
            return(self.run_f64convert_ui32)
        elif opcodeint == 185:
            return(self.run_f64convert_si64)
        elif opcodeint == 186:
            return(self.run_f64convert_ui64)
        elif opcodeint == 187:
            return(self.run_f64promotef32)
        elif opcodeint == 188:
            return(self.run_i32reinterpretf32)
        elif opcodeint == 189:
            return(self.run_i64reinterpretf64)
        elif opcodeint == 190:
            return(self.run_f32reinterpreti32)
        elif opcodeint == 191:
            return(self.run_f64reinterpreti64)
        else:
            raise Exception(Colors.red + 'unknown opcode' + Colors.ENDC)


    def run_unreachable(self, opcodeint, immediates):
        # trap
        raise Exception(Colors.red + "running an unreachable function..." + Colors.ENDC)

    def run_nop(self, opcodeint, immediates):
        pass

    def run_block(self, opcodeint, immediates):
        pass

    def run_loop(self, opcodeint, immediates):
        pass

    def run_if(self, opcodeint, immediates):
        pass

    def run_else(self, opcodeint, immediates):
        pass

    def run_end(self, opcodeint, immediates):
        pass

    def run_br(self, opcodeint, immediates):
        pass

    def run_br_if(self, opcodeint, immediates):
        pass

    def run_br_table(self, opcodeint, immediates):
        pass

    def run_return(self, opcodeint, immediates):
        pass

    def run_call(self, opcodeint, immediates):
        pass

    def run_call_indirect(self, opcodeint, immediates):
        pass

    def run_drop(self, opcodeint, immediates):
        pass

    def run_select(self, opcodeint, immediates):
        pass

    def run_getlocal(self, opcodeint, immediates):
        pass

    def run_setlocal(self, opcodeint, immediates):
        pass

    def run_teelocal(self, opcodeint, immediates):
        pass

    def run_getglobal(self, opcodeint, immediates):
        pass

    def run_setglobal(self, opcodeint, immediates):
        pass

    def run_load(self, opcodeint, immediates):
        if opcodeint == 40:
            pass
        elif opcodeint == 41:
            pass
        elif opcodeint == 42:
            pass
        elif opcodeint == 43:
            pass
        elif opcodeint == 44:
            pass
        elif opcodeint == 45:
            pass
        elif opcodeint == 46:
            pass
        elif opcodeint == 47:
            pass
        elif opcodeint == 48:
            pass
        elif opcodeint == 49:
            pass
        elif opcodeint == 50:
            pass
        elif opcodeint == 51:
            pass
        elif opcodeint == 52:
            pass
        elif opcodeint == 53:
            pass
        else:
            raise Exception(Colors.red + 'invalid load instruction.' + Colors.ENDC)

    def run_store(self, opcodeint, immediates):
        if opcodeint == 54:
            pass
        elif opcodeint == 55:
            pass
        elif opcodeint == 56:
            pass
        elif opcodeint == 57:
            pass
        elif opcodeint == 58:
            pass
        elif opcodeint == 59:
            pass
        elif opcodeint == 60:
            pass
        elif opcodeint == 61:
            pass
        elif opcodeint == 62:
            pass
        else:
            raise Exception(Colors.red + 'invalid store instruction' + Colors.ENDC)

    def run_current_memory(self, opcodeint, immediates):
        pass

    def run_grow_memory(self, opcodeint, immediates):
        pass

    def run_const(self, opcodeint, immediates):
        if opcodeint == 65:
            pass
        elif opcodeint == 66:
            pass
        elif opcodeint == 67:
            pass
        elif opcodeint == 68:
            pass
        else:
            raise Exception(Colors.red + 'invalid const instruction' + Colors.ENDC)

    def run_eqz(self, opcodeint, immediates):
        if opcodeint == 69:
            pass
        elif opcodeint == 80:
            pass
        else:
            raise Exception(Colors.red + 'invalid eqz instruction' + Colors.ENDC)

    def run_eq(self, opcodeint, immediates):
        if opcodeint == 70:
            pass
        elif opcodeint == 81:
            pass
        elif opcodeint == 91:
            pass
        elif opcodeint == 97:
            pass
        else:
            raise Exception(Colors.red + 'invalid eq instruction' + Colors.ENDC)

    def run_ne(self, opcodeint, immediates):
        if opcodeint == 71:
            pass
        elif opcodeint == 82:
            pass
        elif opcodeint == 92:
            pass
        elif opcodeint == 98:
            pass
        else:
            raise Exception(Colors.red + 'invalid ne instruction' + Colors.ENDC)

    def run_lt_s(self, opcodeint, immediates):
        if opcodeint == 72:
            pass
        elif opcodeint == 83:
            pass
        else:
            raise Exception(Colors.red + 'invalid lt_s instruction' + Colors.ENDC)

    def run_lt_u(self, opcodeint, immediates):
        if opcodeint == 73:
            pass
        elif opcodeint == 84:
            pass
        else:
            raise Exception(Colors.red + 'invalid lt_u instruction' + Colors.ENDC)

    def run_gt_s(self, opcodeint, immediates):
        if opcodeint == 74:
            pass
        elif opcodeint == 85:
            pass
        else:
            raise Exception(Colors.red + 'invalid gt_s instruction' + Colors.ENDC)

    def run_gt_u(self, opcodeint, immediates):
        if opcodeint == 75:
            pass
        elif opcodeint == 86:
            pass
        else:
            raise Exception(Colors.red + 'invalid gt_u instruction' + Colors.ENDC)

    def run_le_s(self, opcodeint, immediates):
        if opcodeint == 76:
            pass
        elif opcodeint == 87:
            pass
        else:
            raise Exception(Colors.red + 'invalid le_s instruction' + Colors.ENDC)

    def run_le_u(self, opcodeint, immediates):
        if opcodeint == 77:
            pass
        elif opcodeint == 88:
            pass
        else:
            raise Exception(Colors.red + 'invalid le_u instruction' + Colors.ENDC)

    def run_ge_s(self, opcodeint, immediates):
        if opcodeint == 78:
            pass
        elif opcodeint == 89:
            pass
        else:
            raise Exception(Colors.red + 'invalid ge_s instruction' + Colors.ENDC)

    def run_ge_u(self, opcodeint, immediates):
        if opcodeint == 79:
            pass
        elif opcodeint == 90:
            pass
        else:
            raise Exception(Colors.red + 'invalid ge_u instruction' + Colors.ENDC)

    def run_lt(self, opcodeint, immediates):
        if opcodeint == 93:
            pass
        elif opcodeint == 99:
            pass
        else:
            raise Exception(Colors.red + 'invalid lt instruction' + Colors.ENDC)

    def run_gt(self, opcodeint, immediates):
        if opcodeint == 94:
            pass
        elif opcodeint == 100:
            pass
        else:
            raise Exception(Colors.red + 'invalid gt instruction' + Colors.ENDC)

    def run_le(self, opcodeint, immediates):
        if opcodeint == 95:
            pass
        elif opcodeint == 101:
            pass
        else:
            raise Exception(Colors.red + 'invalid le instruction' + Colors.ENDC)

    def run_ge(self, opcodeint, immediates):
        if opcodeint == 96:
            pass
        elif opcodeint == 102:
            pass
        else:
            raise Exception(Colors.red + 'invalid ge instruction' + Colors.ENDC)

    def run_clz(self, opcodeint, immediates):
        if opcodeint == 103:
            pass
        elif opcodeint == 121:
            pass
        else:
            raise Exception(Colors.red + 'invalid clz instruction' + Colors.ENDC)

    def run_ctz(self, opcodeint, immediates):
        if opcodeint == 104:
            pass
        elif opcodeint == 122:
            pass
        else:
            raise Exception(Colors.red + 'invalid ctz instruction' + Colors.ENDC)

    def run_popcnt(self, opcodeint, immediates):
        if opcodeint == 105:
            pass
        elif opcodeint == 123:
            pass
        else:
            raise Exception(Colors.red + 'invalid popcnt instruction' + Colors.ENDC)

    def run_add(self, opcodeint, immediates):
        if opcodeint == 106:
            pass
        elif opcodeint == 124:
            pass
        elif opcodeint == 146:
            pass
        elif opcodeint == 160:
            pass
        else:
            raise Exception(Colors.red + 'invalid add instruction' + Colors.ENDC)

    def run_sub(self, opcodeint, immediates):
        if opcodeint == 107:
            pass
        elif opcodeint == 125:
            pass
        elif opcodeint == 147:
            pass
        elif opcodeint == 161:
            pass
        else:
            raise Exception(Colors.red + 'invalid sub instruction' + Colors.ENDC)

    def run_mul(self, opcodeint, immediates):
        if opcodeint == 108:
            pass
        elif opcodeint == 126:
            pass
        elif opcodeint == 148:
            pass
        elif opcodeint == 162:
            pass
        else:
            raise Exception(Colors.red + 'invalid mul instruction' + Colors.ENDC)

    def run_div_s(self, opcodeint, immediates):
        if opcodeint == 109:
            pass
        elif opcodeint == 127:
            pass
        else:
            raise Exception(Colors.red + 'invalid div_s instruction' + Colors.ENDC)

    def run_div_u(self, opcodeint, immediates):
        if opcodeint == 110:
            pass
        elif opcodeint == 128:
            pass
        else:
            raise Exception(Colors.red + 'invalid div_u instruction' + Colors.ENDC)

    def run_rem_s(self, opcodeint, immediates):
        if opcodeint == 111:
            pass
        elif opcodeint == 129:
            pass
        else:
            raise Exception(Colors.red + 'invalid rem_s instruction' + Colors.ENDC)

    def run_rem_u(self, opcodeint, immediates):
        if opcodeint == 112:
            pass
        elif opcodeint == 130:
            pass
        else:
            raise Exception(Colors.red + 'invalid rem_u instruction' + Colors.ENDC)

    def run_and(self, opcodeint, immediates):
        if opcodeint == 113:
            pass
        elif opcodeint == 131:
            pass
        else:
            raise Exception(Colors.red + 'invalid and instruction' + Colors.ENDC)

    def run_or(self, opcodeint, immediates):
        if opcodeint == 114:
            pass
        elif opcodeint == 132:
            pass
        else:
            raise Exception(Colors.red + 'invalid or instruction' + Colors.ENDC)

    def run_xor(self, opcodeint, immediates):
        if opcodeint == 115:
            pass
        elif opcodeint == 133:
            pass
        else:
            raise Exception(Colors.red + 'invalid xor instruction' + Colors.ENDC)

    def run_shl(self, opcodeint, immediates):
        if opcodeint == 116:
            pass
        elif opcodeint == 134:
            pass
        else:
            raise Exception(Colors.red + 'invalid shl instruction' + Colors.ENDC)

    def run_shr_s(self, opcodeint, immediates):
        if opcodeint == 117:
            pass
        elif opcodeint == 135:
            pass
        else:
            raise Exception(Colors.red + 'invalid shr_s instruction' + Colors.ENDC)

    def run_shr_u(self, opcodeint, immediates):
        if opcodeint == 118:
            pass
        elif opcodeint == 136:
            pass
        else:
            raise Exception(Colors.red + 'invalid shr_u instruction' + Colors.ENDC)

    def run_rotl(self, opcodeint, immediates):
        if opcodeint == 119:
            pass
        elif opcodeint == 137:
            pass
        else:
            raise Exception(Colors.red + 'invalid rotl instruction' + Colors.ENDC)

    def run_rotr(self, opcodeint, immediates):
        if opcodeint == 120:
            pass
        elif opcodeint == 138:
            pass
        else:
            raise Exception(Colors.red + 'invalid rotl instruction' + Colors.ENDC)

    def run_abs(self, opcodeint, immediates):
        if opcodeint == 139:
            pass
        elif opcodeint == 153:
            pass
        else:
            raise Exception(Colors.red + 'invalid abs instruction' + Colors.ENDC)

    def run_neg(self, opcodeint, immediates):
        if opcodeint == 140:
            pass
        elif opcodeint == 154:
            pass
        else:
            raise Exception(Colors.red + 'invalid neg instruction' + Colors.ENDC)

    def run_ceil(self, opcodeint, immediates):
        if opcodeint == 141:
            pass
        elif opcodeint == 155:
            pass
        else:
            raise Exception(Colors.red + 'invalid ceil instruction' + Colors.ENDC)

    def run_floor(self, opcodeint, immediates):
        if opcodeint == 142:
            pass
        elif opcodeint == 156:
            pass
        else:
            raise Exception(Colors.red + 'invalid floor instruction' + Colors.ENDC)

    def run_trunc(self, opcodeint, immediates):
        if opcodeint == 143:
            pass
        elif opcodeint == 157:
            pass
        else:
            raise Exception(Colors.red + 'invalid trunc instruction' + Colors.ENDC)

    def run_nearest(self, opcodeint, immediates):
        if opcodeint == 144:
            pass
        elif opcodeint == 158:
            pass
        else:
            raise Exception(Colors.red + 'invalid nearest instruction' + Colors.ENDC)

    def run_sqrt(self, opcodeint, immediates):
        if opcodeint == 145:
            pass
        elif opcodeint == 159:
            pass
        else:
            raise Exception(Colors.red + 'invalid sqrt instruction' + Colors.ENDC)

    def run_div(self, opcodeint, immediates):
        if opcodeint == 149:
            pass
        elif opcodeint == 163:
            pass
        else:
            raise Exception(Colors.red + 'invalid float div instruction' + Colors.ENDC)

    def run_min(self, opcodeint, immediates):
        if opcodeint == 150:
            pass
        elif opcodeint == 164:
            pass
        else:
            raise Exception(Colors.red + 'invalid min instruction' + Colors.ENDC)

    def run_max(self, opcodeint, immediates):
        if opcodeint == 151:
            pass
        elif opcodeint == 165:
            pass
        else:
            raise Exception(Colors.red + 'invalid max instruction' + Colors.ENDC)

    def run_copysign(self, opcodeint, immediates):
        if opcodeint == 152:
            pass
        elif opcodeint == 166:
            pass
        else:
            raise Exception(Colors.red + 'invalid max instruction' + Colors.ENDC)

    def run_i32wrapi64(self, opcodeint, immediates):
        pass

    def run_i32trunc_sf32(self, opcodeint, immediates):
        pass

    def run_i32trunc_uf32(self, opcodeint, immediates):
        pass

    def run_i32trunc_sf64(self, opcodeint, immediates):
        pass

    def run_i32trunc_uf64(self, opcodeint, immediates):
        pass

    def run_i64extend_si32(self, opcodeint, immediates):
        pass

    def run_i64extend_ui32(self, opcodeint, immediates):
        pass

    def run_i64trunc_sf32(self, opcodeint, immediates):
        pass

    def run_i64trunc_uf32(self, opcodeint, immediates):
        pass

    def run_i64trunc_sf64(self, opcodeint, immediates):
        pass

    def run_i64trunc_uf64(self, opcodeint, immediates):
        pass

    def run_f32convert_si32(self, opcodeint, immediates):
        pass

    def run_f32convert_ui32(self, opcodeint, immediates):
        pass

    def run_f32convert_si64(self, opcodeint, immediates):
        pass

    def run_f32convert_ui64(self, opcodeint, immediates):
        pass

    def run_f32demotef64(self, opcodeint, immediates):
        pass

    def run_f64convert_si32(self, opcodeint, immediates):
        pass

    def run_f64convert_ui32(self, opcodeint, immediates):
        pass

    def run_f64convert_si64(self, opcodeint, immediates):
        pass

    def run_f64convert_ui64(self, opcodeint, immediates):
        pass

    def run_f64promotef32(self, opcodeint, immediates):
        pass

    def run_i32reinterpretf32(self, opcodeint, immediates):
        pass

    def run_i64reinterpretf64(self, opcodeint, immediates):
        pass

    def run_f32reinterpreti32(self, opcodeint, immediates):
        pass

    def run_f64reinterpreti64(self, opcodeint, immediates):
        pass
