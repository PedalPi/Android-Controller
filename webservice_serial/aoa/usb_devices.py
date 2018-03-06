from pyudev import Context, Monitor, MonitorObserver

context = Context()
'''
monitor = Monitor.from_netlink(context)
monitor.filter_by(subsystem='input')
def print_device_event(device):
    print('background event {0.action}: {0.device_path}'.format(device))
observer = MonitorObserver(monitor, callback=print_device_event, name='monitor-observer')
print(observer.daemon)
observer.start()

from pyudev import Context, Monitor
context = Context()
monitor = Monitor.from_netlink(context)
monitor.filter_by('input')
device = monitor.poll(timeout=1)
if device:
    print('{0.action}: {0}'.format(device))
'''
import time

#while True:
#    time.sleep(1)

'''
import pyudev
context = pyudev.Context()
monitor = Monitor.from_netlink(context)
# For USB devices
monitor.filter_by(subsystem='usb')
# OR specifically for most USB serial devices
#monitor.filter_by(subsystem='tty')
for action, device in monitor:
    vendor_id = device.get('ID_VENDOR_ID')
    # I know the devices I am looking for have a vendor ID of '22fa'
    print(vendor_id)
    #if vendor_id in ['22fa']:
    #    print('Detected {} for device with vendor ID {}'.format(action, vendor_id))
'''

import usb.core
# find USB devices
dev = usb.core.find(find_all=True)
# loop through devices, printing vendor and product ids in decimal and hex
for cfg in dev:
    try:
        print(cfg.manufacturer)
    except Exception:
        print("error")
    print('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct))
    print('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct))
    print()