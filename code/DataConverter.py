from code.FeatureMaker import FeatureMaker
from code.Encoder import Encoder
from random import shuffle

class DataConverter:
    logger = None
    fmaker = None
    encoder = Encoder()

    def __init__(self, logger):
        self.logger = logger
        self.fmaker = FeatureMaker(logger)
        pass

    def JoinData(self, infile, relfile, sep, rsep, header, join_column):
        """
        Join data features
        """
        self.logger.info("Load data")
        indata = [ line.rstrip().split(sep) for line in open(infile[0]) ]
        dataout = indata[:]
        dmap = {}

        for e, columns in enumerate(join_column):
            self.logger.info("Join columns: %s" % columns)
            dmap.clear()
            tcolumn, jcolumn = columns.split(':')
            tcolumn = int(tcolumn)
            jcolumn = int(jcolumn)
            reldata = [ line.rstrip().split(rsep) for line in open(relfile[e]) ]
            for line in reldata:
                key = line[jcolumn]
                del line[jcolumn]
                dmap[key] = line
            dataout = [ a + b for a, b in zip( dataout, [dmap[key] for key in zip(*(indata))[tcolumn]] ) ]
        
        dataout = [ sep.join(cdata) for cdata in dataout ]
        return dataout

    def SplitData(self, infile, target_column, sep, header, ratio, method):
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

        if method == 'random':
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

    def DatatoLib(self, infile, target_column, sep, msep, offset, header, alpha, normalized, c_columns, n_columns, knn, process):
        """
        Convert CSV data to libSVM/libFM format
        """
        self.logger.info("Load data")
        self.encoder.set_offset(offset)

        target = [[] for i in range(len(infile))]
        converted = [[] for i in range(len(infile))]
        data = []
        nn = {}        
        for fname in infile:
            data.append( [ line.rstrip().split(sep) for line in open(fname) ] )
        
        if header:
            for i in range(len(data)):
                data[i] = data[i][1:]
        
        self.logger.info("Encode data")

        k_columns = []
        for tp in knn:
            k, acolumn, bcolumn = tp.split(':')
            k_columns.append(int(acolumn))

        # Cat, Num
        for e, d in enumerate(data):
            for idx in range(len(d[0])):
                if idx == target_column:
                    target[e] = list(zip(*(d))[idx])
                    continue
                elif idx in c_columns:
                    label = 'Cat ' + str(idx)
                    self.encoder.encode_categorical( set(zip(*(d))[idx]), msep=msep, label=label )
                    self.logger.info("label: %s\tnew labels: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )
                elif idx in n_columns:
                    label = 'Num ' + str(idx)
                    self.encoder.encode_numeric( set(zip(*(d))[idx]), label=label )
                    self.logger.info("label: %s\tnew labels: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )

                if idx in k_columns:
                    label = 'Sim ' + str(idx)
                    self.encoder.encode_categorical( set(zip(*(d))[idx]), msep=msep, label=label )
                    self.logger.info("label: %s\tnew labels: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )

        # KNN
        if knn is not None:
            self.logger.info("Compute Similarity Feature")
        for tp in knn:
            tempnn = {}
            k, acolumn, bcolumn = tp.split(':')
            k = int(k)
            acolumn = int(acolumn)
            bcolumn = int(bcolumn)
            nn[acolumn] = {}

            for a in set(list(zip(*(data[0]))[acolumn])):
                tempnn[a] = []
            for a, b in zip( list(zip(*(data[0]))[acolumn]), list(zip(*(data[0]))[bcolumn]) ):
                tempnn[a].append(b)

            self.logger.info("Get column %d similarities based on column %d" % (acolumn, bcolumn))

            nn[acolumn] = self.fmaker.pairwise_similarity(tempnn, k, alpha, process=process)

        # Data Transforming
        self.logger.info("Data Transforming")
        dataout = [[] for i in range(len(infile))]
        for e, d in enumerate(data):
            converted[e].append(target[e])
            for idx in range(len(d[0])):
                if idx in c_columns:
                    label = 'Cat ' + str(idx)
                    self.logger.info("Transforming label: %s" % label)
                    converted[e].append( self.encoder.fit_categorical( zip(*d)[idx], msep, label=label ) )
                elif idx in n_columns:
                    label = 'Num ' + str(idx)
                    self.logger.info("Transforming label: %s" % label)
                    converted[e].append( self.encoder.fit_numeric( zip(*d)[idx], label=label ) )

                if idx in k_columns:
                    label = 'Sim ' + str(idx)
                    self.logger.info("Transforming label: %s" % label)
                    fea_matrix = [ nn[idx][fea] if fea in nn[idx] else "" for fea in zip(*d)[idx] ]
                    converted[e].append( self.encoder.fit_feature( fea_matrix, msep='|', label=label, normalized=normalized ) )

            dataout[e] = [ "%s" % (" ".join(cdata)) for cdata in zip(*converted[e]) ]

        return dataout

    def DatatoRel(self, infile, relfile, target_column, rtarget_column, sep, rsep, msep, offset, header, alpha, normalized, c_columns, n_columns, knn, process):
        """
        Convert data to relational data format
        """
        self.encoder.set_offset(offset)

        self.logger.info("Load data")
        Train = None
        if len(knn) > 0:
            Train = [ line.split(sep) for line in open(infile[0]) ]
        Test = [ line.split(sep) for line in open(infile[0]) ]
        targetTrain = [ line.rstrip('\n').split(sep)[target_column] for line in open(infile[0]) ]
        targetTest = [ line.rstrip('\n').split(sep)[target_column] for line in open(infile[1]) ]
        
        if header:
            keymap = { value:str(idx) for idx, value in enumerate( [line.rstrip('\n').split(rsep)[rtarget_column] for line in open(relfile)] , -1) }
        else:
            keymap = { value:str(idx) for idx, value in enumerate( [line.rstrip('\n').split(rsep)[rtarget_column] for line in open(relfile)] ) }
        datamapTrain = [ keymap[v] if v in keymap else keymap['-1'] for v in targetTrain ]
        datamapTest = [ keymap[v] if v in keymap else keymap['-1'] for v in targetTest ]

        data = [ line.rstrip('\n').split(rsep) for line in open(relfile) ] 
        dim = len(data[0])
 
        nn = {}        
        k_columns = []
        if len(knn) > 0:
            k_columns = [ int(rtarget_column) ]

        if header:
            header = data[0]
            datamapTrain = datamapTrain[1:]
            datamapTest = datamapTest[1:]
            data = data[1:]
        
        self.logger.info("Encode data")
        for idx in range(dim):
            if idx in c_columns:
                label = 'Cat ' + str(idx)
                self.encoder.encode_categorical( set(zip(*data)[idx]), msep=msep, label=label )
                self.logger.info("label: %s\tlength: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )
            elif idx in n_columns:
                label = 'Num ' + str(idx)
                self.encoder.encode_numeric( set(zip(*data)[idx]), label=label )
                self.logger.info("label: %s\tlength: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )

            if idx in k_columns:
                label = 'Sim ' + str(rtarget_column)
                self.encoder.encode_categorical( set(zip(*(data))[idx]), msep=msep, label=label )
                self.logger.info("label: %s\tlength: %d\tMAX: %d" % (label, self.encoder.get_label_len(label), self.encoder.get_max_index()) )


        # KNN
        if len(knn) > 0:
            self.logger.info("Compute Similarity Feature")

        #Train = [ record for record in Train if float(record[3]) >= 3.]

        for tp in knn:
            tempnn = {}
            k, acolumn, bcolumn = tp.split(':')
            k = int(k)
            acolumn = int(acolumn)
            bcolumn = int(bcolumn)
            nn[rtarget_column] = {}

            for a in set(list(zip(*(Train))[acolumn])):
                tempnn[a] = []
            for a, b in zip( list(zip(*(Train))[acolumn]), list(zip(*(Train))[bcolumn]) ):
                tempnn[a].append(b)

            self.logger.info("Get column %d similarities based on column %d" % (acolumn, bcolumn))

            #nn[acolumn] = self.fmaker.pairwise_similarity(tempnn, k, alpha, process=process)
            nn[rtarget_column] = self.fmaker.pairwise_similarity(tempnn, k, alpha, process=process)


        self.logger.info("Transform data")
        converted = [ ["0" for i in range(len(data))] ]
        for idx in range(dim):
            if idx in c_columns:
                label = 'Cat ' + str(idx)
                converted.append( self.encoder.fit_categorical( zip(*data)[idx], msep, label=label ) )
            elif idx in n_columns:
                label = 'Num ' + str(idx)
                converted.append( self.encoder.fit_numeric( zip(*data)[idx], label=label ) )
            
            if idx in k_columns:
                label = 'Sim ' + str(rtarget_column)
                fea_matrix = [ nn[idx][fea] if fea in nn[idx] else "" for fea in zip(*data)[idx] ]
                converted.append( self.encoder.fit_feature( fea_matrix, msep='|', label=label, normalized=normalized ) )

        dataout = [ "%s" % (" ".join(cdata)) for cdata in zip(*converted) ]

        return dataout, datamapTrain, datamapTest, self.encoder.get_max_index()-1

