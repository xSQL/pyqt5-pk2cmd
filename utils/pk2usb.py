import usb.core
import usb.util
import struct

from .constants import Constants as CONST

class Pk2USB(object):
    """..."""

    device = None
    family = None
    lvp_enabled = False
    vpp_first_enabled = True
    fast_programming = True

    def __init__(self, dev_file):
        """..."""

        self.scripts_table = [None for i in range(32)]

        self.dev_file = dev_file
        self.dev = usb.core.find(
            idVendor=CONST.MCHIP_VENDOR_ID,
            idProduct=CONST.PK2_DEVICE_ID
        )
        self.dev.set_configuration()
        cfg = self.dev.get_active_configuration()
        intf = cfg[(0,0)]
        ep_out = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT
        )
        ep_in = usb.util.find_descriptor(
            intf,
            # match the first IN endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN
        )

        self.ep_in = ep_in
        self.ep_out = ep_out

    def write(self, commands):
        """..."""
        data = [CONST.END_OF_BUFFER.to_bytes(1,'little') \
            for i in range(CONST.PACKET_SIZE)]
        as_bytes = lambda x: int(x).to_bytes(
            (x.bit_length() + 7) // 8,
            'little'
        )
        b_data = b''.join([as_bytes(c) for c in commands])

        for i in range(len(b_data)):
            data[i] = b_data[i].to_bytes(1, 'little')
        write = self.ep_out.write(b''.join(data))
        return write

    def read(self):
        """..."""
        return self.ep_in.read(CONST.PACKET_SIZE)

    def exec_script(self, index):
        """..."""
        script_index = index - 1
        if script_index == 0:
            return False;
        script_length = self.dev_file['scripts'][script_index]['ScriptLength'];
        commands = [
            CONST.CLR_UPLOAD_BUFFER,
            CONST.EXECUTE_SCRIPT,
            script_length
        ] + self.dev_file['scripts'][script_index]['Script']
        return self.write(commands);

    def send_script(self, script):
        """..."""
        commands = [CONST.EXECUTE_SCRIPT, len(script)] + script
        return self.write(commands)

    def run_script(self, index, repetitions):
        """..."""

        commands = [
            CONST.CLR_UPLOAD_BUFFER,
            CONST.RUN_SCRIPT,
            self.scripts_table[index]['redirectToScriptLocation'],
            repetitions
        ]

        if self.write(commands):
            if (index == CONST.PROG_EXIT):
                return self.hold_MCLR(False);
        return True

    def hold_MCLR(self, nMCLR):
        """..."""
        assertMCLR = nMCLR
        if nMCLR:
            script = [CONST._MCLR_GND_ON]
        else:
            script = [CONST._MCLR_GND_OFF]
        return self.send_script(script)

    def upload_data(self):
        commands = [CONST.UPLOAD_DATA]
        result = self.write(commands)
        if (result):
            result = self.read()

        return result

    def download_address3(self, address):
        commands = [
            CONST.CLR_DOWNLOAD_BUFFER,
            CONST.DOWNLOAD_DATA,
            3,
            address & 0xFF,
            0xFF & (address >> 8),
            0xFF & (address >> 16)
        ]
        return self.write(commands)

    def read_pk_status(self):
        """..."""
        commands = [CONST.READ_STATUS]
        write = self.write(commands)
        if write:
            read = self.read()
            try:
                return read[1]*256 + read[0]
            except:
                return 0xFFFF
        return 0xFFFF

    def read_unit_id(self):
        commands = [CONST.RD_INTERNAL_EE, CONST.UNIT_ID, 16]
        write = self.write(commands)
        if write:
            read = self.read()
            if read[0] == 0x23:
                for i in range(15):
                    if read[1 + i] == 0:
                        break
                readBytes = read[1:i+1]
                return ''.join([chr(c) for c in readBytes])

    def read_pk_voltages(self):
        commands = [CONST.READ_VOLTAGES];
        write = self.write(commands)
        if write:
            read = self.read()
            adc = read[1] * 256 + read[0]
            vdd = adc / 65536 * 5.0
            adc2 = read[3] * 256 + read[2]
            vpp = adc2 / 65536 * 13.7
            return {
                'vdd': vdd,
                'vpp': vpp
            }
        return False

    def read_osccal(self):
        """..."""
        family = self.dev_file['Families'][self.family]
        if self.device['OSCCALRdScript']:
            if self.run_script(CONST.PROG_ENTRY, 1):
               # self.download_address3(self.device['ProgramMem']-1)
                if self.run_script(CONST.OSSCAL_RD, 1):
                    read = self.upload_data()
                    if read:
                        if self.run_script(CONST.PROG_EXIT, 1):
                            print(read)
                            osscal = (read[1] + read[2]*256)
                            if int.from_bytes(family['ProgMemShift'], 'big') > 0:
                                osscal >>= 1
                            osscal &= family['BlankValue']
                            return osscal
        return False;

    def vdd_on(self):
        commands = [CONST.EXECUTE_SCRIPT, 2, CONST._VDD_GND_OFF, CONST._VDD_ON]
        self.write(commands)

    def vdd_off(self):
        commands = [CONST.EXECUTE_SCRIPT, 2, CONST._VDD_OFF, CONST._VDD_GND_ON]
        self.write(commands)

    def set_vdd_voltage(self, voltage, threshold):
        """..."""
        if voltage < 2.5:
                voltage = 2.5;
        self.vdd_last_set = voltage;
        ccp_value = self.calculate_vdd_cpp(voltage)
        v_fault = ((threshold * voltage) / 5) * 255
        if v_fault > 210:
            v_fault = 210

        commands = [CONST.SETVDD, ccp_value & 0xFF, ccp_value>>8, v_fault]
        return self.write(commands)

    def set_vpp_voltage(self, voltage, threshold):
        """..."""
        ccp_value = 0x40;
        vpp_adc = int(voltage * 18.61);
        v_fault = int(threshold * voltage * 18.61);
        commands = [CONST.SETVPP, ccp_value, vpp_adc, v_fault]
        return self.write(commands);

    def calculate_vdd_cpp(self, voltage):
        """..."""
        ccp_value = int(voltage * 32 + 10.5)
        ccp_value <<= 6
        return ccp_value

    def detect_device(self, family_index, reset_on_not_found, keep_vdd_on):
        """..."""
        if family_index == CONST.SEARCH_ALL_FAMILIES:
            self.set_vdd_voltage(3.3, 0.85)
            for search_index in range(len(self.dev_file['Families'])):
                index = self.dev_file['FamilySearchTable'][search_index]
                if self.dev_file['Families'][index]['PartDetect']:
                    if self.search_device(index, true, keep_vdd_on):
                        return True
                return False
        else:
            self.set_vdd_voltage(self.vdd_last_set, 0.85)
            if self.dev_file['Families'][family_index]['PartDetect']:
                if self.search_device(
                    family_index,
                    reset_on_not_found,
                    keep_vdd_on
                ):
                    return True
                return False
            else:
                return True

    def download_script(self, script_buffer_location, script_array_index):
        """..."""

        redirect_to = script_buffer_location
        for i in range(len(self.scripts_table)):
            if script_array_index ==\
                self.scripts_table[i].get('deviceFileScriptNumber'):
                redirectTo = i
                break
        self.scripts_table[script_buffer_location] ={
            'redirectToScriptLocation': redirect_to,
            'deviceFileScriptNumber': script_array_index
        }
        if script_buffer_location != redirect_to:
            return True

        script_array_index -= 1
        script = self.dev_file['Scripts'][script_array_index]
        script_length = script['ScriptLength']

        commands = [
            CONST.DOWNLOAD_SCRIPT,
            script_buffer_location,
            script_length
        ]
        script_entry = script['Script']
        if self.fast_programming:
            commands += script_entry

        return self.write(commands)

    def download_part_scripts(self, family_index):
        """..."""
        commands = [CONST.CLR_SCRIPT_BUFFER]
        result = self.write(commands)

        family = self.dev_file['Families'][family_index]

        for i in range(len(self.scripts_table)):
            self.scripts_table[i]= {
                'redirectToScriptLocation': 0,
                'deviceFileScriptNumber': 0
            }

        if family['ProgEntryScript'] != 0:
            if self.lvp_enabled and self.device.get('LVPScript') > 0:
                self.download_script(
                    CONST.PROG_ENTRY,
                    self.device['LVPScript']
                )
            elif self.vpp_first_enabled and family['ProgEntryVPPScript'] != 0:
                self.download_script(
                    CONST.PROG_ENTRY,
                    family['ProgEntryVPPScript']
                )
            else:
                self.download_script(
                    CONST.PROG_ENTRY,
                    family['ProgEntryScript']
                )
        if family['ProgExitScript'] != 0:
            self.download_script(
                CONST.PROG_EXIT,
                family['ProgExitScript']
            )

        if self.device['OSCCALRdScript'] != 0:
            self.download_script(
                CONST.OSSCAL_RD,
                self.device['OSCCALRdScript']
            )
