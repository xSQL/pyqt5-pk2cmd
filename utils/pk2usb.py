import usb.core
import usb.util
import struct

from .constants import Constants as CONST

class Pk2USB(object):
    """..."""

    device = None
    family = None
    lvp_enabled = False
    vpp_first_enabled = False
    fast_programming = True
    assert_MCLR = False

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
        as_byte = lambda x: struct.pack('<B', x%256)
        b_data = b''.join([as_byte(c) for c in commands])
        for i in range(len(b_data)):
            data[i] = as_byte(b_data[i])
        write = self.ep_out.write(b''.join(data))
        return write

    def read(self):
        """..."""
        read = self.ep_in.read(CONST.PACKET_SIZE-1)
        return read

    def exec_script(self, index):
        """..."""
        script_index = index-1 
        if script_index == -1:
            return False;
        script_length = self.dev_file['Scripts'][script_index]['ScriptLength']
        commands = [
            CONST.CLR_UPLOAD_BUFFER,
            CONST.EXECUTE_SCRIPT,
            script_length
        ] + self.dev_file['Scripts'][script_index]['Script']

        return self.write(commands)

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

    def run_script_upload_no_len(self, script, repetitions):
        """..."""
        commands = [
            CONST.CLR_UPLOAD_BUFFER,
            CONST.RUN_SCRIPT,
            self.scripts_table[script]['redirectToScriptLocation'],
            repetitions,
            CONST.UPLOAD_DATA_NOLEN
        ]
        result = self.write(commands)
        if result:
            result = self.read()
        return result

    def set_MCLR_temp(self, nMCLR):
        """..."""
        if (nMCLR):
            script = [CONST._MCLR_GND_ON]
        else:
            script = [CONST._MCLR_GND_OFF]
        return self.send_script(script)

    def hold_MCLR(self, nMCLR):
        """..."""
        self.assert_MCLR = nMCLR
        if nMCLR:
            script = [CONST._MCLR_GND_ON]
        else:
            script = [CONST._MCLR_GND_OFF]
        return self.send_script(script)

    def upload_data(self):
        """..."""
        commands = [CONST.UPLOAD_DATA]
        result = self.write(commands)
        if (result):
            result = self.read()
        return result

    def upload_data_no_len(self):
        """..."""
        commands = [CONST.UPLOAD_DATA_NOLEN]
        result = self.write(commands)
        if result:
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

    def read_osscal(self):
        """..."""
        family = self.dev_file['Families'][self.family]
        if self.device['OSCCALRdScript']:
            if self.run_script(CONST.PROG_ENTRY, 1):
                self.download_address3(self.device['ProgramMem']-1)
                if self.run_script(CONST.OSSCAL_RD, 1):
                    read = self.upload_data()
                    if read:
                        if self.run_script(CONST.PROG_EXIT, 1):
                            osscal = (read[1] + read[2]*256)
                            if int.from_bytes(family['ProgMemShift'], 'little') > 0:
                                osscal >>= 1
                            #osscal &= family['BlankValue']
                            return osscal
        return False;

    def read_config_outside_prog_mem(self):
        """..."""
        family = self.dev_file['Families'][self.family]
        self.run_script(CONST.PROG_ENTRY, 1)
        self.run_script(CONST.CONFIG_RD, 1)
        data = self.upload_data()
        self.run_script(CONST.PROG_EXIT, 1)
        config_words = int.from_bytes(self.device['ConfigWords'], 'little')
        buffer_index = 1
        for word in range(config_words):
            config = data[buffer_index]
            buffer_index+=1
            config |= data[buffer_index] << 8;
            if int.from_bytes(family['ProgMemShift'], 'big') > 0:
                config = (config >> 1) & family['BlankValue']
            return config

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
        v_fault = int(((threshold * voltage) / 5) * 255)
        if v_fault > 210:
            v_fault = 210

        commands = [
            CONST.SETVDD,
            ccp_value & 0xFF,
            ccp_value>>8,
            v_fault]
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

    def detect_device(self,
        family_index=CONST.SEARCH_ALL_FAMILIES,
        reset_on_not_found=True,
        keep_vdd_on=False
    ):
        """..."""
        if family_index == CONST.SEARCH_ALL_FAMILIES:
            self.set_vdd_voltage(3.3, 0.85)
            for search_index in range(len(self.dev_file['Families'])):
                index = self.dev_file['FamilySearchTable'][search_index]
                if self.dev_file['Families'][index]['PartDetect']:
                    part = self.search_device(index, True, keep_vdd_on)
                    if part:
                        return part
        else:
            self.set_vdd_voltage(self.vdd_last_set, 0.85)
            if self.dev_file['Families'][family_index]['PartDetect']:
                return self.search_device(
                    family_index,
                    reset_on_not_found,
                    keep_vdd_on
                )
            else:
                return True
        return False

    def search_device(self, family_index, reset_on_no_device, keep_vdd_on):
        """..."""
        last_part = self.device
        family = self.dev_file['Families'][family_index]
        vpp = family['Vpp']

        device = dict()

        self.set_vpp_voltage(vpp, 0.7)
        self.set_MCLR_temp(True)
        self.vdd_on()

        if self.vpp_first_enabled and family['ProgEntryVPPScript'] > 0:
            self.exec_script(family['ProgEntryVPPScript'])
        else:
            self.exec_script(family['ProgEntryScript'])

        self.exec_script(family['ReadDevIDScript'])
        data = self.upload_data()
        self.exec_script(family['ProgExitScript'])
        

        if not keep_vdd_on:
            self.vdd_off();

        if not self.assert_MCLR:
            self.hold_MCLR(False)

        device_id = data[4]*0x1000000 + data[3]*0x10000 + data[2]*256 + data[1]


        for shift in range(int.from_bytes(family['ProgMemShift'],'big')):
            device_id >>= 1
        if data[0] == 4:
            last_device_rev = data[4] * 256 + data[3]
            if family['BlankValue'] == 0xFFFFFFFF:
                last_device_rev >>= 4
        else:
            last_device_rev = device_id & ~family['DeviceIDMask']
        last_device_rev &= 0xFFFF
        last_device_rev &= family['BlankValue']
        device_id &= family['DeviceIDMask']


        last_device_id = device_id

        self.device = None
        for part_entry in range(len(self.dev_file['Parts'])):
            if self.dev_file['Parts'][part_entry]['Family'] == family_index:
                if self.dev_file['Parts'][part_entry]['DeviceID'] == device_id:
                    active_part = part_entry;
                    self.family = family_index
                    part = self.dev_file['Parts'][part_entry]
                    self.device = part
                    break

        if self.device:
            self.download_part_scripts(family_index)
            osscal = None
            band_gap = None
            if part['OSSCALSave']:
                self.vdd_on()
                osscal = self.read_osscal()
            if part['BandGapMask'] > 0:
                self.vdd_on()
                #band_gap = self.read_band_gap()
            if not keep_vdd_on:
                self.vdd_off()
            return {
                'part': part,
                'osscal': hex(osscal),
                'band_gap': band_gap
            }
        else:
            return False

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
            'deviceFileScriptNumber': script_array_index-1
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
        commands = commands + script_entry
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
        
        if self.device['ConfigRdScript'] != 0:
            self.download_script(
                CONST.CONFIG_RD,
                self.device['ConfigRdScript']
            )
        if family['ReadDevIDScript']!= 0:
            self.download_script(
                CONST.RD_DEVID,
                family['ReadDevIDScript']
            )
        if self.device['ProgMemRdScript'] != 0:
            self.download_script(
                CONST.PROGMEM_RD,
                self.device['ProgMemRdScript']
            )
        if self.device['ProgMemAddrSetScript'] != 0:
            self.download_script(
                CONST.PROGMEM_ADDRSET,
                self.device['ProgMemAddrSetScript']
            )

    def device_read(self, read_memory=True, read_eeprom=True):
        """..."""
        #upload_buffer = new byte[KONST.UploadBufferSize];

        self.set_MCLR_temp(True)
        self.vdd_on();
        family = self.dev_file['Families'][self.family]
        memory = list()
        if read_memory:
            self.run_script(CONST.PROG_ENTRY, 1)
            if self.device['ProgMemAddrSetScript'] != 0 and \
                self.device['ProgMemAddrBytes'] != 0:
                self.download_address3(0)
                self.run_script(CONST.PROGMEM_ADDRSET, 1)
            bytes_per_word = int.from_bytes(family['BytesPerLocation'], 'little')
            prog_mem_rd_words = self.device['ProgMemRdWords']
            script_runs_to_fill_upload = int(CONST.UPLOAD_BUFFER_SIZE /\
                (prog_mem_rd_words * bytes_per_word))


            words_per_loop = script_runs_to_fill_upload * prog_mem_rd_words
            words_read = 0
            

            while words_read < self.device['ProgramMem']:
                upload_buffer = self.run_script_upload_no_len(
                    CONST.PROGMEM_RD,
                    script_runs_to_fill_upload
                )
                upload_buffer2 = self.upload_data_no_len()
                upload_buffer+=upload_buffer2
                upload_index = 0
                for word in range(words_per_loop):
                   bite = 0
                   mem_word = upload_buffer[upload_index + bite]
                   bite += 1
                   if bite < bytes_per_word:
                       mem_word |= upload_buffer[upload_index + bite] << 8
                       bite+=1
                   if bite < bytes_per_word:
                       mem_word |= upload_buffer[upload_index + bite] << 16
                       bite+=1
                   if bite < bytes_per_word:
                       mem_word |= upload_buffer[upload_index + bite] << 24
                       bite+=1

                   upload_index += bite
                   if int.from_bytes(family['ProgMemShift'], 'big') > 0:
                       mem_word = (mem_word >> 1) & family['BlankValue']
                   memory.append(mem_word)
                   words_read += 1

            self.run_script(CONST.PROG_EXIT, 1)

        return {
            'memory': memory
        }
