import re
import sys
import typing


class ClearInterval:

    @staticmethod
    def setClearInterval(args, logger) -> typing.Union[int, None]:
        r = re.compile('^--clear-interval=.*')
        confParam = list(filter(r.match, args))
        if len(confParam) == 1:
            try:
                value = confParam[0][17:]
                if value == 'NOW' or value == '0':
                    if input("Do you want 'run clear archives' with 0 interval? (y/N) ").lower() == 'y':
                        value = 0
                    else:
                        sys.exit(0)
                return int(value)
            except Exception as e:
                logger.error(f'Not valid --clear-interval must be a number or NOW {e}')
                sys.exit(1)
        return None
        
