from random import randint


class MissingHandlerInterface(object):

    def __init__(self):
        """
        Contains two interface methods to be implemented to handle missing log entries.
        """
        pass

    def handle_unpaired_open(self, open_time, log_end_time):
        """
        Handles the log entry whose status is "open" whereas there is no "close" time available to pair.

        :param open_time: the time a of "open" log entry.
        :param log_end_time: the last log entry time.
        :return: a proper "close" time to pair this "open" log entry. If unavailable, returns None.

        """
        raise NotImplementedError("Need to implement handle_unpaired_open method.")

    def handle_unpaired_close(self, close_time, log_start_time):
        """
        Handles the log entry whose status is "close" whereas there is no "open" time available to pair.

        :param close_time: the time of a "close" log entry.
        :param log_start_time: the first log entry time.
        :return: a proper "open" time to pair this "close" log entry. If unavailable, returns None.
        """
        raise NotImplementedError("Need to implement handle_unpaired_close method.")

    @staticmethod
    def create_handler(handler):
        """
        A factory to create a corresponding handler to handle log entries that missing "pairable" log time.

        :param handler: name/mode of the handler, by default "ignore" mode.
        :return: the specific implementation of a MissingHandler.
        """
        if handler == "random":
            return RandomHandler()
        elif handler == "average":
            return AverageHandler()
        return IgnoreHandler()


class IgnoreHandler(MissingHandlerInterface):

    def __init__(self):
        """
        Default mode for handling missing "open" or "closr" log entries. Do nothing with handling.
        """
        MissingHandlerInterface.__init__(self)

    def handle_unpaired_open(self, open_time, log_end_time):
        return None

    def handle_unpaired_close(self, close_time, log_start_time):
        return None


class RandomHandler(MissingHandlerInterface):

    def __init__(self):
        MissingHandlerInterface.__init__(self)

    def handle_unpaired_open(self, open_time, log_end_time):
        """
        Randomly pick a "close" time to pair this "open" log entry.
        In the range [begin, end], begin=open_time+1 and end=log_end_time+1.
        So only log time after open_time but equal to or before the log_end_time would be randomly picked.

        :param open_time: the "open" log entry time.
        :param log_end_time: the gloabl log end time.
        :return: If open time < log end time, a random log time between them, otherwise None.
        """
        return RandomHandler.get_random_in_range(open_time+1, log_end_time+1)

    def handle_unpaired_close(self, close_time, log_start_time):
        """
        Randomly pick a "open" time to pair this "close" log entry.
        In the range [begin, end], begin=log_start_time-1 and end=close_time-1.
        So only log time before the close_time but equal to or after the log_start_time would be randomly picked.

        :param close_time: the "close" log entry time.
        :param log_start_time: the gloabl log start time.
        :return: If close_time > log_start_time, a random log time between them, otherwise None.
        """

        return RandomHandler.get_random_in_range(log_start_time-1, close_time-1)

    @staticmethod
    def get_random_in_range(begin, end):
        """
        Given a range [begin, end], if begin <= end, then randomly pick one inside the range.
        Note if the begin == end or being == end-1, there could be only one value, i.e. the begin.

        :param begin:
        :param end:
        :return: a random integer inside the range of [begin, end]
        """
        return randint(begin, end) if begin <= end else None


class AverageHandler(MissingHandlerInterface):

    def __init__(self):
        MissingHandlerInterface.__init__(self)

    def handle_unpaired_open(self, open_time, log_end_time):
        """
        :param open_time:
        :param log_end_time:
        :return: the average value of open_time and log_end_time, if open_time is before log_end_time.
        """
        if open_time < log_end_time:
            return (open_time + log_end_time) / 2
        return None

    def handle_unpaired_close(self, close_time, log_start_time):
        """
        :param close_time:
        :param log_start_time:
        :return: the average value of close_time and log_start_time, if close_time is after log_start_time.
        """
        if close_time > log_start_time:
            return (close_time + log_start_time) / 2
        return None
