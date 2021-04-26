from gateways.GatewayABC import GatewayABC


class S3(GatewayABC):
    def send(self, archivePath):
        print(f"--- S3 send {archivePath}")
        pass

    def delete(self, archiveName):
        print(f"--- S3 delete {archiveName}")
        pass
