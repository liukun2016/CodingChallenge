from src.main import main


class Test(object):

    handler_list = ["ignore", "random", "average"]

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def build_arguments(self, file_name, handler):
        arguments = "test --input_path=%s/%s --output_path=%s/%s/%s --handler=%s --verbose=1" % (
            self.input_path, file_name, self.output_path, file_name, handler, handler)
        return arguments.split()

    def test(self, file_name, handler):
        print handler
        arguments = self.build_arguments(file_name=file_name, handler=handler)
        main(arguments)

    def test_all(self, file_name):
        for handler in Test.handler_list:
            self.test(file_name, handler)


if __name__ == '__main__':
    test = Test(input_path="./sample_inputs", output_path="./sample_outputs")
    test.test_all("4")