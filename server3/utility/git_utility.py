import os


def get_repo_name(path):
    """Get repository name from path.
    1. /x/y.git -> /x/y  and  /x/y/.git/ -> /x/y//
    2. /x/y/ -> /x/y
    3. /x/y -> y
    """
    return path.replace(".git", "").rstrip(os.sep).split(os.sep)[-1]
