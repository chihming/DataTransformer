from code.Encoder import Encoder
from random import shuffle

class DataConverter:
    logger = None
    encoder = Encoder()

    def __init__(self, logger):
        self.logger = logger
        pass

    def SplitData(self, infile, target_column, sep, header, ratio):
        """
        Split data into training / testinf data
        """
        self.logger.info("Load data")
        data = [ line.rstrip().split(sep) for line in open(infile[0]) ]

        self.logger.info("split target")
        target_unique = list( set(zip(*(data))[target_column]) )
        shuffle(target_unique)
        cut_off = int( len(target_unique) * float(ratio[0]) )
        target_train = { t:1 for t in target_unique[:cut_off] }
        #target_test = { t:1 for t in target_unique[cut_off:] }
        self.logger.info("total targets: %d, train targets: %d" % (len(target_unique), len(target_unique) * float(ratio[0])))

        self.logger.info("split data")
        datamap = { target:[] for target in target_unique }
        dataoutTrain = []
        dataoutTest = []
        for d in data:
            datamap[d[target_column]].append(d)
        for target in datamap:
            if target in target_train:
                for d in datamap[target]:
                    dataoutTrain.append(sep.join(d))
            else:
                cut_off = int( len(datamap[target]) * float(ratio[2]) )
                for d in datamap[target][:cut_off]:
                    dataoutTrain.append(sep.join(d))
                for d in datamap[target][cut_off:]:
                    dataoutTest.append(sep.join(d))

        return dataoutTrain, dataoutTest
    
    def CSVtoLib(self, infile, target_column, sep, msep, offset, header, labels, c_columns, n_columns):
        """
        Convert CSV data to libSVM/libFM format
        """

        self.encoder.set_offset(offset)

        self.logger.info("Load data")

        target = [[] for i in range(len(infile))]
        converted = [[] for i in range(len(infile))]
        data = []
        for fname in infile:
            data.append( [ line.rstrip().split(sep) for line in open(fname) ] )
        
        if header:
            for i in range(len(data)):
                data[i] = data[i][1:]
        
        self.logger.info("Encode data")
        
        for e, d in enumerate(data):
            for idx in range(len(d[0])):
                if idx == target_column:
                    target[e] = list(zip(*(d))[idx])
                    continue
                elif idx in c_columns:
                    self.encoder.encode_categorical( set(zip(*(d))[idx]), msep=msep, label=idx )
                    self.logger.info("label: %s\tnew labels: %d\tMAX: %d" % (idx, self.encoder.get_label_len(idx), self.encoder.get_max_index()) )
                    continue
                elif idx in n_columns:
                    self.encoder.encode_numeric( set(zip(*(d))[idx]), label=idx )
                    self.logger.info("label: %s\tnew labels: %d\tMAX: %d" % (idx, self.encoder.get_label_len(idx), self.encoder.get_max_index()) )

        self.logger.info("Transform data")
        dataout = [[] for i in range(len(infile))]
        for e, d in enumerate(data):
            converted[e].append(target[e])
            for idx in range(len(d[0])):
                if idx in c_columns:
                    converted[e].append( self.encoder.fit_categorical( zip(*d)[idx], msep, label=idx ) )
                elif idx in n_columns:
                    converted[e].append( self.encoder.fit_numeric( zip(*d)[idx], label=idx ) )

            dataout[e] = [ "%s" % (" ".join(cdata)) for cdata in zip(*converted[e]) ]

        return dataout


    def CSVtoRel(self, infile, relfile, target_column, rtarget_column, sep, msep, offset, header, labels, c_columns, n_columns):
        """
        Convert data to relational data format
        """
        self.encoder.set_offset(offset)

        self.logger.info("Load data")
        targetTrain = [ line.rstrip().split(sep)[target_column] for line in open(infile[0]) ]
        targetTest = [ line.rstrip().split(sep)[target_column] for line in open(infile[1]) ]
        keymap = { value:str(idx) for idx, value in enumerate( [line.rstrip().split(sep)[rtarget_column] for line in open(relfile)] ) }
        datamapTrain = [ keymap[v] for v in targetTrain ]
        datamapTest = [ keymap[v] for v in targetTest ]
        
        data = [ line.rstrip().split(sep) for line in open(relfile) ]
        dim = len(data[0])
        
        if header:
            header = data[0]
            datamapTrain = datamapTrain[1:]
            datamapTest = datamapTest[2:]
            data = data[1:]
        
        self.logger.info("Encode data")
        for idx in range(dim):
            if idx in c_columns:
                self.encoder.encode_categorical( set(zip(*data)[idx]), msep=msep, label=idx )
                self.logger.info("label: %s\tlength: %d\tMAX: %d" % (idx, self.encoder.get_label_len(idx), self.encoder.get_max_index()) )
                continue
            elif idx in n_columns:
                self.encoder.encode_numeric( set(zip(*data)[idx]), label=idx )
                self.logger.info("label: %s\tlength: %d\tMAX: %d" % (idx, self.encoder.get_label_len(idx), self.encoder.get_max_index()) )

        self.logger.info("Transform data")
        converted = [ ["0" for i in range(len(data))] ]
        for idx in range(dim):
            if idx in c_columns:
                converted.append( self.encoder.fit_categorical( zip(*data)[idx], msep, label=idx ) )
            elif idx in n_columns:
                converted.append( self.encoder.fit_numeric( zip(*data)[idx], label=idx ) )

        dataout = [ "%s" % (" ".join(cdata)) for cdata in zip(*converted) ]

        return datamapTrain, datamapTest, dataout

