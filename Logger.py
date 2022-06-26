import logging, datetime, os
logger = logging.getLogger()
def logging_start(debug):
    global logger
    todayDate = datetime.datetime.now().strftime("%Y-%m-%d")
    nowTime = datetime.datetime.now().strftime("%H.%M:%S")
    try:
        os.makedirs(f"logs" + f"/{todayDate}")
        print("Todays logging directory ", todayDate,  " created.")
    except FileExistsError:
        pass
    
    open(f"logs" + f"/{todayDate}/{nowTime}.log", "w")
    print("This process started time ", nowTime,  " logging file created.")
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s', '%d-%m-%y %H:%M:%S')
    file_handler = logging.FileHandler("logs" + f"/{todayDate}/{nowTime}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    logger.info('Process started.')
    return logger