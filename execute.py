from OpCodes import *
from utils import Colors


class Execute():
    def __init__(self, machinestate):
        self.machinestate = machinestate
        self.opcodeint = ''
        self.immediates = []

    def getInstruction(self, opcodeint, immediates):
        self.opcodeint = opcodeint
        self.immediates = immediates

    # @DEVI-FIXME-string comparisons are more expensive than int comparisons
    def instructionUnwinder(self, opcodeint, immediates, machinestate):
        if opcodeint == 16:
            return self.run_call
        elif opcodeint == 11:
            return self.run_end

    def callExecuteMethod(self):
        runmethod = self.instructionUnwinder(self.opcodeint, self.immediates, self.machinestate)
        #print (self.opcodeint + ' ' + self.immediates)
        runmethod(self.opcodeint, self.immediates)

    def run_unreachable(self, opcodeint, immediates):
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
