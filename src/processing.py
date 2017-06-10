from handler import MissingHandlerInterface
from entity import UserStat
import os


class UserLogProcess(object):
    """
    A class for the porcessing work.
    Use a dictionary with user id as the key and user stat object as the value.
    If verbose mode, will print all details during the work.
    """
    def __init__(self, handler, verbose=False):
        self.user_map = {}
        self.handler = MissingHandlerInterface.create_handler(handler=handler)
        self.log_latest_time = None
        self.log_start_time = None
        self.verbose = verbose

    def get_user_stat(self, user_id):
        """
        Create the user stat object if it is not avaialbe yet.
        :param user_id:
        :return: The user stat object associated with the user_id.
        """
        if user_id not in self.user_map:
            self.user_map[user_id] = UserStat(user_id=user_id)
        return self.user_map[user_id]

    def process_log_entry(self, entry):
        """
        Here is the core method to process each log entry line.
        If the status is "open", simply add it to the user stat's open time queue.
        If "close", get the open time to pair it.
        If not pairable, needs to call the handler to handle it and get the proper "open" time for it.

        :param entry:
        :return:
        """
        if entry:
            entry_list = entry.split("\n")[0].split(",")
            user_id = entry_list[0]
            self.log_latest_time = int(entry_list[1])
            if self.log_start_time is None:
                self.log_start_time = self.log_latest_time
            status = entry_list[2]
            user_stat = self.get_user_stat(user_id)
            if status == "open":
                user_stat.add_open_time(self.log_latest_time)
            elif status == "close":
                if user_stat.has_unpaired_open():
                    open_time = user_stat.pop_first_unpaired_open()
                else:
                    open_time = self.handler.handle_unpaired_close(self.log_latest_time, self.log_start_time)
                if open_time:
                    user_stat.update_duration(open_time=open_time, close_time=self.log_latest_time)

    def start(self, input_path):
        """
        Since the log file may be too large to fit in memory, it is processed line by line.
        For each line, need to consider the unpaired "close" log entries.
        After all lines, for each user, need to handle its "open" log entries that not paired yet, if any.
        """
        with open(input_path, "r") as input_file:
            for line in input_file:
                self.process_log_entry(line)
        for user_stat in self.user_map.values():
            while user_stat.has_unpaired_open():
                unpaired_open_time = user_stat.pop_first_unpaired_open()
                close_time = self.handler.handle_unpaired_open(unpaired_open_time, self.log_latest_time)
                if close_time:
                    user_stat.update_duration(open_time=unpaired_open_time, close_time=close_time)

    def save(self, output_path):
        parent_dir = output_path[0:output_path.rfind("/")]
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(output_path, 'w') as output:
            for user_stat in self.user_map.values():
                line = str(user_stat)
                if self.verbose:
                    print line
                output.write(line+"\n")
