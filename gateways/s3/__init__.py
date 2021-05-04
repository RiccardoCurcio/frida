from gateways.GatewayABC import GatewayABC


class S3(GatewayABC):
    def __init__(self, logger):
        self.__logger = logger

    def send(self, archivePath) -> str:
        self.__logger.warning(f"S3 GATEWAY COMING SOON")
        self.__logger.info(f"S3 send {archivePath}")
        key = "s3 key"
        return key

    def delete(self, key) -> None:
        self.__logger.warning(f"S3 GATEWAY COMING SOON")
        self.__logger.info(f"--- S3 delete {key}")
        pass

    def check(self) -> bool:
        self.__logger.warning(f"S3 GATEWAY COMING SOON")
        self.__logger.info(f"S3 check")
        return True
