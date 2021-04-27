from gateways.GatewayABC import GatewayABC


class S3(GatewayABC):
    def send(self, archivePath) -> str:
        print(f"--- S3 send {archivePath}")
        key = "s3 key"
        return key

    def delete(self, key):
        print(f"--- S3 delete {key}")
        pass
