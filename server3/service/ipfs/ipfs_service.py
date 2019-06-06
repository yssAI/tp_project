import os
import ipfsapi

from server3.constants import IpfsError

# Add this comment for pull request test

class IpfsService(object):
    ipfs_server = '127.0.0.1'
    ipfs_server_port = 5001

    def __init__(self, ip=ipfs_server, port=ipfs_server_port):
        self.ipfs_server = ip
        self.ipfs_server_port = port
        self.ipfs_api = None
        # try:
        #     self.api = self.connect(self.ipfs_server, self.ipfs_server_port)
        # except Exception as err:
        #     raise RuntimeError(err)

    def connect(self, ip, port):
        """

        :param ip:
        :param port:
        :return:
        """
        try:
            self.ipfs_api = ipfsapi.connect(ip, port)
        except Exception as err:
            raise IpfsError("Cannot connect to IPFS server!", err)
        else:
            return self.ipfs_api

    def add_dataset(self, path):
        """

        :param path:
        :return:
        """
        if os.path.isdir(path):
            if not self.ipfs_api:
                api = self.connect(self.ipfs_server, self.ipfs_server_port)
            else:
                api = self.api
        else:
            raise IpfsError('must be a folder path')

        # ipfs_hash = api.add(path,
        # recursive=True,
        # wrap_with_directory=True)[-1]["Hash"]

        add_result = api.add(path, recursive=True)

        if 'Name' in add_result[-1].keys() and \
                add_result[-1]['Name'] == os.path.basename(path):
            return add_result[-1]['Hash']
        else:
            raise IpfsError(add_result)

    def get_dataset(self, hash):
        """

        :param hash:
        :return:
        """
        if not self.api:
            api = self.connect(self.ipfs_server, self.ipfs_server_port)
        else:
            api = self.api

        api.get(hash)
        pass


if __name__ == '__main__':
    pass
    # test = IpfsService()
    # folder_file_return = test.add_dataset('/Users/Chun/Documents/workspace/momodel/mo/pyserver/user_directory/chun/my_exercise')
    # # # folder_file_return = test.add_dataset('/Users/Chun/Desktop/Status')
    # print(folder_file_return)
