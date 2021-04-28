from converter import case

class Gateway:

    @staticmethod
    def get(gatewayPath):
        try:
            modulePath = f'gateways.{gatewayPath}'
            modName = case.pascal(string=modulePath.split('.')[-1], replaceSeparator='-')
            modName = case.pascal(string=modName, replaceSeparator='_')
            gateway = Gateway.load_module(modulePath, modName)
            return getattr(gateway, modName)()
        except Exception as e:
            print(f"gateway error {gatewayPath} {e}")

    @staticmethod
    def load_module(modPath, modName):
        return __import__(modPath, fromlist=[modName])
