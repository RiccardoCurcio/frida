import re
import sys
import os


class OverrideClearGatewayExcept:

    @staticmethod
    def setClearGatewayExcept(args, logger) -> None:
        r = re.compile('^--clear-gateway-except=.*')
        confParam = list(filter(r.match, args))
        if len(confParam) == 1:
            if len(confParam[0][23:]) > 0:
                os.environ['FRIDA_OVERRIDE_CLEAR_GATEWAY_EXCEPT'] = confParam[0][23:]
            else:
                logger.error(f"Not valid override")
                sys.exit(1)
                
        r = re.compile('^--clear-gateway-except$')
        confParam = list(filter(r.match, args))
        if len(confParam) == 1:
            os.environ['FRIDA_OVERRIDE_CLEAR_GATEWAY_EXCEPT'] = '--RESET--'
            
