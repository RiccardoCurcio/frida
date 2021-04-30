import git
import logging
from src.application.command.version import VersionCommand
from src.process import Process


class VersionProcess(Process):

    def __init__(self, logger: logging.Logger, command: VersionCommand):
        self.__version = None
        self.__command = command
        self.__logger = logger
        super().__init__(self.__command.config, logger)

        try:
            local_repo = git.Repo(path=self._fridaParentPath)
            tags = sorted(
                local_repo.tags,
                key=lambda t: t.commit.committed_datetime
            )
            self.__version = tags[-1]
        except Exception:
            pass

        try:
            local_repo = git.Repo(path=self._fridaParentPath)
            self.__version = local_repo.active_branch.name
        except Exception:
            pass
        pass

    def run(self):
        print(f"{self.__version}")
