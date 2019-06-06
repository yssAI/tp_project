import os

from io import BytesIO
from PIL import Image
import base64
import re
import importlib
import yaml
import unittest
from datetime import datetime
from unittest import TextTestRunner


class ModuleValidation(unittest.TestCase):
    """
    VALIDATE USER'S MODULE
    """

    MODULE_AUTHOR = ""
    MODULE_PATH = "./"
    MODULE_NAME = ""
    MODULE_USER_DIRECTORY = "user_directory"
    # model / toolkit
    MODULE_TYPE = "model"
    # basic / advance
    MODULE_VALIDATION_MODE = 'basic'

    # user_directory.zhaofengli.sesese.src.main
    # MODULE_INPUT = {}
    # MODULE_YAML_OBJ = None

    def test_src_data_directory(self):
        """
        To check the [/src/data/] direcotary

        :return:
        """
        self.assertTrue(os.path.isdir(
            "{}/data".format(self.MODULE_PATH)) or os.path.isdir(
            "{}/src/data".format(self.MODULE_PATH)),
            msg="[/data/] directory does not exist")

    def test_main_file(self):
        """
        To check the [/src/main.py] file

        :return:
        """
        self.assertTrue(os.path.exists(
            "{}/main.py".format(self.MODULE_PATH)) or os.path.exists(
            "{}/src/main.py".format(self.MODULE_PATH)),
            msg="[/main.py] does not exist")

    def test_module_spec_file(self):
        """
        To check the [/src/module_spec.yml] file

        :return:
        """
        self.assertTrue(os.path.exists(
            "{}/module_spec.yml".format(self.MODULE_PATH)) or os.path.exists(
            "{}/src/module_spec.yml".format(self.MODULE_PATH)),
            msg="[/module_sepc.yml] does not exist")

    # def test_requirements_file(self):
    #     """
    #     To check the [/requirements.txt] file
    #
    #     :return:
    #     """
    #     self.assertTrue(os.path.exists(
    #         "{}/requirements.txt".format(self.MODULE_PATH)),
    #         msg="[requirements.txt] does not exist")

    # Step 2: main.py
    def test_signature(self):
        path = "{}/main.py".format(self.MODULE_PATH)
        old_path = "{}/src/main.py".format(self.MODULE_PATH)
        if not os.path.exists(path) and os.path.exists(old_path):
            path = old_path
        with open(path, 'r', encoding="utf-8", errors='ignore') as f:
            read_data = f.read()

            # Check class name
            with self.subTest(name='class name in main.py'):
                self.assertIsNotNone(
                    re.search(r'class\s+{}'.format(self.MODULE_NAME),
                              read_data),
                    msg="class name is not eqaul to {}".format(
                        self.MODULE_NAME))

            if self.MODULE_TYPE == 'model':
                # Check [def __init__()] section
                with self.subTest(name="[def __init__()] in main.py"):
                    self.assertIsNotNone(
                        re.search(r'def\s+__init__\(self', read_data),
                        msg="[def __init__()] signature is missing")

                # Check [def train()] section
                # with self.subTest(name="[def train()] in main.py"):
                #     self.assertIsNotNone(
                #         re.search(r'def\s+train\(self,\s+conf={}', read_data),
                #         msg="[def train()] signature is missing")

                # Check [def predict()] section
                with self.subTest(name="[def predict()] in main.py"):
                    self.assertIsNotNone(
                        re.search(r'def\s+predict\(self,\s+conf={}',
                                  read_data),
                        msg="[def predict()] signature is missing")

                # Check [def load_model()] section
                # with self.subTest(name="[def load_model()] in main.py"):
                #     self.assertIsNotNone(
                #         re.search(r'def\s+load_model\(self', read_data),
                #         msg="[def load_model()] signature is missing")

            elif self.MODULE_TYPE == 'toolkit':
                # Check [def __init__()] section
                with self.subTest(name="[def __init__()] in main.py"):
                    self.assertIsNotNone(
                        re.search(r'def\s+__init__\(self', read_data),
                        msg="[def __init__()] signature is missing")

                # Check [def run()] section
                with self.subTest(name="[def run()] in main.py"):
                    self.assertIsNotNone(
                        re.search(r'def\s+run\(self,\s+conf={}', read_data),
                        msg="[def run()] signature is missing")

    # Step 3: YAML
    def test_yaml(self):
        '''
            To check the content of [module_spec.yaml] file
        :return:
        '''

        path = "{}/module_spec.yml".format(self.MODULE_PATH)
        old_path = "{}/src/module_spec.yml".format(self.MODULE_PATH)
        if not os.path.exists(path) and os.path.exists(old_path):
            path = old_path
        # Check yml file can be loaded correctly
        with open(path,
                  encoding="utf-8", errors='ignore') as stream:
            # Load yaml file
            try:
                yaml_obj = yaml.load(stream)
            except Exception as e:
                self.fail(msg="yaml cannot be loaded")

            # Check [input] section
            with self.subTest(name="[input] section"):
                self.assertIsNotNone(
                    yaml_obj.get("input"),
                    msg="[input] section missing in module_spec.yml")

            # Check [output] section
            with self.subTest(name="[output] section"):
                self.assertIsNotNone(
                    yaml_obj.get("output"),
                    msg="[output] section missing in module_spec.yml")

            # Check value_name / value_type / default_value of each parameter
            required_predict_items = {"value_name": "name",
                                      "value_type": "value_type",
                                      "default_value": "default"}

            prefixes = []
            if self.MODULE_TYPE == 'model':
                prefixes = ['predict']
            elif self.MODULE_TYPE == 'toolkit':
                prefixes = ['run']

            for prefix in prefixes:
                # Check [input:predict or input:run] section
                with self.subTest(name="[input:{}] section".format(prefix)):
                    yaml_input = yaml_obj.get("input", {}).get(prefix, None)
                    self.assertIsNotNone(
                        yaml_input,
                        msg="[input/{}] section missing in module_spec.yml".
                            format(prefix))

                input_feed = {}
                for k, v in yaml_input.items():
                    # Check value_name
                    # with self.subTest(name="[input:{}:{}]".format(prefix, k)):
                    #     name = v.get(required_predict_items["value_name"], None)
                    #     self.assertIsNotNone(
                    #         name,
                    #         msg="[{}/name] missing in module_spec.yml".format(
                    #                 k, name))

                    # Check value_type
                    with self.subTest(name="[input:{}:{}]".format(prefix, k)):
                        value_type = v.get(required_predict_items["value_type"],
                                           None)
                        self.assertIsNotNone(
                            value_type,
                            msg="[{}/value_type] missing in module_spec.yml".format(
                                k, value_type))

                    # Check default_value
                    if self.MODULE_VALIDATION_MODE == 'advance':
                        with self.subTest(name="[input:{}:{}]".format(prefix, k)):
                            default_value = v.get(
                                required_predict_items["default_value"], None)
                            self.assertIsNotNone(
                                default_value,
                                msg="[{}/default] missing in module_spec.yml".format(
                                    k, default_value))

                        # Check if type of default_value is matched with value_type
                        with self.subTest(name=
                                          "[input:{}:{}] - "
                                          "Type Checking".format(prefix, k)):
                            assert_result, value = \
                                self.check_value_type(value_type, default_value)
                            self.assertTrue(
                                assert_result,
                                msg="[{}/default] value is not match "
                                    "with [{}/value_type]".format(k, k))

                        input_feed[k] = value

                # print("input_feed", input_feed)

                if input_feed:
                    # Check predict() with default_value of each parameter
                    with self.subTest(name="{}()".format(prefix)):
                        try:
                            old_module_import_path = \
                                "{}.{}.{}.src.main".format(
                                    self.MODULE_USER_DIRECTORY,
                                    self.MODULE_AUTHOR,
                                    self.MODULE_NAME)
                            module_import_path = \
                                "{}.{}.{}.main".format(
                                    self.MODULE_USER_DIRECTORY,
                                    self.MODULE_AUTHOR,
                                    self.MODULE_NAME)
                            try:
                                my_module = importlib. \
                                    import_module(module_import_path)
                            except ModuleNotFoundError:
                                my_module = importlib. \
                                    import_module(old_module_import_path)
                            m = getattr(my_module, self.MODULE_NAME)()

                            if self.MODULE_TYPE == 'model':
                                result = m.predict(input=input_feed)
                            elif self.MODULE_TYPE == 'toolkit':
                                result = m.run(input=input_feed)

                            # print("result", result)
                            # Check result type

                        except Exception as e:
                            self.fail(
                                msg=
                                "{}() cannot be executed correctly - {}".format(
                                    prefix, str(e)))
                else:
                    if self.MODULE_VALIDATION_MODE == 'advance':
                        self.fail(msg="MODULE_INPUT cannot be generated")

    def check_value_type(self, value_type, default_value):
        # available Types: int, str, float, img, datetime, [int], [str], [float]
        check_funcs = {
            "int": self.check_int(default_value),
            "float": self.check_float(default_value),
            "str": self.check_str(default_value),
            "datetime": self.check_datetime(default_value),
            "img": self.check_img(default_value),
            "base64_image": self.check_img(default_value),
            "['int']": self.check_array_int(default_value),
            "[int]": self.check_array_int(default_value),
            "[str]": self.check_array_str(default_value),
            "['str']": self.check_array_str(default_value),
            "[float]": self.check_array_float(default_value),
            "['float']": self.check_array_float(default_value)
        }

        # print('value_type', value_type)
        try:
            return check_funcs[str(value_type)]
        except Exception as e:
            self.fail(msg="[value_type] is not valid")

    @staticmethod
    def check_int(value):
        return type(value) is int, value

    @staticmethod
    def check_float(value):
        return type(value) is float, value

    @staticmethod
    def check_str(value):
        return type(value) is str, value

    @staticmethod
    def check_img(value):
        try:
            base64_data = re.sub('^data:image/.+;base64,', '', value)
            byte_data = base64.b64decode(base64_data)
            image_data = BytesIO(byte_data)
            Image.open(image_data)
            return True, value
        except Exception as e:
            print(str(e))
            return False, None

    @staticmethod
    def check_datetime(value):
        return type(value) is datetime, value

    @staticmethod
    def check_array_int(value):
        if type(value) is list:
            # print("in check_array_int()")
            return all(isinstance(item, int) for item in value), value
        else:
            return False, None

    @staticmethod
    def check_array_str(value):
        if type(value) is list:
            return all(isinstance(item, str) for item in value), value
        else:
            return False, None

    @staticmethod
    def check_array_float(value):
        if type(value) is list:
            return all(isinstance(item, float) for item in value)
        else:
            return False, None

    @classmethod
    def run_test(cls, module_path, module_name, module_user_ID, module_type,
                 val_mode='basic'):
        ModuleValidation.MODULE_PATH = module_path
        ModuleValidation.MODULE_NAME = module_name
        ModuleValidation.MODULE_AUTHOR = module_user_ID
        ModuleValidation.MODULE_TYPE = module_type
        ModuleValidation.MODULE_VALIDATION_MODE = val_mode

        test_suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        return TextTestRunner().run(test_suite)

# if __name__ == '__main__':
#     # GDValidation.MODULE_PATH = os.environ.get('MODULE_PATH', GDValidation.MODULE_PATH)
#     # GDValidation.MODULE_NAME = os.environ.get('MODULE_NAME', GDValidation.MODULE_NAME)
#
#     # if len(sys.argv) > 1:
#     #     GDValidation.MODULE_NAME = sys.argv.pop()
#     #     GDValidation.MODULE_PATH = sys.argv.pop()
#     # print(GDValidation.MODULE_NAME)
#     # print(GDValidation.MODULE_PATH)
#     import sys
#     sys.path.append('../../../')
#     ModuleValidation.MODULE_PATH = "/Users/Chun/Documents/workspace/momodel/goldersgreen/pyserver/user_directory/zhaofengli/weather_prediction"
#     ModuleValidation.MODULE_NAME = "weather_prediction"
#     ModuleValidation.MODULE_AUTHOR = "zhaofengli"
#     ModuleValidation.MODULE_TYPE = 'model'
#     ModuleValidation.MODULE_VALIDATION_MODE = 'basic'
#     # /Users/Chun/Documents/workspace/goldersgreen/pyserver/user_directory/zhaofengli/sesese
#     # unittest.main()
#
#     test_suite = unittest.TestLoader().loadTestsFromTestCase(ModuleValidation)
#     test_result = TextTestRunner().run(test_suite)
#
#     print("total_errors", len(test_result.errors))
#     print("total_failures", len(test_result.failures))
#
#     # print("test_result.__dict__", test_result.__dict__)
#     # print("test_resultXXX", test_result.failures[0][1])
