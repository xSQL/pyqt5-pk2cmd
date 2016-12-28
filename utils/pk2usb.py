import usb.core
import usb.util

from constants import Constants as CONST

# find our device
dev = usb.core.find(idVendor=CONST.MCHIP_VENDOR_ID, idProduct=CONST.PK2_DEVICE_ID)
print(dev.port_number)
print(dir(dev))

