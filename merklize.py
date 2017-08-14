import hashlib
from math import log, floor


def Flatten(machinestate):
    flat_ms = []
    for iter in machinestate.Linear_Memory:
        for iterer in iter:
            flat_ms.append(iterer)

    for iter in machinestate.Stack_Omni:
        flat_ms.append(iter)

    for iter in machinestate.Index_Space_Function:
        flat_ms.append(iter)

    for iter in machinestate.Index_Space_Table:
        flat_ms.append(iter)

    for iter in machinestate.Index_Space_Global:
        flat_ms.append(iter)

    for iter in machinestate.Index_Space_Linear:
        flat_ms.append(iter)



# @DEVI-expects a flattened machinestate
class Merklizer():
    def __init__ (self, machinestate):
        self.machinestate = machinestate
        height = log(len(machinestate), 2)

        if height - floor(height) > 0.0:
            self.height = int(height) + 1
        else:
            self.height = int(height)

    def calcTreeLength():
        length = int()
        total_length = int()
        length = len(self.machinestate)
        while True:
            if length == 2:
                total_length += 1
                break
            if length % 2 == 0:
                temp_length = length / 2
            else:
                temp_length = (length / 2) + 1

            total_length += temp_length
            length = temp_length

        self.total_length = total_length

    def allocateTree():
        self.merkletree = ['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' ] * self.calcTreeLength()

    def merklize():
        # create the first level hashes
        for index in range(0, len(self.machinestate), 2):
            current_leaf = self.machinestate[index]
            current_hash = hashlib.sha256(current_leaf)
            merkletree.append(current_hash.hexdigest())
            try:
                leaf_right = self.machinestate[index + 1]
            except IndexError:
                # current leaf is the last element so we there is no right leaf
                leaf_right = int()
            hash_right = hashlib.sha256(leaf_right)
            merkletree.append(hash_right.hexdigest())

        for level in range(0, self.height - 1):

    def getTree():
        return(self.total_length, self.merkletree)

    def run():
        self.calcTreeLength()
        allocateTree()
