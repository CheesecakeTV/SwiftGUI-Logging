import time
import SwiftGUI_Logging as sgl
import logging

def main():
    for k in range(3):
        for i in range(10):
            logging.debug(f"Test {i}")
            print(i)
            time.sleep(0.15)

        logging.error(f"Hehehe {k}")

    time.sleep(1)
    logging.info("Crashing the program now")

    1 / 0   # Cause a ZeroDivisionError, which crashes the program

if __name__ == '__main__':
    sgl.Configs.exceptions_to_file("Crashlogs/Crash.log") # Set up the crash-log
    main()  # Execute program
