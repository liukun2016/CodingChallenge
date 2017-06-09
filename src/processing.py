from random import randint
from entity import UserStat
import os


class MissingHandler(object):

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
        :return: a proper time to "close" this entry, i.e. the close time to pair this open time.
        """
        raise NotImplementedError("Need to implement handle_unpaired_open method.")

    def handle_unpaired_close(self, close_time, log_start_time):
        """
        Handles the log entry whose status is "close" whereas there is no "open" time available to pair.

        :param close_time: the time of a "close" log entry.
        :param log_start_time: the first log entry time.
        :return: a proper time to "open" this entry, i.e. the open time to pair this close time.
        """
        raise NotImplementedError("Need to implement handle_unpaired_close method.")

    @staticmethod
    def create_handler(handler):
        """
        A factory to create a corresponding handler for log entries that missing "pairable" log time.
        :param handler: name/mode of the handler, by default "ignore" mode
        :return: the specific implementation of a MissingHandler.
        """
        if handler == "random":
            return RandomHandler()
        elif handler == "average":
            return AverageHandler()
        return IgnoreHandler()


class IgnoreHandler(MissingHandler):

    def __init__(self):
        MissingHandler.__init__(self)

    def handle_unpaired_open(self, open_time, log_end_time):
        return open_time

    def handle_unpaired_close(self, close_time, log_start_time):
        return close_time


class RandomHandler(MissingHandler):

    def __init__(self):
        MissingHandler.__init__(self)

    def handle_unpaired_open(self, open_time, log_end_time):
        return RandomHandler.get_random_in_range(open_time+1, log_end_time)

    def handle_unpaired_close(self, close_time, log_start_time):
        return RandomHandler.get_random_in_range(log_start_time, close_time-1)

    @staticmethod
    def get_random_in_range(begin, end):
        # Given a range [begin, end], randomly pick one inside the range
        return randint(begin, end)


class AverageHandler(MissingHandler):

    def __init__(self):
        MissingHandler.__init__(self)

    def handle_unpaired_open(self, open_time, log_end_time):
        return (open_time + log_end_time) / 2

    def handle_unpaired_close(self, close_time, log_start_time):
        return (close_time + log_start_time) / 2


class UserLogProcess(object):
    # a collection of user
    def __init__(self, input_path, handler, verbose=False):
        self.input_path = input_path
        self.user_map = {}
        self.handler = MissingHandler.create_handler(handler=handler)
        self.log_latest_time = None
        self.log_start_time = None
        self.verbose = verbose

    def get_user_stat(self, user_id):
        if user_id not in self.user_map:
            self.user_map[user_id] = UserStat(user_id=user_id)
        return self.user_map[user_id]

    def process_log_entry(self, entry):
        if entry:
            entry_list = entry.split(",")
            user_id = entry_list[0]
            self.log_latest_time = int(entry_list[1])
            if self.log_start_time is None:
                self.log_start_time = self.log_latest_time
            status = entry_list[2].split("\n")[0]
            user_stat = self.get_user_stat(user_id)
            if status == "open":
                user_stat.add_open_time(self.log_latest_time)
            elif status == "close":
                if user_stat.has_unpaired_open():
                    open_time = user_stat.pop_first_unpaired_open()
                else:
                    open_time = self.handler.handle_unpaired_close(user_stat, self.log_start_time)
                user_stat.update_duration(open_time=open_time, close_time=self.log_latest_time)

    def start(self):
        with open(self.input_path, "r") as input_file:
            for line in input_file:
                self.process_log_entry(line)
        for user_stat in self.user_map.values():
            while user_stat.has_unpaired_open():
                unpaired_open_time = user_stat.pop_first_unpaired_open()
                close_time = self.handler.handle_unpaired_open(unpaired_open_time, self.log_latest_time)
                user_stat.update_duration(open_time=unpaired_open_time, close_time=close_time)

    def save_output(self, output_path):
        parent_dir = output_path[0:output_path.rfind("/")]
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(output_path, 'w') as output:
            for user_stat in self.user_map.values():
                line = str(user_stat)
                if self.verbose:
                    print line
                output.write(line+"\n")
