import time

import SwiftGUI_Logging as sgl
import logging

#logging.basicConfig()
#sgl.disable_root_handlers()
sgl.Configs.exceptions_to_file("debug/test/blabli/Test.log")

#my_logger = logging.getLogger("SwiftGUI")

for i in range(10):
    logging.debug(f"Test {i}")
    print(i)
    time.sleep(0.25)

#1 / 0
