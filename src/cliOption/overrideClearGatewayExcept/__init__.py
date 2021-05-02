import re
import sys
import typing


class OverrideClearGatewayExcept:

    @staticmethod
    def setClearGatewayExcept(args, logger) -> typing.Union[list, None]:
        r = re.compile('^--clear-gateway-except=.*')
        confParam = list(filter(r.match, args))
        if len(confParam) == 1:
            if len(confParam[0][23:]) > 0:
                return confParam[0][23:].split(',')
            else:
                logger.error(f"Not valid override")
                sys.exit(1)

        r = re.compile('^--clear-gateway-except$')
        confParam = list(filter(r.match, args))
        if len(confParam) == 1:
            return []
        
        return None
