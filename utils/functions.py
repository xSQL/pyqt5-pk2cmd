#!/usr/bin/env python

from constants import Constants
from binary import BinaryReader


def read_device_file(device_file):
    bin_read = BinaryReader(device_file)
    parts = list()
    families = list()
    scripts = list()
    devfile = {
        'info': {
            'VersionMajor': bin_read.read_int32(),
            'VersionMinor': bin_read.read_int32(),
            'VersionDot': bin_read.read_int32(),
            'VersionNotes': bin_read.read_string(),
            'number_families': bin_read.read_int32(),
            'number_parts': bin_read.read_int32(),
            'number_scripts': bin_read.read_int32(),
            'Compatibility': bin_read.read_byte(),
            'UNUSED1A': bin_read.read_byte(),
            'UNUSED1B': bin_read.read_uint16(),
            'UNUSED2': bin_read.read_uint32()
        }
    }
    i=0
    while i<devfile['info']['number_families']:
        data = {
            'FamilyID': bin_read.read_uint16(),
            'FamilyType': bin_read.read_uint16(),
            'SearchPriority': bin_read.read_uint16(),
            'FamilyName': bin_read.read_string(),
            'ProgEntryScript': bin_read.read_uint16(),
            'ProgExitScript': bin_read.read_uint16(),
            'ReadDevIDScript': bin_read.read_uint16(),
            'DeviceIDMask': bin_read.read_uint32(),
            'BlankValue': bin_read.read_uint32(),
            'BytesPerLocation': bin_read.read_byte(),
            'AddressIncrement': bin_read.read_byte(),
            'PartDetect': bin_read.read_boolean(),
            'ProgEntryVPPScript': bin_read.read_uint16(),
            'UNUSED1': bin_read.read_uint16(),
            'EEMemBytesPerWord': bin_read.read_byte(),
            'EEMemAddressIncrement': bin_read.read_byte(),
            'UserIDHexBytes': bin_read.read_byte(),
            'UserIDBytes': bin_read.read_byte(),
            'ProgMemHexBytes': bin_read.read_byte(),
            'EEMemHexBytes': bin_read.read_byte(),
            'ProgMemShift': bin_read.read_byte(),
            'TestMemoryStart': bin_read.read_uint32(),
            'TestMemoryLength': bin_read.read_uint16(),
            'Vpp': bin_read.read_single(),
        }
        families.append(data)
        i+=1

    i=0
    while i<devfile['info']['number_parts']:
        data = {
            'PartName': bin_read.read_string(),
            'Family': bin_read.read_uint16(),
            'DeviceID': bin_read.read_uint32(),
            'ProgramMem': bin_read.read_uint32(),
            'EEMem': bin_read.read_uint16(),
            'EEAddr': bin_read.read_uint32(),
            'ConfigWords': bin_read.read_byte(),
            'ConfigAddr': bin_read.read_uint32(),
            'UserIDWords': bin_read.read_byte(),
            'UserIDAddr': bin_read.read_uint32(),
            'BandGapMask': bin_read.read_uint32(),
            # Init config arrays
            'config_masks': [],
            'config_blank': []
        }
        j = 0
        while j<Constants.MAX_READ_CFG_MASKS:
            data['config_masks'].append(bin_read.read_uint16())
            j+=1
        j = 0
        while j<Constants.MAX_READ_CFG_MASKS:
            data['config_blank'].append(bin_read.read_uint16())
            j+=1

        data2 = {
            'CPMask': bin_read.read_uint16(),
            'CPConfig': bin_read.read_byte(),
            'OSSCALSave': bin_read.read_boolean(),
            'IgnoreAddress': bin_read.read_uint32(),
            'VddMin': bin_read.read_single(),
            'VddMax': bin_read.read_single(),
            'VddErase': bin_read.read_single(),
            'CalibrationWords': bin_read.read_byte(),
            'ChipEraseScript': bin_read.read_uint16(),
            'ProgMemAddrSetScript': bin_read.read_uint16(),
            'ProgMemAddrBytes': bin_read.read_byte(),
            'ProgMemRdScript': bin_read.read_uint16(),
            'ProgMemRdWords': bin_read.read_uint16(),
            'EERdPrepScript': bin_read.read_uint16(),
            'EERdScript': bin_read.read_uint16(),
            'EERdLocations': bin_read.read_uint16(),
            'UserIDRdPrepScript': bin_read.read_uint16(),
            'UserIDRdScript': bin_read.read_uint16(),
            'ConfigRdPrepScript': bin_read.read_uint16(),
            'ConfigRdScript': bin_read.read_uint16(),
            'ProgMemWrPrepScript': bin_read.read_uint16(),
            'ProgMemWrScript': bin_read.read_uint16(),
            'ProgMemWrWords': bin_read.read_uint16(),
            'ProgMemPanelBufs': bin_read.read_byte(),
            'ProgMemPanelOffset': bin_read.read_uint32(),
            'EEWrPrepScript': bin_read.read_uint16(),
            'EEWrScript': bin_read.read_uint16(),
            'EEWrLocations': bin_read.read_uint16(),
            'UserIDWrPrepScript': bin_read.read_uint16(),
            'UserIDWrScript': bin_read.read_uint16(),
            'ConfigWrPrepScript': bin_read.read_uint16(),
            'ConfigWrScript': bin_read.read_uint16(),
            'OSCCALRdScript': bin_read.read_uint16(),
            'OSCCALWrScript': bin_read.read_uint16(),
            'DPMask': bin_read.read_uint16(),
            'WriteCfgOnErase': bin_read.read_boolean(),
            'BlankCheckSkipUsrIDs': bin_read.read_boolean(),
            'IgnoreBytes': bin_read.read_uint16(),
            'ChipErasePrepScript': bin_read.read_uint16(),
            'BootFlash': bin_read.read_uint32(),
            #'UNUSED4': bin_read.read_uint32();
            'Config9Mask': bin_read.read_uint16(),
            'Config9Blank': bin_read.read_uint16(),
            'ProgMemEraseScript': bin_read.read_uint16(),
            'EEMemEraseScript': bin_read.read_uint16(),
            'ConfigMemEraseScript': bin_read.read_uint16(),
            'reserved1EraseScript': bin_read.read_uint16(),
            'reserved2EraseScript': bin_read.read_uint16(), 
            'TestMemoryRdScript': bin_read.read_uint16(),
            'TestMemoryRdWords': bin_read.read_uint16(),
            'EERowEraseScript': bin_read.read_uint16(),
            'EERowEraseWords': bin_read.read_uint16(),
            'ExportToMPLAB': bin_read.read_boolean(),
            'DebugHaltScript': bin_read.read_uint16(),
            'DebugRunScript': bin_read.read_uint16(),
            'DebugStatusScript': bin_read.read_uint16(),
            'DebugReadExecVerScript': bin_read.read_uint16(),
            'DebugSingleStepScript': bin_read.read_uint16(),
            'DebugBulkWrDataScript': bin_read.read_uint16(),
            'DebugBulkRdDataScript': bin_read.read_uint16(),
            'DebugWriteVectorScript': bin_read.read_uint16(),
            'DebugReadVectorScript': bin_read.read_uint16(),
            'DebugRowEraseScript': bin_read.read_uint16(),
            'DebugRowEraseSize': bin_read.read_uint16(),
            'DebugReserved5Script': bin_read.read_uint16(),
            'DebugReserved6Script': bin_read.read_uint16(),
            'DebugReserved7Script': bin_read.read_uint16(),
            'DebugReserved8Script': bin_read.read_uint16(),
            #'DebugReserved9Script': bin_read.read_uint16(),       
            'LVPScript': bin_read.read_uint16()
        }
        data.update(data2)
        parts.append(data)
        i+=1
    i = 0
    while i < devfile['info']['number_scripts']:
        data = {
            'ScriptNumber': bin_read.read_uint16(),
            'ScriptName': bin_read.read_string(),
            'ScriptVersion': bin_read.read_uint16(),
            'UNUSED1':  bin_read.read_uint32(),
            'script_length': bin_read.read_uint16(),
            'script': [],
            'comment': ''
        }
        j = 0
        while j<data['script_length']:
            data['script'].append(bin_read.read_uint16())
            j += 1
        data['comment'] = bin_read.read_string()
        scripts.append(data)
        i += 1
    return {
        'devfile': devfile,
        'families': families,
        'parts': parts,
        'scripts': scripts
    }

         

print(read_device_file('PK2DeviceFile.dat'))
        

