from collections import deque


class UserStat(object):
    def __init__(self, user_id):
        """
        An entity class to represent a user statistics data in log entry.
        Use Queue to store the time of "open" log entries that not "paired" by a "close" entry yet, by FIFO rules.
        Currently only cares about unpaired "open" log entries.

        :param user_id: the unique ID of a user.
        """
        self.user_id = user_id
        self.open_time_queue = deque([])
        self.duration = 0
        self.pair_count = 0

    def get_time_spent(self):
        if self.pair_count > 0:
            return max(1, self.duration / self.pair_count)
        return 0

    def update_duration(self, open_time, close_time):
        self.duration += close_time - open_time
        self.pair_count += 1

    def add_open_time(self, open_time):
        self.open_time_queue.append(int(open_time))

    def has_unpaired_open(self):
        """
        :return: True if the open time queue is not empty, i.e. contains unpaired "open" log entries; False otherwise.
        """
        return len(self.open_time_queue) > 0

    def pop_first_unpaired_open(self):
        if len(self.open_time_queue) > 0:
            return self.open_time_queue.popleft()
        return None

    def __repr__(self):
        return "%s, %s" % (self.user_id, self.get_time_spent())
