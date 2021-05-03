import logging
from src.application.command.clear import ClearCommand
from src.process import Process
from datetime import datetime, timedelta
from src.process.clear.subProcess import Clear


class ClearProcess(Process):
    def __init__(self, logger: logging.Logger, command: ClearCommand):
        self._cmd = command
        super().__init__(self._cmd.config, logger)

    def run(self):
        diffTime = self._cmd.config['DEFAULT'].get(
            'CLEAR_INTERVAL',
            '365'
        )

        for service in self._cmd.services:
            clearGatewayExcept = []
            gateway = self._cmd.config[service].get(
                    'GATEWAY',
                    self._cmd.config['DEFAULT'].get(
                        'GATEWAY',
                        'local'
                    )
                ).split(',')

            if self._cmd.overrideGateway:
                gateway = self._cmd.overrideGateway

            if self._cmd.config[service].get('CLEAR_GATEWAY_EXCEPT', None):
                clearGatewayExcept = self._cmd.config[service].get(
                    'CLEAR_GATEWAY_EXCEPT',
                    None
                ).split(',')

            if self._cmd.overrideClearGatewayExcept is not None:
                clearGatewayExcept = self._cmd.overrideClearGatewayExcept

            clearInterval = self._cmd.config[service].get(
                'CLEAR_INTERVAL',
                diffTime
            )
            if self._cmd.overrideClearInterval is not None:
                clearInterval = self._cmd.overrideClearInterval

            gateway = [x for x in gateway if (x not in clearGatewayExcept)]
            date = datetime.now() - timedelta(days=int(clearInterval))
            Clear(self, service, gateway, date).run()
