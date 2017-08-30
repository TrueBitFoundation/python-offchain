import hashlib
from math import log, floor
from copy import deepcopy


# serializes the machinestate-unused
def Serialize(machinestate): # pragma: no cover
    flat_ms = []
    for iter in machinestate.Linear_Memory:
        for iterer in iter:
            flat_ms.append(iterer)

    for iter in machinestate.Stack_Omni:
        flat_ms.append(iter)


# expects to receive a flat list, creates a merkle tree for it.
class Merklizer(): # pragma: no cover
    def __init__ (self, machinestate, module):
        self.machinestate = machinestate
        self.module = module
        self.temp_level = machinestate
        self.double_temp = []
        self.treeindex = int()
        height = log(len(machinestate), 2)

        if height - floor(height) > 0.0:
            self.height = int(height) + 1
        else:
            self.height = int(height)

    # @DEVI-FIXME
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
        self.merkletree = ['\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'] * self.calcTreeLength()

    # create the first level hashes
    def hashallleaves(self):
        for index in range(0, self.module.data_section.count):
            current_hash = hashlib.sha256(self.module.data_section.data_segments[index].data)
            #print(current_hash.hexdigest())
            #print(hashlib.sha256(b"Nobody inspects the spammish repetition").hexdigest())
            self.merkletree[self.treeindex] = current_hash.hexdigest()
            self.treeindex += 1
            #self.double_temp.append(current_hash.hexdigest())
            self.double_temp.append(current_hash.hexdigest())

        self.temp_level = self.double_temp
        self.double_temp = []

    # creates the higher-level hashes
    def merklize(self):
        print('----------------------------------------------------------------')
        for member in self.temp_level:
            print(member)
        print('----------------------------------------------------------------')
        for index in range(0, len(self.temp_level), 2):
            current_hash = self.temp_level[index]
            print(current_hash)

            if index + 1 > len(self.temp_level) - 1:
                new_parent = hashlib.sha256(bytearray(current_hash.encode('utf-8')))
                #print(new_parent.hexdigest())
                self.merkletree[self.treeindex] = new_parent.hexdigest()
                self.treeindex += 1
                self.double_temp.append(new_parent.hexdigest())
            else:
                hash_right = self.temp_level[index + 1]
                new_parent = hashlib.sha256(bytearray(current_hash.encode('utf-8') + hash_right.encode('utf-8')))
                print(new_parent.hexdigest())
                self.merkletree[self.treeindex] = new_parent.hexdigest()
                self.treeindex += 1
                self.double_temp.append(new_parent.hexdigest())

        if len(self.temp_level) != 1:
            self.temp_level = self.double_temp
            self.double_temp = []
            self.merklize()
        else:
            return


    # returns the tree length along with the tree itself
    def getTree(self):
        return(self.total_length, self.merkletree)

    def run(self):
        self.allocateTree()
        self.hashallleaves()
        self.merklize()
        return(self.getTree())
