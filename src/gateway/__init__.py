class Gateway:

    @staticmethod
    def get(gatewayPath):
        modulePath = f'gateways.{gatewayPath}'
        modName = (modulePath.split('.')[-1]).capitalize()
        gateway = Gateway.load_module(modulePath, modName)
        return getattr(gateway, modName)()

    @staticmethod
    def load_module(modPath, modName):
        return __import__(modPath, fromlist=[modName])
