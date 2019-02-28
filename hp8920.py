import tkinter as tk
from tkinter import *
import serial
import serial.tools.list_ports
import instruments as ik
import time

window = tk.Tk()
window.title('HP-8920B TEST SET')
window.geometry('700x500')


def serial_port_check():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) <= 0:
        port_info.set('The serial port cannot be found!')
    else:
        str1 = ''
        for i in port_list:
            str1 += str(i) + '\r'
        port_info.set(str1)


port_info = tk.StringVar()
port_check_x = 0
port_check_y = 0
SerialPortCheckButton = tk.Button(window, text='Serial Port Check', width=13, height=1, command=serial_port_check)
SerialPortCheckButton.place(x=port_check_x, y=port_check_y)
SerialPortCheckResults = tk.Label(window, textvariable=port_info, bg='light gray', width=40, height=7)
SerialPortCheckResults.place(x=port_check_x + 100, y=port_check_y)

port_set = StringVar()
port_set_x = 450
port_set_y = 70
PortSet = tk.Label(window, text='Port:', width=3)
PortSet.place(x=port_set_x, y=port_set_y)
PortInput = tk.Entry(window, width=3, textvariable=port_set)
PortInput.place(x=port_set_x + 30, y=port_set_y)
PortInput.insert(END, '5')

addr_set = StringVar()
addr_set_x = 510
addr_set_y = 70
AddrSet = tk.Label(window, text='Addr:', width=3)
AddrSet.place(x=addr_set_x, y=addr_set_y)
AddrInput = tk.Entry(window, width=3, textvariable=addr_set)
AddrInput.place(x=addr_set_x + 30, y=addr_set_y)
AddrInput.insert(END, '15')

baud_set = StringVar()
baud_set_x = 570
baud_set_y = 70
BaudSet = tk.Label(window, text='Baud:', width=3)
BaudSet.place(x=baud_set_x, y=baud_set_y)
BaudInput = tk.Entry(window, width=10, textvariable=baud_set)
BaudInput.place(x=baud_set_x + 30, y=baud_set_y)
BaudInput.insert(END, '9600')

sn_get = StringVar()
sn_get_x = 450
sn_get_y = 120
SNSet = tk.Label(window, text='S/N:', width=3)
SNSet.place(x=sn_get_x, y=sn_get_y)
SNInput = tk.Entry(window, width=10, textvariable=sn_get)
SNInput.place(x=sn_get_x + 30, y=sn_get_y)
SNInput.insert(END, '003300')


def serial_port_verify():
    serial_port = 'COM%s' % port_set.get()
    try:
        ser = serial.Serial(serial_port, int(baud_set.get()), timeout=1)
        ser.close()
        inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)
        port_open.set(inst.name)
    except:
        port_open.set('Port check error')


port_open = StringVar()
port_open.set('Wait for verification')
port_verify_x = 0
port_verify_y = 120
SerialPortVerifyButton = tk.Button(window, text='Serial Port Verify', width=13, height=1, command=serial_port_verify)
SerialPortVerifyButton.place(x=port_verify_x, y=port_verify_y)
SerialPortVerifyResults = tk.Label(window, textvariable=port_open, bg='light gray', width=40, height=1)
SerialPortVerifyResults.place(x=port_verify_x + 100, y=port_verify_y)


def tx_test_set():
    serial_port = 'COM%s' % port_set.get()
    inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)

    inst.sendcmd('*RST')
    inst.sendcmd('*CLS')
    inst.sendcmd('DISP TX;RFAN:TMOD "Auto";PME:DET "Peak"')
    inst.sendcmd('RFAN:INP "RF In";IFBW "230 kHz";TKEY "Off"')
    time.sleep(1)
    inst.sendcmd('AFAN:INPUT "FM DEMOD";FILT1 "300Hz HPF";FILT2 "3kHz LPF";DEMP "Off";DET "Pk+-/2"')
    inst.sendcmd('AFGenerator1:FREQ 1KHz;OUTP 388mV')
    time.sleep(0.5)
    inst.sendcmd('MEAS:RFR:FREQ:ABS:AVER:VAL 40')
    inst.sendcmd('MEAS:RFR:FREQ:ABS:AVER:STAT 1')
    inst.sendcmd('MEAS:RFR:POW:AVER:VAL 40')
    inst.sendcmd('MEAS:RFR:POW:AVER:STAT 1')
    inst.sendcmd('MEAS:AFR:FM:AVER:VAL 40')
    inst.sendcmd('MEAS:AFR:FM:AVER:STAT 1')
    inst.sendcmd('MEAS:AFR:SEL "DISTN";DIST:AVER:VAL 40')
    inst.sendcmd('MEAS:AFR:SEL "DISTN";DIST:AVER:STAT 1')


tx_test_set_x = 0
tx_test_set_y = 160
TXTestSet = tk.Button(window, text='TX Setup', width=7, height=1, command=tx_test_set)
TXTestSet.place(x=tx_test_set_x, y=tx_test_set_y)


def tx_avr_set():
    serial_port = 'COM%s' % port_set.get()
    inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)

    inst.sendcmd('MEAS:RFR:FREQ:ABS:AVER:STAT 0')
    inst.sendcmd('MEAS:RFR:POW:AVER:STAT 0')
    inst.sendcmd('MEAS:AFR:FM:AVER:STAT 0')
    inst.sendcmd('MEAS:AFR:SEL "DISTN";DIST:AVER:STAT 0')


tx_avr_set_x = 150
tx_avr_set_y = 160
TXAVRSet = tk.Button(window, text='Average Off', width=10, height=1, command=tx_avr_set)
TXAVRSet.place(x=tx_avr_set_x, y=tx_avr_set_y)


def tx_setup_verify():
    serial_port = 'COM%s' % port_set.get()
    inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)

    tune_mode = inst.query('RFAN:TMOD?', size=5000)
    print(tune_mode)
    tx_pwr_meas = inst.query('RFAN:PME:DET?', size=5000)
    print(tx_pwr_meas)
    input_port = inst.query('RFAN:INP?', size=5000)
    print(input_port)
    if_filter = inst.query('RFAN:IFBW?', size=5000)
    print(if_filter)
    ext_tx_key = inst.query('RFAN:TKEY?', size=5000)
    print(ext_tx_key)
    af_anl_in = inst.query('AFAN:INPUT?', size=5000)
    print(af_anl_in)
    filter1 = inst.query('AFAN:FILT1?', size=5000)
    print(filter1)
    filter2 = inst.query('AFAN:FILT2?', size=5000)
    print(filter2)
    de_emphasis = inst.query('AFAN:DEMP?', size=5000)
    print(de_emphasis)
    detector1 = inst.query('AFAN:DET?', size=5000)
    print(detector1)
    afgen1_freq = inst.query('AFGenerator1:FREQ?', size=5000)
    print(afgen1_freq)
    afgen1_lvl = inst.query('AFGenerator1:OUTP?', size=5000)
    print(afgen1_lvl)
    inst.sendcmd('*CLS')

    setup_info = 'Tune Mode: ' + tune_mode + '\n'
    setup_info += 'TX Pwr Meas: ' + tx_pwr_meas + '\n'
    setup_info += 'Input Port: ' + input_port + '\n'
    setup_info += 'IF Filter: ' + if_filter + '\n'
    setup_info += 'Ext TX Key: ' + ext_tx_key + '\n'
    setup_info += 'AF Anl In: ' + af_anl_in + '\n'
    setup_info += 'Filter 1: ' + filter1 + '\n'
    setup_info += 'Filter 2: ' + filter2 + '\n'
    setup_info += 'De-Emphasis: ' + de_emphasis + '\n'
    setup_info += 'Detector: ' + detector1 + '\n'
    setup_info += 'AFGen1 Freq: ' + str(round(float(afgen1_freq) / 1000, 1)) + ' kHz\n'
    setup_info += 'AFGen1 Lvl: ' + str(round(float(afgen1_lvl) * 1000, 0)) + ' mV'

    tx_setup_info.set(setup_info)


tx_setup_info = tk.StringVar()
tx_setup_verify_x = 0
tx_setup_verify_y = 190
TXSetupVerifyButton = tk.Button(window, text='Setup Verify', width=10, height=1, command=tx_setup_verify)
TXSetupVerifyButton.place(x=tx_setup_verify_x, y=tx_setup_verify_y)
TXSetupVerifyResults = tk.Label(window, textvariable=tx_setup_info, bg='light gray', width=20, height=20)
TXSetupVerifyResults.place(x=tx_setup_verify_x, y=tx_setup_verify_y + 25)


def tx_test_e2():
    serial_port = 'COM%s' % port_set.get()
    inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)

    inst.sendcmd('MEAS:RES')

    tx_freq = inst.query('MEAS:RFR:FREQ:ABS?', size=10000)
    time.sleep(0.5)
    print(tx_freq)
    inst.sendcmd('*CLS')
    tx_power = inst.query('MEAS:RFR:POW?', size=10000)
    time.sleep(0.5)
    print(tx_power)
    inst.sendcmd('*CLS')
    tx_fm = inst.query('MEAS:AFR:FM?', size=10000)
    time.sleep(0.5)
    print(tx_fm)
    inst.sendcmd('*CLS')
    tx_dst = inst.query('MEAS:AFR:SEL "DISTN";DIST?', size=10000)
    time.sleep(0.5)
    print(tx_dst)
    inst.sendcmd('*CLS')

    freq = str(round(float(tx_freq) / 1000000, 1))

    test_result = 'TX Freq: ' + freq + ' MHz \n'
    test_result += 'TX OPwr: ' + str(round(float(tx_power), 2)) + ' W \n'
    test_result += 'FM Devi: ' + str(round(float(tx_fm) / 1000, 2)) + ' kHz \n'
    test_result += 'TX Dist: ' + str(round(float(tx_dst), 2)) + ' % \n\n'
    tx_test_results.set(test_result)


'''
    filename = sn_get.get()+'-'+freq+'.txt'
    with open(filename, 'w') as result_file:
        result_file.write(str(test_result))
'''

tx_test_results = tk.StringVar()
tx_test_x = 150
tx_test_y = 190
TXTestE2 = tk.Button(window, text='Test TX', width=8, height=1, command=tx_test_e2)
TXTestE2.place(x=tx_test_x, y=tx_test_y)
TXTestResults = tk.Label(window, textvariable=tx_test_results, bg='light gray', width=15, height=20)
TXTestResults.place(x=tx_test_x, y=tx_test_y + 25)


def tx_dev_set():
    serial_port = 'COM%s' % port_set.get()
    inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)

    inst.sendcmd('AFAN:FILT1 "<20Hz HPF";FILT2 "15kHz LPF"')
    inst.sendcmd('AFGenerator1:FREQ 3KHz;OUTP 3888mV')
    inst.sendcmd('MEAS:AFR:FM:AVER:STAT 0')


tx_dev_set_x = 270
tx_dev_set_y = 160
TXDevSet = tk.Button(window, text='High Audio Set', width=11, height=1, command=tx_dev_set)
TXDevSet.place(x=tx_dev_set_x, y=tx_dev_set_y)


def tx_dev_e2():
    serial_port = 'COM%s' % port_set.get()
    inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)

    tx_dev_r = ''
    af_freq = 3.0
    for i in range(28):
        dev = inst.query('MEAS:AFR:FM?', size=10000)
        time.sleep(0.2)
        print(dev)
        if float(dev) > 2450:
            tx_dev_r += str(round(af_freq, 1)) + 'kHz: ' + str(round(float(dev) / 1000, 3)) + 'kHz' + '\n'
        af_freq = round(af_freq - 0.1, 1)
        inst.sendcmd('*CLS')
        if af_freq < 0.3:
            break
        inst.sendcmd('AFGenerator1:FREQ %fKHz' % af_freq)
    tx_dev.set(tx_dev_r)


tx_dev = tk.StringVar()
tx_dev_x = 270
tx_dev_y = 190
TXDev = tk.Button(window, text='Deviation Test', width=11, height=1, command=tx_dev_e2)
TXDev.place(x=tx_dev_x, y=tx_dev_y)
TXDevResults = tk.Label(window, textvariable=tx_dev, bg='light gray', width=15, height=20)
TXDevResults.place(x=tx_dev_x, y=tx_dev_y + 25)


def rx_test_set():
    serial_port = 'COM%s' % port_set.get()
    inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)

    inst.sendcmd('*RST')
    inst.sendcmd('*CLS')
    inst.sendcmd('DISP RX;RFG:FREQ {} MHz;AMPL -119dBm;ATT "off";OUTP "RF out"'.format(freq_get.get()))
    time.sleep(0.5)
    inst.sendcmd('AFG1:FREQ 1 kHz;FM 1.5 kHz')
    inst.sendcmd('AFG2:FREQ 100 Hz; FM "off"')
    inst.sendcmd('AFAN:FILT1 "300Hz HPF";FILT2 "3kHz LPF";ELR 50')


rx_test_set_x = 450
rx_test_set_y = 160
RXTestSet = tk.Button(window, text='RX Setup', width=7, height=1, command=rx_test_set)
RXTestSet.place(x=rx_test_set_x, y=rx_test_set_y)

freq_get = StringVar()
freq_get_x = 530
freq_get_y = 160
FREQSet = tk.Label(window, text='Freq:', width=3)
FREQSet.place(x=freq_get_x, y=freq_get_y)
FreqInput = tk.Entry(window, width=15, textvariable=freq_get)
FreqInput.place(x=freq_get_x + 30, y=freq_get_y)
FreqInput.insert(END, '155')
RXFreqUnit = tk.Label(window, text='MHz', width=5, height=1)
RXFreqUnit.place(x=freq_get_x + 100, y=freq_get_y)


def rx_test_e2():
    serial_port = 'COM%s' % port_set.get()
    inst = ik.generic_scpi.SCPIInstrument.open_gpibusb(serial_port, int(addr_set.get()), timeout=3, write_timeout=3)

    inst.sendcmd('MEAS:AFR:SEL "SINAD"')
    inst.sendcmd('MEAS:AFR:SINAD:AVER:VAL 40')
    inst.sendcmd('MEAS:AFR:SINAD:AVER:STAT 1')
    inst.sendcmd('MEAS:RES')

    rx_freq = inst.query('RFG:FREQ?', size=10000)
    time.sleep(0.3)
    print(rx_freq)

    rx_SINAD = inst.query('MEAS:AFR:SINAD?', size=10000)
    time.sleep(0.3)
    print(rx_SINAD)
    inst.sendcmd('*CLS')

    inst.sendcmd('RFG:AMPL -60dBm')
    inst.sendcmd('MEAS:AFR:SEL "Distn"')
    inst.sendcmd('MEAS:AFR:Distn:AVER:VAL 40')
    inst.sendcmd('MEAS:AFR:Distn:AVER:STAT 1')
    inst.sendcmd('MEAS:RES')

    rx_distn = inst.query('MEAS:AFR:Distn?', size=10000)
    time.sleep(0.3)
    print(rx_distn)
    inst.sendcmd('*CLS')
    rx_aclevel = inst.query('MEAS:AFR:ACL?', size=10000)
    time.sleep(0.3)
    print(rx_aclevel)
    inst.sendcmd('*CLS')

    freq = str(round(float(rx_freq) / 1000000, 1))

    test_result = 'RX Freq: ' + freq + ' MHz \n'
    test_result += 'RX SINAD: ' + str(round(float(rx_SINAD), 2)) + ' dB \n'
    test_result += 'RX Distn: ' + str(round(float(rx_distn), 2)) + ' % \n'
    test_result += 'AC Level: ' + str(round(float(rx_aclevel), 3)) + ' V \n\n'
    rx_test_results.set(test_result)


'''
    filename = sn_get.get()+'-'+freq+'.txt'
    with open(filename, 'w') as result_file:
        result_file.write(str(test_result))
'''

rx_test_results = tk.StringVar()
rx_test_x = 450
rx_test_y = 190
RXTestE2 = tk.Button(window, text='Test RX', width=8, height=1, command=rx_test_e2)
RXTestE2.place(x=rx_test_x, y=rx_test_y)
RXTestResults = tk.Label(window, textvariable=rx_test_results, bg='light gray', width=20, height=20)
RXTestResults.place(x=rx_test_x, y=rx_test_y + 25)

window.mainloop()

