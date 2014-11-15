import argparse, logging
from code.DataConverter import DataConverter

# Arguments
PARSER = argparse.ArgumentParser(description="Parameters for the script.",
                                 usage="python main.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]")

# Header for splitting data
task_list = ['dsplit', 'djoin']
PARSER.add_argument('-task', "--Task", default=None,
                    help="Specify the task. Options: %s" % task_list)

PARSER.add_argument('-target', "--TargetColumn", type=int, default=None,
                    help="Target column for input data.")
PARSER.add_argument('-ratio', "--Ratio", default=None,
                    help="param for splitting data")
PARSER.add_argument('-join', "--JoinColumn", default=None,
                    help="Join columns form input data to relation data.")

# files
PARSER.add_argument('-infile', "--InputFileName", default=None,
                    help="Input File Name")
PARSER.add_argument('-outfile', "--OutputFileName", default=None,
                    help="Output File Name")
PARSER.add_argument('-relfile', "--RelationFileName", default=None,
                    help="Relation File Name")

PARSER.add_argument('-header', "--Header", type=int, default=None,
                    help="With header or not")
PARSER.add_argument('-sep', "--Separator", default=None,
                    help="separator for splitting data")
PARSER.add_argument('-rsep', "--RSeparator", default=None,
                    help="separator for splitting relation data")

# model parameters
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

    if CONFIG.Task == 'dsplit':

        dataout = DC.SplitData(infile=CONFIG.InputFileName,
                               target_column=CONFIG.TargetColumn,
                               sep=CONFIG.Separator,
                               header=CONFIG.Header,
                               ratio=CONFIG.Ratio,
                               method=CONFIG.Method)

        for e, out in enumerate(dataout):
            logger.info("Output result to '%s'" % (CONFIG.OutputFileName[e]))
            file_out = open(CONFIG.OutputFileName[e], 'wb')
            file_out.write('\n'.join(out))
            file_out.close()

    elif CONFIG.Task == 'djoin':
    
        dataout = DC.JoinData(infile=CONFIG.InputFileName,
                              relfile=CONFIG.RelationFileName,
                              join_column=CONFIG.JoinColumn,
                              sep=CONFIG.Separator,
                              rsep=CONFIG.RSeparator,
                              header=CONFIG.Header)

        logger.info("Output result to '%s'" % (CONFIG.OutputFileName[0]))
        file_out = open(CONFIG.OutputFileName[0], 'wb')
        file_out.write('\n'.join(dataout))
        file_out.close()

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

    if CONFIG.InputFileName is not None:
        CONFIG.InputFileName = CONFIG.InputFileName.split(',')
        logger.info("Input File: %s" % (CONFIG.InputFileName))
    else:
        logger.error("Please specify input file.")
        logger.error("e.g. -infile [InputFile]")
        exit()

    if CONFIG.OutputFileName is not None:
        CONFIG.OutputFileName = CONFIG.OutputFileName.split(',')
        if CONFIG.Task == 'dsplit' and len(CONFIG.OutputFileName) != 2:
            logger.error("Please specify output file names.")
            logger.error("e.g. -outfile [TrainFile],[TestFile]")
            exit()
        logger.info("Output File: %s" % (CONFIG.OutputFileName))
    else:
        logger.error("Please specify output file names.")
        logger.error("e.g. -outfile [TrainFile],[TestFile]")
        exit()

    if CONFIG.Task == 'djoin':
        if CONFIG.RelationFileName is not None:
            CONFIG.RelationFileName = CONFIG.RelationFileName.split(',')
            logger.info("Relation File: %s" % (CONFIG.RelationFileName))
        else:
            logger.error("Please specify relation file.")
            logger.error("e.g. -relfile [InputFile]")
            exit()

        if CONFIG.RSeparator is not None:
            logger.info("Relation Separator: '%s'" % CONFIG.RSeparator)
            if CONFIG.RSeparator == "\\t": CONFIG.RSeparator = "\t"
        else:
            logger.error("Please Specify Separator for relation data.")
            logger.error("e.g. -rsep ','")
            exit()

        if CONFIG.JoinColumn is not None:
            CONFIG.JoinColumn = CONFIG.JoinColumn.split(',')
            logger.info("Join Columns: '%s'" % CONFIG.JoinColumn)
            if len(CONFIG.JoinColumn) != len(CONFIG.RelationFileName):
                logger.error("Number of Join Columns shall be the same as the number of Relation Files")
        else:
            logger.error("Please Specify Join Columns.")
            logger.error("e.g. -join 1:0")
            exit()

    if CONFIG.Task == 'dsplit':
        if CONFIG.TargetColumn is not None:
            logger.info("Target Column: '%d'" % (CONFIG.TargetColumn))
        else:
            logger.error("Please specify the target column.")
            logger.error("e.g. -target 0")
            exit()

        if CONFIG.Ratio is not None:
            CONFIG.Ratio = CONFIG.Ratio.split(':')
            if len(CONFIG.Ratio) != 3:
                logger.error("Please specify data split ratio.")
                logger.error("e.g. -ratio 0.8:0.2:0.5")
                exit()
            logger.info("Ratio: '%s'" % (CONFIG.Ratio))
        else:
            logger.error("Please specify data split ratio.")
            logger.error("e.g. -ratio 0.8:0.2:0.5")
            exit()

        if CONFIG.Method is not None:
            logger.info("Splitting method: '%s'" % (CONFIG.Method))
        else:
            logger.warning("Default splitting method: 'random'")
            CONFIG.Method = 'random'

    if CONFIG.Header is not None:
        logger.info("Header: '%s'" % (CONFIG.Header))
    else:
        logger.warning("Default Header: '0'")
        CONFIG.Header = False

    if CONFIG.Separator is not None:
        logger.info("Separator: '%s'" % CONFIG.Separator)
        if CONFIG.Separator == "\\t": CONFIG.Separator = "\t"
    else:
        logger.error("Please Specify Separator.")
        logger.error("e.g. -sep ','")
        exit()


    logger.info("Task Start")
    main()

