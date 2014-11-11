from code.Encoder import Encoder

class DataConverter:
    logger = None
    encoder = Encoder()
    label_index = 0

    def __init__(self, logger):
        self.logger = logger
        pass
    
    def CSVtolib(self, infile, target_column, sep, header, labels):
        """
        Convert CSV data to libSVM/libFM format
        """
        target = []
        data = [ line.rstrip().split(sep) for line in open(infile) ]
        dim = len(data[0])
        
        if header:
            header = data[0]
            data = data[1:]

        for idx in range(dim):
            if idx == target_column:
                target = list(zip(*data)[idx])
                continue
            self.encoder.encode_categorical( set(zip(*data)[idx]), label=idx )
            self.logger.info("label: %s\tlength: %d\tMAX: %d" % (idx, self.encoder.get_label_len(idx), self.encoder.get_max_index()) )

        converted = []
        converted.append(target)
        for idx in range(dim):
            if idx == target_column: continue
            converted.append( self.encoder.fit_categorical( zip(*data)[idx], label=idx ) )

        dataout = [ "%s" % (" ".join(cdata)) for cdata in zip(*converted) ]

        return dataout

