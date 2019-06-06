from server3.repository.general_repo import Repo


class ToolsRepo(Repo):
    def __init__(self, instance):
        Repo.__init__(self, instance)
