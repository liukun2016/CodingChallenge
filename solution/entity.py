class UserStat(object):
    user_id = ""
    open_time_list = list([])
    duration = 0
    open_offset = 0

    def __init__(self, user_id, log_time, status):
        self.user_id = user_id
        self.add_log_time(log_time=log_time, status=status)

    def get_time_spent(self):
        if self.count > 0:
            return self.duration / self.count
        return 0

    def add_log_time(self, log_time, status):
        if status == "open":
            self.open_time_list.append(log_time)
        elif status == "close":
            self.close_time_list.append(log_time)

    def add_duration(self, duration):
        self.duration += duration
        self.count += 1

    def get_paired_log_times(self, status):
        if self.open_time_list:
            if status == "open":
                return self.open_time_list[0: self.open_offset]
            elif status == "close":
                return self.close_time_list[0: self.close_offset]

    def add_open_time(self, open_time):
        self.open_time_list.append(open_time)

    def __repr__(self):
        return "%s, %s" % (self.user_id, self.get_time_spent())
