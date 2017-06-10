from collections import deque


class UserStat(object):
    def __init__(self, user_id):
        """
        An entity class to represent a user statistics data in log entry.
        Use Queue to store the time of "open" log entries that not "paired" by a "close" entry yet, by FIFO rules.
        Currently only cares about unpaired "open" log entries.
        If needs to keep the history of paired "open" log entries, may need to extend this class.

        :param user_id: the unique ID of a user.
        """
        self.user_id = user_id
        self.open_time_queue = deque([])
        self.total_duration = 0
        self.duration_count = 0

    def get_time_spent(self):
        """
        :return: the average time the user spent. Logically it should be at least 1.
        """
        if self.duration_count > 0:
            return max(1, self.total_duration / self.duration_count)
        return 0

    def update_duration(self, open_time, close_time):
        """
        Update the total total_duration of the time that a user spent on.
        :param open_time: user log entry open time, should be smaller than close time
        :param close_time: user log entry close time.
        """
        if open_time < close_time:
            self.total_duration += close_time - open_time
            self.duration_count += 1

    def add_open_time(self, open_time):
        """
        Append user log entry to the open time queue.
        :param open_time:
        """
        self.open_time_queue.append(int(open_time))

    def has_unpaired_open(self):
        """
        :return: True if the open time queue is not empty, i.e. contains unpaired "open" log entries; False otherwise.
        """
        return len(self.open_time_queue) > 0

    def pop_first_unpaired_open(self):
        """
        :return: The first user log entry open time, if any
        """
        if len(self.open_time_queue) > 0:
            return self.open_time_queue.popleft()
        return None

    def __repr__(self):
        return "%s, %s" % (self.user_id, self.get_time_spent())
