import logging.handlers


class MemoryHandlerRotatingBuffer(logging.handlers.MemoryHandler):

    def __init__(self, capacity, flushLevel=logging.ERROR, target=None):
        """
        This handler saves the last n records.
        Following records replace the oldest ones.
        If something with a higher level than 'flushLevel' is logged, the handler passes all entries to another, specified handler.

        THE BUFFER STILL FLUSHES WHEN THE SCRIPT ENDS, I COULDN'T AVOID THAT...
        Happy for suggestions.

        :param capacity: How many records to buffer before the oldest ones get deleted
        :param flushLevel: At which level of record the whole buffer is passed to the target-handler
        :param target: Handler to receive all records if necessary
        """
        super().__init__(capacity, flushLevel, target, flushOnClose=False)

    def shouldFlush(self, record):
        """
        New records are checked if the "flushing-condition" is met.
        :param record:
        :return:
        """
        if len(self.buffer) > self.capacity:    # Remove 0th element so the buffer doesn't "overflow"
            self.buffer.pop(0)

        return record.levelno >= self.flushLevel

