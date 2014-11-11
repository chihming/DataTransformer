import argparse, json, logging
from datetime import datetime
from code.DataConverter import DataConverter

# Arguments
PARSER = argparse.ArgumentParser(description="Parameters for the script.")

# Header for splitting data
PARSER.add_argument('-labels', "--Labels", default=None,
                    help="Specify labels for splitting data")
PARSER.add_argument('-target', "--TargetColumn", type=int, default=0,
                    help="Target column for prediction.")

# files
PARSER.add_argument('-infile', "--InputFileName", default=None,
                    help="Input File Name")
PARSER.add_argument('-outfile', "--OutputFileName", default=None,
                    help="Output File Name")

PARSER.add_argument('-header', "--Header", type=int, default=None,
                    help="With header or not")
PARSER.add_argument('-sep', "--Separtor", default=",",
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
                          labels=CONFIG.Labels)

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
    
    if CONFIG.InputFileName:
        logger.info("Input File Name: '%s'" % CONFIG.InputFileName)
    else:
        logger.error("Please Specify Input File Name")
        exit()

    if CONFIG.OutputFileName:
        logger.info("Output File Name: '%s'" % CONFIG.OutputFileName)
    else:
        logger.error("Please Specify Output File Name")
        exit()

    if CONFIG.TargetColumn:
        logger.info("Target Column: '%d'" % (CONFIG.TargetColumn))
    else:
        logger.warning("Default Target Column: '%d'" % (CONFIG.TargetColumn))

    if CONFIG.Header != 0:
        logger.info("Header: 'True'")
    else:
        logger.warning("Default Header: 'False'")
        CONFIG.Header = None

    if CONFIG.Separtor != ',':
        logger.info("Separtor: '%s'" % CONFIG.Separtor)
    else:
        logger.warning("Default Separtor: ','")


    logger.info("Task Start")
    main()

