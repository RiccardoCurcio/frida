import re
import sys
import os


class Service:

    @staticmethod
    def getOnlyService(args, logger, config) -> list:
        r = re.compile('^--service=.*')
        confParam = list(filter(r.match, args))
        if len(confParam) == 1:
            services = confParam[0][10:].split(',')
            for service in services:
                if service not in config.sections():
                    logger.error(
                        f'"{service}" not exsist in {os.getenv("CONFIG_FILE", None)}'
                    )
                    sys.exit(1)
                logger.info(f'"{service}" found')
        else:
            services = config.sections()
        return services
