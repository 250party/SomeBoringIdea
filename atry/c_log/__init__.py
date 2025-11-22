#from .c_log import openLog,writeLog,writeMapDataLog
from .create_logging import get_module_logger,writeMapDataLog
from .create_main_important_data import write_main_important_data,start_main_important_data
__all__=['writeMapDataLog','get_module_logger','write_main_important_data','start_main_important_data']