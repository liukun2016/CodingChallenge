from src.main import main


class Test(object):

    def __init__(self, input_path="./sample_inputs/", output_path="./sample_outputs/"):
        self.input_path = input_path
        self.output_path = output_path

    def build_arguments(self, file_name, handler):
        arguments = "test --input_path=%s%s --output_path=%s%s_%s --handler=%s --verbose=1" % (
            self.input_path, file_name, self.output_path, file_name, handler, handler)
        return arguments.split()

    def test_random(self, file_name):
        arguments = self.build_arguments(file_name=file_name, handler="random")
        main(arguments)

    def test_ignore(self, file_name):
        arguments = self.build_arguments(file_name=file_name, handler="ignore")
        main(arguments)

    def test_average(self, file_name):
        arguments = self.build_arguments(file_name=file_name, handler="average")
        main(arguments)

    def test_all(self, file_name):
        self.test_ignore(file_name)
        self.test_random(file_name)
        self.test_average(file_name)


test = Test()
test.test_all("1")