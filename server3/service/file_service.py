# -*- coding: UTF-8 -*-
import os
import zipfile
import concurrent.futures
from pathlib import Path
from server3.business.kaggle_dataset_business import KaggleDatasetBusiness
import shutil
from server3.repository import config

UPLOAD_FOLDER = config.get_file_prop('UPLOAD_FOLDER')
IGNORED_FILES = ['__MACOSX/']
PASSED_FILES = ['__MACOSX', '.DS_Store']


def get_tree_size(path):
    """
    Return total size of files in given path and subdirs.
    """
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total


def save_upload(f, path, chunked):
    """ Save an upload.
    """
    if not path.parent.exists():
        path.parent.mkdir()
    if not chunked:
        while path.exists():
            # path = path.stem + '(1)'
            path = Path(path.parent, path.stem + '(1)' + path.suffix)
    with path.open('wb+') as destination:
        destination.write(f.read())


def combine_chunks(total_parts, total_size, source_folder, dest):
    """ Combine a chunked file into a whole file again. Goes through each part
    , in order, and appends that part's bytes to another destination file.
    Chunks are stored in media/chunks
    Uploads are saved in media/uploads
    """
    if not dest.parent.exists():
        dest.parent.makedirs()
    while dest.exists():
        dest = Path(dest.parent, dest.stem + '(1)' + dest.suffix)

    with dest.open('wb+') as destination:
        for i in range(int(total_parts)):
            part = source_folder / str(i)
            with part.open('rb') as source:
                destination.write(source.read())


def unzip_file(file_name, dest):
    """
    解压缩 zip 文件
    :param file_name: 压缩包名称
    :param dest: 基础路径
    :return:
    """

    # 在处理中文名时，会产生空文件夹，存储它们的路径，在解压完成后删除
    KaggleDatasetBusiness.unzip_file(file_name=file_name, dest=dest)
    # empty_dirs = []
    # with zipfile.ZipFile(file_name, 'r') as zip_file:
    #     for name in zip_file.namelist():
    #         extracted_path = Path(zip_file.extract(name, dest))
    #         utf8name = name.encode('cp437').decode('utf-8')
    #         if utf8name != name:
    #             # 进行中文名重命名
    #             extracted_path.replace(dest / utf8name)
    #             # 如果 name 的结尾是 '/'，说明是文件夹，需要存储起来
    #             if name[-1] == '/':
    #                 empty_dirs.append(extracted_path)
    #     # 递归删除文件夹
    #     for empty_dir in empty_dirs:
    #         if empty_dir.is_dir():
    #             shutil.rmtree(empty_dir)
