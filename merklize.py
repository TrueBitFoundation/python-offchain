import hashlib
from math import log, floor
from copy import deepcopy


# falttens the machinestate-unused
def Flatten(machinestate):
    flat_ms = []
    for iter in machinestate.Linear_Memory:
        for iterer in iter:
            flat_ms.append(iterer)

    for iter in machinestate.Stack_Omni:
        flat_ms.append(iter)

    '''
    for iter in machinestate.Index_Space_Function:
        flat_ms.append(iter)

    for iter in machinestate.Index_Space_Table:
        flat_ms.append(iter)

    for iter in machinestate.Index_Space_Global:
        flat_ms.append(iter)

    for iter in machinestate.Index_Space_Linear:
        flat_ms.append(iter)
    '''


# expects to receive a flat list, creates a merkle tree for it.
class Merklizer():
    def __init__ (self, machinestate):
        self.machinestate = machinestate
        self.temp_level = machinestate
        self.double_temp = []
        self.treeindex = int()
        height = log(len(machinestate), 2)

        if height - floor(height) > 0.0:
            self.height = int(height) + 1
        else:
            self.height = int(height)

    def calcTreeLength(self):
        length = len(self.machinestate)
        total_length = length
        print('length: ', end='')
        print(length)
        while True:
            if length == 2:
                total_length += 1
                break
            if length % 2 == 0:
                temp_length = int(length / 2)
            else:
                temp_length = int(length / 2) + 1

            total_length += temp_length
            length = temp_length

        self.total_length = total_length
        print(total_length)
        return(total_length)

    # we are allocating the tree as a flat list. the root hash will be the last
    # element in the tree.
    def allocateTree(self):
        self.merkletree = ['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'] * self.calcTreeLength()

    # create the first level hashes
    def hashallleaves(self):
        for leaf in self.machinestate:
            current_hash = hashlib.sha256(leaf)
            self.merkletree[self.treeindex] = current_hash.hexdigest()
            self.treeindex += 1
            self.double_temp.append(current_hash.hexdigest())

        self.temp_level = deepcopy(self.double_temp)
        self.double_temp = []

    # creates the parent hashes
    def merklize(self):
        for index in range(0, len(self.temp_level), 2):
            current_leaf = self.temp_level[index]
            current_hash = hashlib.sha256(current_leaf)

            if index + 1 > len(self.temp_level) - 1:
                new_parent = hashlib.sha256(current_hash)
                self.merkletree[self.treeindex] = new_parent.hexdigest()
                self.treeindex += 1
                self.double_temp.append(new_parent)
            else:
                leaf_right = self.temp_level[index + 1]
                hash_right = hashlib.sha256(leaf_right)
                new_parent = hashlib.sha256(current_hash + hash_right)
                self.merkletree[self.treeindex] = new_parent.hexdigest()
                self.treeindex += 1
                self.double_temp.append(new_parent)

            if len(self.temp_level) != 1:
                self.temp_level = deepcopy(self.double_temp)
                self.double_temp = []
                self.merklize(self.temp_level)


    # returns the tree length along with the tree itself
    def getTree(self):
        return(self.total_length, self.merkletree)

    def run(self):
        self.allocateTree()
        self.hashallleaves()
        self.merklize()
        return(self.getTree)
