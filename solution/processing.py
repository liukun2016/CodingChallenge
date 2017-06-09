class MissingHandler(object):

    def __init__(self):
        pass

    def handle_missing_open(self, entry):
        raise NotImplementedError("Need to implement handle_missing_open method.")

    def handle_missing_close(self, entry):
        raise NotImplementedError("Need to implement handle_missing_close method.")

    @staticmethod
    def create_handler(mode):
        if mode == "random":
            return RandomHandler()
        elif mode == "average":
            return AverageHandler()
        elif mode == "ignore-early":
            return IgnoreHandler(from_early=True)
        elif mode == "ignore-late":
            return IgnoreHandler(from_early=False)
        elif mode == "chain-begin":
            return ChainHandler(from_begin=True)
        elif mode == "chain-end":
            return ChainHandler(from_begin=False)


class IgnoreHandler(MissingHandler):

    def __init__(self, from_early):
        self.from_early = from_early

    def handle_missing_open(self, entry):
        return entry

    def handle_missing_close(self, entry):
        return entry


class RandomHandler(MissingHandler):

    def __init__(self):
        pass


class AverageHandler(MissingHandler):

    def __init__(self):
        pass


class ChainHandler(MissingHandler):

    def __init__(self):
        pass


print MissingHandler.create_handler("ignore-early").handle_missing_close("ignore-early")