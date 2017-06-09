import sys
from utility import parse_main_arguments, print_usage
from processing import UserLogProcess


if __name__ == '__main__':
    config = parse_main_arguments(sys.argv)
    input_path = config.get("input_path")
    output_path = config.get("output_path")
    handler = config.get("handler")
    if not input_path or not output_path or not handler:
        print_usage()
    user_log_process = UserLogProcess(input_path=input_path, handler=handler)
    user_log_process.start()
    user_log_process.save_output(output_path=output_path)
