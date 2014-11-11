from collections import Counter
import math

class Encoder:

    def __init__(self, idx_offset=1):
        self.idx = idx_offset
        self.keymap = {}
        self.label_len = {}

    def get_max_index(self):
        return self.idx

    def get_label_len(self, label):
        return self.label_len[label]

    def encode_categorical(self, fea_vec, label=None, sep=None):
        """
        Encode for categorical features
        Return: Successful / Fail
        """
        if sep:
            idx_init = self.idx
            for feas in fea_vec:
                for fea in feas:
                    key = "%s %s" % (label, fea)
                    if key not in self.keymap:
                        self.keymap[key] = self.idx
                        self.idx += 1
        else:
            idx_init = self.idx
            for fea in fea_vec:
                key = "%s %s" % (label, fea)
                if key not in self.keymap:
                    self.keymap[key] = self.idx
                    self.idx += 1

        self.label_len[label] = self.idx - idx_init

    def encode_numeric(self, fea_vec, label=None):
        """
        Encode for categorical features
        Return: Successful / Fail
        """
        idx_init = self.idx
        key = "%s numerical" % (label)
        self.keymap[key] = self.idx
        self.idx += 1
        self.label_len[label] = self.idx - idx_init

    def fit_categorical(self, fea_matrix, label=None, sep=None):
        """
        transform data to encoded index
        """
        dataout = []
        
        if sep:
            for fea_vec in fea_matrix:
                out = ["%d:1" % (self.keymap["%s %s" % (label, fea)]) for fea in fea_vec.split(sep)]
                dataout.append(" ".join(out))
        else:
            for fea_vec in fea_matrix:
                out = ["%d:1" % (self.keymap["%s %s" % (label, fea_vec)])]
                dataout.append(" ".join(out))

        return dataout

    def transform_numeric(self, matrix, offset=0):
        dataout = []
        dim = len(matrix[0])
        for vector in matrix:
            out = []
            for col in range(dim):
                v = float(vector[col]) + 0.01
                if v < 0.0:
                    out.append("%d:1" % (self.keymap["%d numeric -1" % (col + offset)]) )
                elif v != 0.0:
                    out.append("%d:%f" % (self.keymap["%d numeric" % (col + offset)], v) )

            dataout.append(" ".join(out))
        return dataout

