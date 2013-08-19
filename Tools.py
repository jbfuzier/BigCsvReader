from chardet.chardet.universaldetector import UniversalDetector
from Config import ConfigBorg
import logging


def guessEncoding(file_path):
    config = ConfigBorg()
    u = UniversalDetector()
    file = open(file_path, "rb")
    for i in range(config.chardet_nb_of_line):
        u.feed(file.readline())
    u.close()
    result = u.result
    logging.info("Charset is %s with confidence of %s" % (result['encoding'], result['confidence']))
    return result['encoding']