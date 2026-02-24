import time
import SwiftGUI_Logging as sgl
import logging

def main():
    for i in range(10):
        logging.debug(f"Test {i}")
        print(i)
        time.sleep(0.25)

    logging.info("Crashing the program now")

    logging.critical("CRITICAL")
    1 / 0   # Cause a ZeroDivisionError, which crashes the program

if __name__ == '__main__':
    sgl.Configs.exceptions_to_file("Crashlogs/Crash.log") # Set up the crash-log
    main()  # Execute program
