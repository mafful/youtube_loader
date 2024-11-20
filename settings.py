import os
import logging


# - - - - - - - - -
# initiate Directories
# - - - - - - - - -
BASE_DIR = os.getcwd()
input_dir = os.path.join(BASE_DIR, 'input_dir')
output_dir = os.path.join(BASE_DIR, 'output_dir')
logs_dir = os.path.join(BASE_DIR, 'logs_dir')

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)


# - - - - - - - - -
# initiate Logger
# - - - - - - - - -
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, 'project.log')),  # Log file in the logs_dir
        logging.StreamHandler()  # Log to the console as well
    ]
)
logger = logging.getLogger(__name__)

logger.info("Logger is set up and ready!")

