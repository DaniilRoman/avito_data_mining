import logging

logging.basicConfig(filename="flats.log",
                    format='%(asctime)s :: %(levelname)s :: %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')


def info(msg):
    logging.info(msg)
    print(msg)

def error(msg):
    logging.error(msg)
    print('ERROR: ' + msg)
