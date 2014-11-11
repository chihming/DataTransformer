from code.Encoder import Encoder

class DataConverter:
    logger = None
    encoder = Encoder()
    label_index = 0

    def __init__(self, logger):
        self.logger = logger
        pass
    
    def CSVtoLib(self, infile, target_column, sep, msep, header, labels, c_columns, n_columns):
        """
        Convert CSV data to libSVM/libFM format
        """
        target = []
        
        self.logger.info("Load data")
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
            if idx == target_column:
                continue
            elif idx in c_columns:
                converted.append( self.encoder.fit_categorical( zip(*data)[idx], msep, label=idx ) )
            elif idx in n_columns:
                converted.append( self.encoder.fit_numeric( zip(*data)[idx], msep, label=idx ) )

        dataout = [ "%s" % (" ".join(cdata)) for cdata in zip(*converted) ]

        return dataout


    def CSVtoRel(self, infile, target_column, sep, header, labels, c_columns, n_columns):
        """
        Convert data to relational data format
        """
        pass




