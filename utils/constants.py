class Constants(object):
    """..."""
    
    # APPLICATION VERSION
    APP_VERSION = "0.01"
    DEV_FILE_COMPAT_LEVEL = 6
    DEV_FILE_COMPAT_LEVEL_MIN = 0
    USER_GUIDE_FILENAME = "PICkit2 User Guide 51553E.pdf"

    # min firmware version
    FW_VER_MAJOR_REQ = 2
    FW_VER_MINOR_REQ = 32
    FW_VER_DOT_REQ = 0
    FW_FILENAME = "PK2V023200.hex"
    PACKET_SIZE = 65 # 64 + leading 0
    USB_REPORTLENGTH = 64

    BIT_MASK_0 = 0x01
    BIT_MASK_1 = 0x02
    BIT_MASK_2 = 0x04
    BIT_MASK_3 = 0x08
    BIT_MASK_4 = 0x10
    BIT_MASK_5 = 0x20
    BIT_MASK_6 = 0x40
    BIT_MASK_7 = 0x80
    #
    MCHIP_VENDOR_ID = 0x04D8
    PK2_DEVICE_ID = 0x0033
    #
    CONFIG_ROWS = 2
    CONFIG_COLUMNS = 4
    MAX_READ_CFG_MASKS = 8
    NUM_CONFIG_MASKS = 9
    #
    PICKIT2_2USB = {
        'found': None, # implies firmware version is good.
        'not_found': None,
        'write_error': None,
        'read_error': None,
        'firmware_invalid': None,
        'bootloader': None
    }

    PICKIT2_PWR = {
        'no_response': None,
        'vdd_on': None,
        'vdd_off': None,
        'vdderror': None,
        'vpperror': None,
        'vddvpperrors': None,
        'selfpowered': None,
        'unpowered': None
    }

    FILE_READ = {
        'success': None,
        'failed': None,
        'noconfig': None,
        'partialcfg': None,
        'largemem': None
    }

    STATUC_COLOR = {
        'normal': None,
        'green': None,
        'yellow': None,
        'red': None
    }

    VDD_TARGET_SELECT = {
        'auto': None,
        'pickit2': None,
        'target': None
    }

    VDD_THRESHOLD_FOR_SELF_POWERED_TARGET = 2.3
    NO_MESSAGE = False
    SHOW_MESSAGE = True
    UPDATE_MEMORY_DISPLAYS = True
    DONT_UPDATE_MEM_DISPLAYS = False
    ERASE_EE = True
    WRITE_EE = False

    UPLOAD_BUFFER_SIZE = 128
    DOWNLOAD_BUFFER_SIZE = 256
   
    READFWFLASH = 1
    WRITEFWFLASH = 2
    ERASEFWFLASH = 3
    READFWEEDATA = 4
    WRITEFWEEDATA = 5
    RESETFWDEVICE = 0xFF
    NO_OPERATION = 0x5A
    FIRMWARE_VERSION = 0x76
    SETVDD = 0xA0
    SETVPP = 0xA1
    READ_STATUS = 0xA2
    READ_VOLTAGES = 0xA3
    DOWNLOAD_SCRIPT = 0xA4
    RUN_SCRIPT = 0xA5
    EXECUTE_SCRIPT = 0xA6
    CLR_DOWNLOAD_BUFFER = 0xA7
    DOWNLOAD_DATA = 0xA8
    CLR_UPLOAD_BUFFER = 0xA9
    UPLOAD_DATA = 0xAA
    CLR_SCRIPT_BUFFER = 0xAB
    UPLOAD_DATA_NOLEN = 0xAC
    END_OF_BUFFER = 0xAD
    RESET = 0xAE
    SCRIPT_BUFFER_CHKSUM = 0xAF
    SET_VOLTAGE_CALS = 0xB0
    WR_INTERNAL_EE = 0xB1
    RD_INTERNAL_EE = 0xB2
    ENTER_UART_MODE = 0xB3
    EXIT_UART_MODE = 0xB4
    ENTER_LEARN_MODE = 0xB5
    EXIT_LEARN_MODE = 0xB6
    ENABLE_PK2GO_MODE = 0xB7
    LOGIC_ANALYZER_GO = 0xB8
    COPY_RAM_UPLOAD = 0xB9
    # META COMMANDS
    MC_READ_OSCCAL = 0x80
    MC_WRITE_OSCCAL = 0x81
    MC_START_CHECKSUM = 0x82
    MC_VERIFY_CHECKSUM = 0x83
    MC_CHECK_DEVICE_ID= 0x84
    MC_READ_BANDGAP = 0x85
    MC_WRITE_CFG_BANDGAP = 0x86
    MC_CHANGE_CHKSM_FRMT = 0x87
    #
    _VDD_ON = 0xFF
    _VDD_OFF = 0xFE
    _VDD_GND_ON = 0xFD
    _VDD_GND_OFF = 0xFC
    _VPP_ON = 0xFB
    _VPP_OFF = 0xFA
    _VPP_PWM_ON = 0xF9
    _VPP_PWM_OFF = 0xF8
    _MCLR_GND_ON = 0xF7
    _MCLR_GND_OFF = 0xF6
    _BUSY_LED_ON = 0xF5
    _BUSY_LED_OFF = 0xF4
    _SET_ICSP_PINS = 0xF3
    _WRITE_BYTE_LITERAL = 0xF2
    _WRITE_BYTE_BUFFER = 0xF1
    _READ_BYTE_BUFFER = 0xF0
    _READ_BYTE = 0xEF
    _WRITE_BITS_LITERAL = 0xEE
    _WRITE_BITS_BUFFER = 0xED
    _READ_BITS_BUFFER = 0xEC
    _READ_BITS = 0xEB
    _SET_ICSP_SPEED = 0xEA
    _LOOP = 0xE9
    _DELAY_LONG = 0xE8
    _DELAY_SHORT = 0xE7
    _IF_EQ_GOTO = 0xE6
    _IF_GT_GOTO = 0xE5
    _GOTO_INDEX = 0xE4
    _EXIT_SCRIPT = 0xE3
    _PEEK_SFR = 0xE2
    _POKE_SFR = 0xE1

    _ICDSLAVE_RX = 0xE0
    _ICDSLAVE_TX_LIT = 0xDF
    _ICDSLAVE_TX_BUF = 0xDE
    _LOOPBUFFER = 0xDD
    _ICSP_STATES_BUFFER = 0xDC
    _POP_DOWNLOAD = 0xDB
    _COREINST18 = 0xDA
    _COREINST24 = 0xD9
    _NOP24 = 0xD8
    _VISI24 = 0xD7
    _RD2_BYTE_BUFFER = 0xD6
    _RD2_BITS_BUFFER = 0xD5
    _WRITE_BUFWORD_W = 0xD4
    _WRITE_BUFBYTE_W = 0xD3
    _CONST_WRITE_DL = 0xD2

    _WRITE_BITS_LIT_HLD = 0xD1
    _WRITE_BITS_BUF_HLD = 0xD0
    _SET_AUX = 0xCF
    _AUX_STATE_BUFFER = 0xCE
    _I2C_START = 0xCD
    _I2C_STOP = 0xCC
    _I2C_WR_BYTE_LIT = 0xCB
    _I2C_WR_BYTE_BUF = 0xCA
    _I2C_RD_BYTE_ACK = 0xC9
    _I2C_RD_BYTE_NACK = 0xC8
    _SPI_WR_BYTE_LIT = 0xC7
    _SPI_WR_BYTE_BUF = 0xC6
    _SPI_RD_BYTE_BUF = 0xC5
    _SPI_RDWR_BYTE_LIT = 0xC4
    _SPI_RDWR_BYTE_BUF = 0xC3
    _ICDSLAVE_RX_BL = 0xC2
    _ICDSLAVE_TX_LIT_BL = 0xC1
    _ICDSLAVE_TX_BUF_BL = 0xC0
    _MEASURE_PULSE = 0xBF
    _UNIO_TX = 0xBE
    _UNIO_TX_RX = 0xBD
    _JT2_SETMODE = 0xBC
    _JT2_SENDCMD = 0xBB
    _JT2_XFERDATA8_LIT = 0xBA
    _JT2_XFERDATA32_LIT = 0xB9
    _JT2_XFRFASTDAT_LIT = 0xB8
    _JT2_XFRFASTDAT_BUF = 0xB7
    _JT2_XFERINST_BUF = 0xB6
    _JT2_GET_PE_RESP = 0xB5
    _JT2_WAIT_PE_RESP = 0xB4
    #
    SEARCH_ALL_FAMILIES = 0xFFFFFF
    # Script Buffer Reserved Locations
    PROG_ENTRY = 0
    PROG_EXIT = 1
    RD_DEVID = 2
    PROGMEM_RD = 3
    ERASE_CHIP_PREP = 4
    PROGMEM_ADDRSET = 5
    PROGMEM_WR_PREP = 6
    PROGMEM_WR = 7
    EE_RD_PREP = 8
    EE_RD = 9
    EE_WR_PREP = 10
    EE_WR = 11
    CONFIG_RD_PREP = 12
    CONFIG_RD = 13
    CONFIG_WR_PREP = 14
    CONFIG_WR = 15
    USERID_RD_PREP = 16
    USERID_RD = 17
    USERID_WR_PREP = 18
    USERID_WR = 19
    OSSCAL_RD = 20
    OSSCAL_WR = 21
    ERASE_CHIP = 22
    ERASE_PROGMEM = 23
    ERASE_EE = 24
    #ERASE_CONFIG = 25
    ROW_ERASE = 26
    TESTMEM_RD = 27
    EEROW_ERASE = 28

    # OSCCAL valid mask in config masks
    OSCCAL_MASK = 7

    # EEPROM config words
    PROTOCOL_CFG = 0
    ADR_MASK_CFG = 1
    ADR_BITS_CFG = 2
    CS_PINS_CFG = 3
    # EEPROM Protocols
    I2C_BUS = 1
    SPI_BUS = 2
    MICROWIRE_BUS = 3
    UNIO_BUS = 4
    READ_BIT = True
    WRITE_BIT = False

    # for user32.dll window flashing
    #Stop flashing. The system restores the window to its original state. 
    FLASHW_STOP = 0
    #Flash the window caption. 
    FLASHW_CAPTION = 1
    #Flash the taskbar button. 
    FLASHW_TRAY = 2
    #Flash both the window caption and taskbar button.
    #This is equivalent to setting the FLASHW_CAPTION | FLASHW_TRAY flags. 
    FLASHW_ALL = 3
    #Flash continuously, until the FLASHW_STOP flag is set. 
    FLASHW_TIMER = 4
    #Flash continuously until the window comes to the foreground. 
    FLASHW_TIMERNOFG = 12; 

    # PICkit 2 internal EEPROM Locations
    ADC_CAL_L = 0x00
    ADC_CAL_H = 0x01
    CPP_OFFSET = 0x02
    CPP_CAL = 0x03
    UNIT_ID = 0xF0 #through 0xFF

    '''OVERLAPPED = {
        internal: None,
        internal_high: None,
        offset: None,
        offset_high: None,
        h_event: None
    }'''

    # PIC32 related
    P32_PROGRAM_FLASH_START_ADDR = 0x1D000000
    P32_BOOT_FLASH_START_ADDR = 0x1FC00000

    # OSCCAL regeration
    BASELINE_CAL = (
        0x0C00, 0x0025, 0x0067, 0x0068, 0x0069, 0x0066, 0x0CFE, 0x0006, 
        0x0626, 0x0A08, 0x0726, 0x0A0A, 0x0070, 0x0C82, 0x0031, 0x02F0, 
        0x0A0F, 0x02F1, 0x0A0F, 0x0CF9, 0x0030, 0x0CC8, 0x0031, 0x0506, 
        0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x02F0, 0x0A18, 0x0000, 
        0x0CF9, 0x0030, 0x0000, 0x0000, 0x0000, 0x02F1, 0x0A18, 0x0406, 
        0x0A08
    )

    MR16F676FAM_CAL = (
        0x3000, 0x2805, 0x0000, 0x0000, 0x0009, 0x1683, 0x0090, 0x0191, 
        0x019F, 0x30FE, 0x0085, 0x1283, 0x3007, 0x0099, 0x0185, 0x1885, 
        0x280F, 0x1C85, 0x2811, 0x01A0, 0x3082, 0x00A1, 0x0BA0, 0x2816, 
        0x0BA1, 0x2816, 0x30F9, 0x00A0, 0x30C8, 0x00A1, 0x1405, 0x0000, 
        0x0000, 0x0000, 0x0000, 0x0000, 0x0BA0, 0x281F, 0x0000, 0x30F9, 
        0x00A0, 0x0000, 0x0000, 0x0000, 0x0BA1, 0x281F, 0x1005, 0x280F
    )

