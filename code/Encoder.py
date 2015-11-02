class Encoder:

    def __init__(self):
        self.idx = 0
        self.keymap = {}
        self.label_len = {}

    def set_offset(self, offset):
        self.idx = int(offset)

    def get_max_index(self):
        return self.idx

    def get_label_len(self, label):
        return self.label_len[label]

    def dump_map(self, mfile):
        out = []
        for key in self.keymap.keys():
            out.append("%s %s" % (key, self.keymap[key]))
        fout = open(mfile, 'w')
        fout.write("\n".join(out))
        fout.close()

    def encode_categorical(self, fea_vec, msep, label=None, sep=None):
        """
        Encode for categorical features
        Return: Successful / Fail
        """
        if msep:
            idx_init = self.idx
            for feas in fea_vec:
                for fea in feas.split(msep):
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

        #key = "%s numerical_except" % (label)
        #self.keymap[key] = self.idx
        #self.idx += 1

        self.label_len[label] = self.idx - idx_init

    def fit_categorical(self, fea_vec, msep, label=None, sep=None):
        """
        transform categorical data to encoded index
        """
        dataout = []
        
        if msep:
            feas = fea_vec.split(msep)
            weight = 1./len(feas)
            return " ".join( ["%d:%f" % (self.keymap["%s %s" % (label, fea)], weight) for fea in feas] )
        else:
            return "%d:1" % (self.keymap["%s %s" % (label, fea_vec)])

    def fit_feature(self, fea_vec, normalized=False, msep=None, label=None, sep=None):
        """
        transform extracted feature to encoded index
        """
        dataout = []
        
        if normalized:
            if fea_vec == '': return ""

            out = []
            efeas = fea_vec.split(msep)
            allw = 0.0
            for efea in efeas:
                allw += float(efea.split(':')[1])
                #allw += 1.
            for efea in efeas:
                fea, weight = efea.split(':')
                out.append( "%d:%s" % (self.keymap["%s %s" % (label, fea)], float(weight)/allw) )
                #out.append( "%d:%s" % (self.keymap["%s %s" % (label, fea)], 1./allw) )
            return " ".join(out).rstrip()

        else:
            if fea_vec == '': return ""
            
            out = []
            efeas = fea_vec.split(msep)
            for efea in efeas:
                fea, weight = efea.split(':')
                out.append( "%d:%s" % (self.keymap["%s %s" % (label, fea)], weight) )
            return " ".join(out).rstrip()


    def fit_numeric(self, fea_vec, label=None):
        """
        transform numeric data to encoded index
        """
        #if value.isdigit():
        return "%s:%f" % (self.keymap["%s numerical" % (label)], float(value))
        #else:
        #    dataout.append( "%s:1" % (self.keymap["%s numerical_except" % (label)]) )

