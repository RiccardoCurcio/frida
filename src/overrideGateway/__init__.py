import re
import sys
import os


class OverrideGateway:

    @staticmethod
    def setGateway(args, logger) -> None:
        r = re.compile('^--gateway=.*')
        confParam = list(filter(r.match, args))
        if len(confParam) == 1:
            if len(confParam[0][10:]) > 0:
                os.environ['FRIDA_OVERRIDE_GATEWAY'] = confParam[0][10:]
            else:
                logger.error(f"Not valid override")
                sys.exit(1)
                
