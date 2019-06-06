"""
util to diff two requirements.txt
"""

import itertools


def split_package(line):
    result = line.split('==')
    if not len(result) == 2:
        result = line.split('@')

        if not len(result) == 2:
            if line.startswith('-e'):
                # OK, I'll give a try but ONLY if you use the #egg in the end of the str
                result = line.split('#egg=')[1].split('-')
                result = '-'.join(result[:-1]), result[-1]
            else:
                raise Exception('Weird result of splitting: %s' % result)

    return map(lambda x: x.strip(), result)


def packages(freeze_f):
    for line in freeze_f.readlines():
        package, version = split_package(line)
        yield package, version


def merge_packages(*freezes):
    all_keys = set(itertools.chain(*[freeze.keys() for freeze in freezes]))

    for k in all_keys:
        versions = []
        for freeze in freezes:
            versions.append(
                freeze.get(k, None))  # Add the version for the package

        yield k, versions


def is_unique_value(l):
    """
    Checks if all elements in l are the same
    :param l: list of str
    """
    return not l or l[0] == '' or l.count(l[0]) == len(l)


def compare(old_packages, new_packages, result):
    """

    :param old_packages:
    :param new_packages:
    :param result:
    :return:
    """
    requirements = dict(merge_packages(old_packages, new_packages))

    for package_name, versions in list(requirements.items()):
        if not is_unique_value(versions):
            version = versions[1]
            if version is not None:
                print(f'{package_name}=={version}', file=result)
            # print(f'{package_name}=={version}')


def diff(old_req, new_req, result_req='./requirements.txt'):
    """
    util to diff two requirements.txt

    :param old_req:
    :param new_req:
    :param result_req:
    :return:
    """
    # print(f"Diff between {old_req} and {new_req}, write into {result_req}")
    with open(old_req, 'r') as old, open(new_req, 'r') as new, \
            open(result_req, 'w') as result:
        old_packages = dict(packages(old))
        new_packages = dict(packages(new))
        compare(old_packages, new_packages, result)


if __name__ == '__main__':
    diff('./requirements1.txt', './requirements2.txt')
