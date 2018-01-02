import logging

FORMAT = '%(asctime)-15s - %(name)s - %(levelname)s:%(message)s'

def setup_logger():
    # todo add logging level to config file - json.
    logging.basicConfig(format=FORMAT, filename='Apo.log', level=logging.INFO)

