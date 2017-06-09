import sys
from processing import UserLogProcess


def parse_main_arguments(arguments):
    config = {}
    if arguments and len(arguments) > 1:
        for arg in arguments[1:]:
            args = arg.split("=")
            config[args[0][2:]] = args[1]
    return config


def print_usage():
    s = """Program usage:
    Arguments format: --arg_name=arg_value
    Required arguments:
        input_path: input path
        output_path: output path
        handler: the way to handle missing "close" or "open" log time entry, currently supported ways:
            ignore: default mode, ignore the missing close or open entry.
            random:
                for close status: randomly pick a open log time before the close log time.
                for open status: randomly pick a time between this open log time and the last log time.
            average:
                for close status: get the average time of all previous open log time of the missing one.
                for open status: get the average time between this open log time and the last log time.
    """
    print(s)
    exit(0)


def main(arguments):
    config = parse_main_arguments(arguments)
    input_path = config.get("input_path")
    output_path = config.get("output_path")
    handler = config.get("handler")
    verbose = True if "verbose" in config else False
    if not input_path or not output_path or not handler:
        print_usage()
    user_log_process = UserLogProcess(input_path=input_path, handler=handler, verbose=verbose)
    user_log_process.start()
    user_log_process.save_output(output_path=output_path)


if __name__ == '__main__':
    main(arguments=sys.argv)