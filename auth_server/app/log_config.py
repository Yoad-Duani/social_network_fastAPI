import logging
import uvicorn



# Define a custom log formatter class
class CustomLogFormatter(uvicorn.logging.DefaultFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record):
        record.__dict__["request_id"] = record.__dict__.get("request_id", "")
        # record.__dict__["levelprefix"] = record.__dict__.get("levelname", "").lower()
        return super().format(record)

FORMAT: str = "%(levelprefix)s %(asctime)s [%(threadName)s]  [%(name)s]  (%(request_id)s)  %(message)s"

def init_loggers(logger_name: str = "main-logger"):

    # create logger
    logger = logging.getLogger(f'{logger_name}')
    logger.setLevel(logging.DEBUG)

    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # create formatter
    # formatter = uvicorn.logging.DefaultFormatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    
    # Create a CustomLogFormatter instance for your custom logs
    formatter_custom = CustomLogFormatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

    # add formatter to console_handler
    console_handler.setFormatter(formatter_custom)

    # add console_handler to logger
    logger.addHandler(console_handler)

    return logging.getLogger(logger_name)







# ##
# import traceback
# try:
#     # ...
# except:
#     logging.error("the error is %s", traceback.format_exc())


# message queues, or log correlation techniques
