import argparse, logging
from code.DataConverter import DataConverter

# Arguments
PARSER = argparse.ArgumentParser(description="Parameters for the script.",
                                 usage="python main.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]")

task_list = ['data2sparse', 'data2rel']
PARSER.add_argument('-task', "--Task", default=None,
                    help="Specify the task. Options: %s" % task_list)

# Header for splitting data
PARSER.add_argument('-target', "--TargetColumn", type=int, default=None,
                    help="Target column for input data.")
PARSER.add_argument('-rtarget', "--RTargetColumn", type=int, default=None,
                    help="Target column for rlational data.")
PARSER.add_argument('-cat', "--CategoricalColumn", default=None,
                    help="Categorical columns for encoding.")
PARSER.add_argument('-num', "--NumericColumn", default=None,
                    help="Numeric column for encoding.")
PARSER.add_argument('-knn', "--KNNColumn", default=None,
                    help="Columns for KNN encoding.")

# files
PARSER.add_argument('-infile', "--InputFileName", default=None,
                    help="Input File Name")
PARSER.add_argument('-outfile', "--OutputFileName", default=None,
                    help="Output File Name")
PARSER.add_argument('-relfile', "--RelationalFileName", default=None,
                    help="Relational File Name")

PARSER.add_argument('-header', "--Header", type=int, default=None,
                    help="With header or not")
PARSER.add_argument('-sep', "--Separator", default=None,
                    help="separtor for splitting data")
PARSER.add_argument('-rsep', "--RSeparator", default=None,
                    help="separtor for splitting relational data")
PARSER.add_argument('-msep', "--MutiLabelSeparator", default=None,
                    help="separator for splitting multiple-labeled data")

# model parameters
PARSER.add_argument('-alpha', "--Alpha", type=float, default=0.5,
                    help="Parameter of cosine similarity.")
PARSER.add_argument('-nor', "--Normalized", type=float, default=0,
                    help="Do normalization or not.")
PARSER.add_argument('-offset', "--Offset", default=None,
                    help="Encoding offset")
PARSER.add_argument('-group', "--Group", type=float, default=None,
                    help="Grouping number.")
PARSER.add_argument('-method', "--Method", default=None,
                    help="Split data according to specified method.")

PARSER.set_defaults(argument_default=False)
CONFIG = PARSER.parse_args()
logging.basicConfig(format="[%(asctime)s] %(levelname)s\t%(message)s",
                    level=logging.DEBUG,
                    datefmt='%m/%d/%y %H:%M:%S')
logger = logging.getLogger( __name__ )


# ----------------------

def main():
    DC = DataConverter(logger)

    if CONFIG.Task == 'data2sparse':
        dataout = DC.DatatoLib(infile=CONFIG.InputFileName,
                               target_column=CONFIG.TargetColumn,
                               sep=CONFIG.Separator,
                               msep=CONFIG.MutiLabelSeparator,
                               offset=CONFIG.Offset,
                               header=CONFIG.Header,
                               alpha=CONFIG.Alpha,
                               normalized=CONFIG.Normalized,
                               c_columns=CONFIG.CategoricalColumn,
                               n_columns=CONFIG.NumericColumn,
                               knn=CONFIG.KNNColumn)

        for e, out in enumerate(dataout):
            logger.info("Output result to '%s'" % (CONFIG.OutputFileName[e]))
            file_out = open(CONFIG.OutputFileName[e], 'wb')
            file_out.write('\n'.join(out))
            file_out.close()

    elif CONFIG.Task == 'data2rel':
        dataout = DC.DatatoRel(infile=CONFIG.InputFileName,
                               relfile=CONFIG.RelationalFileName,
                               target_column=CONFIG.TargetColumn,
                               rtarget_column=CONFIG.RTargetColumn,
                               sep=CONFIG.Separator,
                               rsep=CONFIG.RSeparator,
                               msep=CONFIG.MutiLabelSeparator,
                               offset=CONFIG.Offset,
                               header=CONFIG.Header,
                               alpha=CONFIG.Alpha,
                               normalized=CONFIG.Normalized,
                               c_columns=CONFIG.CategoricalColumn,
                               n_columns=CONFIG.NumericColumn,
                               knn=CONFIG.KNNColumn)

        logger.info("Output result to '%s'" % (CONFIG.OutputFileName[0]))
        file_out = open(CONFIG.OutputFileName[0], 'wb')
        file_out.write('\n'.join(dataout[0]))
        file_out.close()

        logger.info("Output result to '%s'" % (CONFIG.OutputFileName[0] + '.train'))
        file_out = open(CONFIG.OutputFileName[0] + '.train', 'wb')
        file_out.write('\n'.join(dataout[1]))
        file_out.close()

        logger.info("Output result to '%s'" % (CONFIG.OutputFileName[0] + '.test'))
        file_out = open(CONFIG.OutputFileName[0] + '.test', 'wb')
        file_out.write('\n'.join(dataout[2]))
        file_out.close()

        if CONFIG.Group is not None:
            logger.info("Output result to '%s'" % (CONFIG.OutputFileName[0]) + '.group')
            file_out = open(CONFIG.OutputFileName[0] + '.group', 'wb')
            file_out.write('\n'.join( ["%s" % (CONFIG.Group)]*dataout[-1] ))
            file_out.close()

    else:
        logger.error("Unknow Task")


# ----------------------

if __name__ == '__main__':
    """
    Check Arguments &&
    Start Task
    """

    logger.info("Arguments Check")

    if CONFIG.Task is not None:
        if CONFIG.Task not in task_list:
            logger.error("Unknow Task.")
            logger.error("Options: %s" % task_list)
            exit()
        logger.info("Task: '%s'" % CONFIG.Task)
    else:
        logger.error("Please Specify the Task.")
        logger.error("Options: %s" % task_list)
        exit()

    if CONFIG.Task == 'data2rel':
        if CONFIG.RelationalFileName is not None:
            logger.info("Relational File: '%s'" % CONFIG.RelationalFileName)
        else:
            logger.error("Please specify corresponding relational data")
            logger.error("e.g. -relfile [RelationFile]")
            exit()

        if CONFIG.RTargetColumn is not None:
            logger.info("Relational Target Column: '%d'" % (CONFIG.RTargetColumn))
        else:
            logger.error("Please specify the target for relational data.")
            logger.error("e.g. -rtarget 0")
            exit()

    if CONFIG.InputFileName is not None:
        CONFIG.InputFileName = CONFIG.InputFileName.split(',')
        logger.info("Input File: %s" % (CONFIG.InputFileName))
        if CONFIG.Task == 'data2rel':
            if len(CONFIG.InputFileName) != 2:
                logger.error("Input Files shall contains one [TrainFile] and one [Testfile].")
                logger.error("e.g. -infile [TrainFile],[Testfile].")
                exit()
    else:
        logger.error("Please specify input files splitted by ','")
        logger.error("e.g. -infile [InputFile1],[InputFile2],...")
        exit()

    if CONFIG.OutputFileName is not None:
        CONFIG.OutputFileName = CONFIG.OutputFileName.split(',')
        if len(CONFIG.InputFileName) != len(CONFIG.OutputFileName) and CONFIG.Task == 'data2csv':
            logger.error("Amount of Input files shall be equaled to amount of Ouput files.")
            exit()
        logger.info("Output File: %s" % (CONFIG.OutputFileName))
    else:
        logger.error("Please specify output files splitted by ','")
        logger.error("e.g. -outfile [OutputFile1],[OutputFile2],...")
        exit()

    if CONFIG.TargetColumn is not None:
        logger.info("Target Column: '%d'" % (CONFIG.TargetColumn))
    else:
        logger.error("Please specify the target column.")
        logger.error("e.g. -target 0")
        exit()

    if CONFIG.Separator is not None:
        logger.info("Separator: '%s'" % CONFIG.Separator)
        if CONFIG.Separator == "\\t": CONFIG.Separator = "\t"
    else:
        logger.error("Please specify the separator.")
        logger.error("e.g. -sep ','")
        exit()

    if CONFIG.Header is not None:
        logger.info("Header: '%s'" % (CONFIG.Header))
    else:
        logger.warning("Default Header: '0'")
        CONFIG.Header = False

    if CONFIG.Alpha is not None:
        logger.info("Alpha: '%s'" % (CONFIG.Alpha))

    if CONFIG.RSeparator is not None:
        logger.info("Separator for relation data: '%s'" % CONFIG.RSeparator)
        if CONFIG.RSeparator == "\\t": CONFIG.RSeparator = "\t"
    else:
        logger.warning("Set Relational Data Separator as Separtor '%s'" % CONFIG.Separator)
        CONFIG.RSeparator = CONFIG.Separator

    if CONFIG.MutiLabelSeparator is not None:
        logger.info("Multi-labeled Separtor: '%s'" % CONFIG.MutiLabelSeparator)
    else:
        logger.warning("No multi-labeled data")

    if CONFIG.CategoricalColumn is not None:
        logger.info("Categorical Columns: '%s'" % CONFIG.CategoricalColumn)
        CONFIG.CategoricalColumn = [ int(c) for c in CONFIG.CategoricalColumn.split(',') ]
    else:
        logger.warning("No categorical column is specified.")
        CONFIG.CategoricalColumn = []

    if CONFIG.NumericColumn is not None:
        logger.info("Numeric Columns: '%s'" % CONFIG.NumericColumn)
        CONFIG.NumericColumn = [ int(c) for c in CONFIG.NumericColumn.split(',') ]
    else:
        logger.warning("No numerical column is specified.")
        CONFIG.NumericColumn = []

    if CONFIG.KNNColumn is not None:
        logger.info("Columns for KNN: '%s'" % CONFIG.KNNColumn.split(','))
        CONFIG.KNNColumn = CONFIG.KNNColumn.split(',')
    else:
        logger.warning("No knn column is specified.")
        CONFIG.KNNColumn = []

    if CONFIG.Offset is not None:
        logger.info("Offset: '%s' (encoding index starts from %s)" % (CONFIG.Offset, CONFIG.Offset))
    else:
        logger.info("Offset: '1' (encoding index starts from 1)")
        CONFIG.Offset = 1

    #if CONFIG.Method is not None:
    #    logger.info("Splitting method: '%s'" % (CONFIG.Method))
    #else:
    #    logger.warning("Default splitting method: 'random'")
    #    CONFIG.Method = 'random'

    logger.info("Task Start")
    main()

