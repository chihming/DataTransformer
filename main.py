import argparse, json, logging
from datetime import datetime
from code.DataConverter import DataConverter

# Arguments
PARSER = argparse.ArgumentParser(description="Parameters for the script.")

# Header for splitting data
PARSER.add_argument('-labels', "--Labels", default=None,
                    help="Specify labels for splitting data")
PARSER.add_argument('-target', "--TargetColumn", type=int, default=None,
                    help="Target column for prediction.")
PARSER.add_argument('-cat', "--CategoricalColumn", default=None,
                    help="Categorical columns for encoding.")
PARSER.add_argument('-num', "--NumericColumn", default=None,
                    help="Numeric column for encoding.")

# files
PARSER.add_argument('-infile', "--InputFileName", default=None,
                    help="Input File Name")
PARSER.add_argument('-outfile', "--OutputFileName", default=None,
                    help="Output File Name")

PARSER.add_argument('-header', "--Header", type=int, default=None,
                    help="With header or not")
PARSER.add_argument('-sep', "--Separtor", default=None,
                    help="separtor for splitting data")

# features
PARSER.add_argument('-his', "--History", action="store_true",
                    help="Add history feature.")
PARSER.add_argument('-usim', "--AddUserSimilarity", action="store_true",
                    help="Add user similarity feature.")
PARSER.add_argument('-msim', "--AddMovieSimilarity", action="store_true",
                    help="Add movie similarity feature.")
PARSER.add_argument('-genre', "--AddGenres", action="store_true",
                    help="Add movie genres feature.")

# model parameters
PARSER.add_argument('-alpha', "--alpha", type=float, default=0.5,
                    help="Parameter of cosine similarity.")
PARSER.add_argument('-topk', "--topk", type=int, default=10,
                    help="Get top-k similarities.")

PARSER.set_defaults(argument_default=False)
CONFIG = PARSER.parse_args()
logging.basicConfig(format="[%(asctime)s] %(levelname)s\t%(message)s",
                    level=logging.DEBUG,
                    datefmt='%m/%d/%y %H:%M:%S')
logger = logging.getLogger( __name__ )


# ----------------------

def main():
    DC = DataConverter(logger)

    dataout = DC.CSVtolib(infile=CONFIG.InputFileName,
                          target_column=CONFIG.TargetColumn,
                          sep=CONFIG.Separtor,
                          header=CONFIG.Header,
                          labels=CONFIG.Labels,
                          c_columns=CONFIG.CategoricalColumn,
                          n_columns=CONFIG.NumericColumn)

    logger.info("Output result to '%s'" % (CONFIG.OutputFileName))
    file_out = open(CONFIG.OutputFileName, 'wb')
    file_out.write('\n'.join(dataout))
    file_out.close()


# ----------------------

if __name__ == '__main__':
    """
    Check Arguments &&
    Start Task
    """

    logger.info("Arguments Check")
    
    if CONFIG.InputFileName is not None:
        logger.info("Input File Name: '%s'" % CONFIG.InputFileName)
    else:
        logger.error("Please Specify Input File Name")
        exit()

    if CONFIG.OutputFileName is not None:
        logger.info("Output File Name: '%s'" % CONFIG.OutputFileName)
    else:
        logger.error("Please Specify Output File Name")
        exit()

    if CONFIG.TargetColumn is not None:
        logger.info("Target Column: '%d'" % (CONFIG.TargetColumn))
    else:
        logger.warning("Default Target Column: '0'")
        CONFIG.TargetColumn = 0

    if CONFIG.Header is not None:
        logger.info("Header: '%s'" % (CONFIG.Header))
    else:
        logger.warning("Default Header: '0'")
        CONFIG.Header = False

    if CONFIG.Separtor is not None:
        logger.info("Separtor: '%s'" % CONFIG.Separtor)
    else:
        logger.warning("Default Separtor: ','")
        CONFIG.Separtor = ','

    if CONFIG.CategoricalColumn is not None:
        logger.info("Categorical Columns: %s" % CONFIG.CategoricalColumn)
        CONFIG.CategoricalColumn = [ int(c) for c in CONFIG.CategoricalColumn.split(',') ]
    else:
        CONFIG.CategoricalColumn = []

    if CONFIG.NumericColumn is not None:
        logger.info("Numeric Columns: %s" % CONFIG.NumericColumn)
        CONFIG.NumericColumn = [ int(c) for c in CONFIG.NumericColumn.split(',') ]
    else:
        CONFIG.NumericColumn = []


    logger.info("Task Start")
    main()

