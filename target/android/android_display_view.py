from webservice_serial.target.target import Target
from webservice_serial.target.android.adb import Adb


class AndroidDisplayView(Target):
    """
    :param string adb_command: Command that call the Android Debug Bridge
                               In Raspberry maybe be a `./adb` executable file
    """
    activity = 'io.github.pedalpi.pedalpi_display/io.github.pedalpi.pedalpi_display.MainActivity'

    def __init__(self, adb_command="adb"):
        super(AndroidDisplayView, self).__init__()
        self.adb = None
        self.adb_command = adb_command

    def init(self, application, port):
        super(AndroidDisplayView, self).init(application, port)

        self.adb = Adb(self.adb_command, application.log)
        self.adb.start(port, AndroidDisplayView.activity)

    def close(self):
        self.adb.close(self.port)
