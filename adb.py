import os


class Adb(object):
    """
    :param string command: Command that call the Android Debug Bridge
                           In Raspberry maybe be a `./adb` executable file
    :param callable log: Log function to show the command called
                         If None, not call
    """

    def __init__(self, command="adb", log=None):
        self.command = command
        self.log = log

    def start(self, port, activity):
        self.execute('shell am start -n {}'.format(activity))
        self.execute('forward --remove-all')
        self.execute('forward tcp:{} tcp:{}'.format(port, port))

    def execute(self, command):
        command = '{} {}'.format(self.command, command)
        if self.log is not None:
            self.log('ADB - {}'.format(command))

        os.system(command)

    def close(self, port):
        self.execute('forward --remove tcp:{}'.format(port))
