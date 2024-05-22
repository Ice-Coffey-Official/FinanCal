import logging

class customLogging:
    def __init__(self, name):
        self.name = name
        self.Log_Format = "%(message)s"

        logging.basicConfig(
            filename="logfile_pid_{name}.log".format(name=self.name), filemode="w", format=self.Log_Format, level=logging.DEBUG
        )

    def getLogger(self):
        return logging.getLogger()