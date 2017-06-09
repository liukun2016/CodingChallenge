from entity import UserStat
import os


class MissingHandler(object):

    def __init__(self):
        pass

    def handle_missing(self, user_stat, log_time, status):
        if status == "open":
            self.handle_missing_open(user_stat, log_time)
        elif status == "close":
            self.handle_missing_close(user_stat, log_time)

    def handle_missing_open(self, user_stat, log_time):
        raise NotImplementedError("Need to implement handle_missing_open method.")

    def handle_missing_close(self, user_stat, log_time):
        raise NotImplementedError("Need to implement handle_missing_close method.")

    @staticmethod
    def create_handler(handler):
        if handler == "random":
            return RandomHandler()
        elif handler == "average":
            return AverageHandler()
        elif handler == "ignore-early":
            return IgnoreHandler(from_early=True)
        elif handler == "ignore-late":
            return IgnoreHandler(from_early=False)
        elif handler == "chain-begin":
            return ChainHandler(from_begin=True)
        elif handler == "chain-end":
            return ChainHandler(from_begin=False)


class IgnoreHandler(MissingHandler):

    def __init__(self, from_early):
        self.from_early = from_early

    def handle_missing_open(self, user_stat, log_time):
        pass

    def handle_missing_close(self, user_stat, log_time):
        pass


class RandomHandler(MissingHandler):

    def __init__(self):
        pass

    def handle_missing_open(self, user_stat, log_time):
        pass

    def handle_missing_close(self, user_stat, log_time):
        pass


class AverageHandler(MissingHandler):

    def __init__(self):
        pass

    def handle_missing_open(self, user_stat, log_time):
        pass

    def handle_missing_close(self, user_stat, log_time):
        pass


class ChainHandler(MissingHandler):

    def __init__(self):
        pass

    def handle_missing_open(self, user_stat, log_time):
        pass

    def handle_missing_close(self, user_stat, log_time):
        pass


class UserLogProcess(object):
    # a collection of user
    def __init__(self, input_path, handler):
        self.input_path = input_path
        self.user_map = {}
        self.handler = MissingHandler.create_handler(handler=handler)

    def get_user_stat(self, user_id):
        if user_id in self.user_map:
            return self.user_map[user_id]
        return None

    def process_log_entry(self, entry):
        if entry:
            entry_list = entry.split(",")
            user_id = entry_list[0]
            log_time = entry_list[1]
            status = entry_list[2]
            user_stat = self.get_user_stat(user_id)
            if user_stat:
                if self.check_missing(user_id=user_id, log_time=log_time, status=status):
                    self.handler.handle_missing(entry_list, status)
                user_stat.add_entry_time(entry_time=log_time, status=status)
            elif status == "open":
                self.user_map[user_id] = UserStat(user_id=user_id, log_time=log_time, status=status)

    def check_missing(self, user_id, log_time, status):
        user_stat = self.get_user_stat(user_id)
        if user_stat:
            if status == "open":
                user_stat = self.get_user_stat(user_id)
            elif status == "close":
                user_stat = self.get_user_stat(user_id)

    def start(self):
        with open(self.input_path, "r") as input_file:
            for line in input_file:
                self.process_log_entry(line)

    def save_output(self, output_path):
        parent_dir = output_path[0:output_path.rfind("/")]
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(output_path, 'w') as output:
            for user_stat in self.user_map.values():
                output.write(str(user_stat))
