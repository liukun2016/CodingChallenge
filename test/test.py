from src.main import main
from os.path import isfile, join
from os import listdir


class Test(object):

    handler_list = ["ignore", "random", "average"]

    def __init__(self):
        pass

    def test(self, input_path, output_path, file_name, handler):
        print "----handler=" + handler
        arguments = "test --input_path=%s/%s --output_path=%s/%s/%s --handler=%s --verbose=1" % (
            input_path, file_name, output_path, file_name, handler, handler)
        main(arguments.split())

    def test_all(self, input_path, output_path):
        for file_name in Test.get_all_files(input_path):
            print "--file_name=" + file_name
            for handler in Test.handler_list:
                self.test(input_path, output_path, file_name, handler)

    @staticmethod
    def get_all_files(input_dir):
        all_files = []
        for f in listdir(input_dir):
            if isfile(join(input_dir, f)):
                all_files.append(f)
        return all_files


if __name__ == '__main__':
    test = Test()
    test.test_all(input_path="./sample_inputs", output_path="./sample_outputs")