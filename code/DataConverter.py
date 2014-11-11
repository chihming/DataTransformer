from code.Encoder import Encoder

class DataConverter:
    logger = None
    encoder = Encoder()

    def __init__(self, logger):
        self.logger = logger
        pass
    
    def CSVtoLib(self, infile, target_column, sep, msep, offset, header, labels, c_columns, n_columns):
        """
        Convert CSV data to libSVM/libFM format
        """

        self.encoder.set_offset(offset)

        self.logger.info("Load data")
        target = []
        data = [ line.rstrip().split(sep) for line in open(infile) ]
        dim = len(data[0])
        
        if header:
            header = data[0]
            data = data[1:]
        
        self.logger.info("Encode data")
        for idx in range(dim):
            if idx == target_column:
                target = list(zip(*data)[idx])
                continue
            elif idx in c_columns:
                self.encoder.encode_categorical( set(zip(*data)[idx]), msep=msep, label=idx )
                self.logger.info("label: %s\tlength: %d\tMAX: %d" % (idx, self.encoder.get_label_len(idx), self.encoder.get_max_index()) )
                continue
            elif idx in n_columns:
                self.encoder.encode_numeric( set(zip(*data)[idx]), label=idx )
                self.logger.info("label: %s\tlength: %d\tMAX: %d" % (idx, self.encoder.get_label_len(idx), self.encoder.get_max_index()) )

        self.logger.info("Transform data")
        converted = []
        converted.append(target)
        for idx in range(dim):
            if idx in c_columns:
                converted.append( self.encoder.fit_categorical( zip(*data)[idx], msep, label=idx ) )
            elif idx in n_columns:
                converted.append( self.encoder.fit_numeric( zip(*data)[idx], msep, label=idx ) )

        dataout = [ "%s" % (" ".join(cdata)) for cdata in zip(*converted) ]

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
            datamapTest = datamapTest[1:]
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

