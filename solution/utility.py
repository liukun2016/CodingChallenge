import subprocess


def sub_process(cmd_list):
    process = subprocess.Popen(cmd_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return out


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
        handler: the way to handle missing close|open entries, currently supported ways:
            IE | ignore-early: default mode, ignore the missing entry starting from the earliest one.
            IL | ignore-late: ignore the missing entry starting from the latest one.
            R  | random: randomly pick a open|close entry from all entries before the missing one.
            CB | chain-begin: pick a open|close entry to match the missing one from the beginning with round-robin.
            CE | chain-end: pick a open|close entry to match the missing one from the ending with round-robin.
            A  | average: pick the average value of all previous open|close entry time of the missing one.
    """
    print(s)
    exit(0)