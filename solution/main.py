import sys
from utility import parse_main_arguments, print_usage


if __name__ == '__main__':
    config = parse_main_arguments(sys.argv)
    input_path = config.get("input_path")
    output_path = config.get("output_path")
    handler = config.get("handler")
    if not input_path or not output_path or not handler:
        print_usage()

