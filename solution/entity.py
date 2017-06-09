class UserStat(object):
    user_id = ""
    open_time_sum = 0
    close_time_sum = 0
    pairs = 0

    def __init__(self, user_id):
        self.user_id = user_id

    def get_time_spent(self):
        if self.pairs > 0:
            return (self.close_time_sum - self.open_time_sum) / self.pairs
        return 0

    