import os
import re
import yaml
import unittest
from unittest import TextTestRunner


class AppValidation(unittest.TestCase):
    """
    VALIDATE USER'S App

    """

    # APP_AUTHOR = ""
    APP_PATH = "./"
    APP_NAME = ""
    # APP_USER_DIRECTORY = "user_directory"
    TARGET_PY_FILE = ""

    APP_VALIDATION_MODE = 'basic'

    def test_py_file(self):
        """
        To check the [handler.py] file

        :return:
        """

        self.assertTrue(os.path.isfile(
            "{}/{}".format(self.APP_PATH, self.TARGET_PY_FILE)),
            msg="py file does not exist")

    def test_yml_file(self):
        """
        To check the [app_spec.yml] file

        :return:
        """
        self.assertTrue(os.path.exists(
            "{}/app_spec.yml".format(self.APP_PATH)),
            msg="[app_spec.yml] file does not exist")

    def test_signature(self):
        """
        To check the handle() function in target py file.

        :return:
        """
        with open("{}/{}".format(self.APP_PATH, self.TARGET_PY_FILE),
                  'r', encoding="utf-8", errors='ignore') as f:
            read_data = f.read()
            # Check [def predict()] section
            with self.subTest(name="[def handle()] in main.py"):
                self.assertIsNotNone(
                    re.search(r'def\s+handle\(\w+\)', read_data),
                    msg="[def handle()] signature is missing or incorrect")

    def test_yaml(self):
        """
        To check the content of app_spec yml file

        :return:
        """

        # Check yml file can be loaded correctly
        with open("{}/app_spec.yml".format(self.APP_PATH), mode='r',
                  encoding="utf-8", errors='ignore') as stream:
            # Load yaml file
            try:
                yaml_obj = yaml.load(stream) or {}
            except Exception as e:
                self.fail(msg="app_spec.yml cannot be loaded")
            ll = ['input', 'output']
            check_list = ['value_type']

            for l in ll:
                l_obj = yaml_obj.get(l, None)
                # Check [input] and [output] section
                with self.subTest(name=f"[{l}] section"):
                    self.assertIsNotNone(
                        l_obj,
                        msg=f"[{l}] section missing in app_spec.yml")

                for k, v in l_obj.items():
                    for cl in check_list:
                        with self.subTest(name=f"[{l}:{k}]"):
                            value = v.get(cl)
                            self.assertIsNotNone(
                                value,
                                msg=f"[{k}/{cl}] missing in app_spec.yml")
                    if l == 'input' and 'value_range' in v and v['value_range']:
                        with self.subTest(
                                name=f"[input:{k}] section"):
                            self.assertTrue(
                                type(v['value_range']) is list,
                                msg=f"value_range [input:{k}] not a list")

    @classmethod
    def run_test(cls, app_path, app_name, app_file):
        AppValidation.APP_PATH = app_path
        AppValidation.MODULE_NAME = app_name
        AppValidation.TARGET_PY_FILE = app_file

        test_suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        return TextTestRunner().run(test_suite)
