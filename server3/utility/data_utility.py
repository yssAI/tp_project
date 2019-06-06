# encoding: utf-8
"""
utility used in all project

Author: Zhaofeng Li, Tianyi Zhang
Date: 2017.06.09
"""
import numpy as np
import math

# int, float
def convert_data_array_by_fields(array, field_type_arrays):
    """

    :param array: array of data_set documents
    :param field_type_arrays: [['name', 'str'],['age', 'int'], ['salary',
    'float']]
    :return:
    """
    failure_exists = False
    failure_count = {f_t[0]: [] for f_t in field_type_arrays}
    for i, a in enumerate(array):
        oid = a['_id']
        for f_t in field_type_arrays:
            field = f_t[0]
            value_type = f_t[1]
            try:
                if value_type == 'int':
                    a[field] = str_to_int(a[field])
                elif value_type == 'float':
                    a[field] = str_to_float(a[field])
                elif value_type == 'str':
                    a[field] = str(a[field])
            except ValueError:
                failure_count[field].append(str(oid))
                failure_exists = True
                continue
    if failure_exists:
        return {'result': array, 'failures': failure_count}
    else:
        return {'result': array}


def str_to_int(s):
    return int(float(s))


def str_to_float(s):
    return float(s)


def convert_string_to_number(s):
    """
    just convert string to number, if not possibility, raise error
    @author   : Tianyi Zhang
    :param s: input string
    :return: int or float of raise error
    """
    try:
        return int(s)
    except ValueError:
        return float(s)


def convert_string_to_number_with_poss(s):
    """
    just convert string to number, if not possibility, keep string itself
    @author   : Tianyi Zhang
    :param s: input string
    :return: np.nan(not a number), int or float, or string
    """
    if s == "" or s != s:
        return np.nan
    try:
        float(s)
        try:
            int(s)
            return int(s) if int(s) == float(s) else float(s)
        except ValueError:
            return float(s)
    except ValueError:
        return s


def k_fold_cross_validation(data_train, data_target, ratio=0.1):
    """
    k-fold cross validation, split the training data into two part:
    one of it is for training
    the other is for testing
    @author   : Tianyi Zhang
    :param data_train: raw training data
    :param data_target: raw training target
    :param ratio: number of training data/testing data
    :return: X_train, X_test, y_train, y_test
    """
    from sklearn.model_selection import train_test_split
    from random import randint
    ramdom_state = randint(1,100)
    x_train, x_test, y_train, y_test = train_test_split(data_train, data_target,
                                                        test_size=ratio, random_state=ramdom_state)
    return x_train, x_test, y_train, y_test


def tensor_transform(data_matrix, order=(0, 1, 2)):
    """
    tensor_transform


    :param data_matrix: nd array
    :param order: transform to new order
    :return: new ordered array
    """
    X = np.array(data_matrix)
    X_out = X.transpose(order)
    return X_out


def string_label_encoder(arr):
    """
    string to numeric method


    :param arr: arr of set(string list)
    :return: list of number
    """
    from sklearn.preprocessing import LabelEncoder
    lab = LabelEncoder()
    return lab.fit_transform(arr)


def one_hot_encoder(arr):
    """
    string to numeric method, the label is random and 无序


    :param arr: arr of set(string list)
    :return: list of number
    """
    # from sklearn.preprocessing import LabelBinarizer
    # return LabelBinarizer().fit_transform(arr)

    from sklearn.preprocessing import OneHotEncoder
    return OneHotEncoder(sparse=False).fit_transform(arr.reshape(-1, 1))


def multi_one_hot_encoder(matrix):
    """
    string to numeric method, field selected is combined together
    a bedy bedy gud weib: https://ask.hellobi.com/blog/DataMiner/4897


    :param arr: arr of set(string list)
    # :param col: col is an array of field
    :return: matrix
    """

    from sklearn.preprocessing import MultiLabelBinarizer
    return MultiLabelBinarizer().fit_transform(matrix)


def retrieve_nan_index(result, nan_index):
    for ind in nan_index:
        result.insert(ind, np.nan)
    return result


def find_nan_index(data):
    return [index for index, item in enumerate(data) if math.isnan(item)]
