import re
import sys
import typing
import logging


class OverrideGateway:

    @staticmethod
    def setGateway(
        args: list,
        logger: logging.Logger
    ) -> typing.Union[list, None]:
        confParam = list(filter(re.compile('^--gateway=.*').match, args))

        if len(confParam) == 1:
            if len(confParam[0][10:]) > 0:
                return confParam[0][10:].split(',')
            else:
                logger.error(f"Not valid override")
                sys.exit(1)

        return None
