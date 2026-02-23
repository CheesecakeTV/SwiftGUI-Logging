import SwiftGUI_Logging as sgl
import logging
import sys
import time

logging.basicConfig()

my_logger = logging.Logger("SwiftGUI", logging.DEBUG)
my_handler = logging.StreamHandler(sys.stderr)

my_buffer = sgl.MemoryHandlerRotatingBuffer(5, logging.CRITICAL, target=my_handler)
my_logger.addHandler(my_buffer)

sgl.reroute_exceptions(logger=my_logger, reraise=False)

for i in range(10):
    print(i)
    my_logger.info(f"Hallo World {i}")
    time.sleep(0.25)

1 / 0
