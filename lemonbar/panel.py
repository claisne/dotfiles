#!/usr/bin/python
# pylint: disable=C0111
# pylint: disable=W0603
# pylint: disable=W0702

import sys
import time
import json
import datetime
import threading
import subprocess
import urllib.request

CLOCK_ICON = '\U0000e016'
LIGHTING_BOLT_ICON = '\U0000e09e'
CPU_ICON = '\U0000e139'
CODE_ICON = '\U0000e1ce'
TERMINAL_ICON = '\U0000e1ec'
BROWSER_ICON = '\U0000e09f'
MISC_ICON = '\U0000e005'
BITCOIN_USD_ICON = '\U0000e223'
DISK_USAGE_ICON = '\U0000e133'

PING = 0
CPU_USAGE = 0
DESKTOPS_FOCUSED = set()
BITCOIN_USD = 0
BITCOIN_USD_CHANGE = 0

def refresh_ping():
    global PING
    try:
        output = subprocess.check_output(['ping', '-c', '1', 'www.google.fr']).decode('utf-8')
        last_line = output.splitlines()[-1]
        ping_s = last_line.split('/')[4]
        PING = float(ping_s)
    except:
        PING = -1

def refresh_cpu_usage():
    global CPU_USAGE
    try:
        output = subprocess.check_output(['mpstat', '-P', 'ALL', '1', '1']).decode('utf-8')
        idle_per = output.splitlines()[3].split()[-1]
        CPU_USAGE = 100 - float(idle_per)
    except:
        CPU_USAGE = -1

def refresh_bitcoin_usd():
    global BITCOIN_USD
    global BITCOIN_USD_CHANGE
    try:
        resp = urllib.request.urlopen('https://api.gdax.com/products/btc-usd/book').read()
        data = json.loads(resp)
        btc_usd_last = float(data['asks'][0][0])
        resp = urllib.request.urlopen('https://api.gdax.com/products/btc-usd/stats').read()
        data = json.loads(resp)
        btc_usd_open = float(data['open'])
        BITCOIN_USD = btc_usd_last
        BITCOIN_USD_CHANGE = ((btc_usd_last - btc_usd_open) / btc_usd_open) * 100
    except:
        BITCOIN_USD = -1
        BITCOIN_USD_CHANGE = -1

def thread_target(refresher, delay):
    def target():
        while True:
            refresher()
            time.sleep(delay)
    return target

threading.Thread(target=thread_target(refresh_ping, 10)).start()
threading.Thread(target=thread_target(refresh_cpu_usage, 10)).start()
threading.Thread(target=thread_target(refresh_bitcoin_usd, 30)).start()

def cpu():
    return '{}{:.0f}%%'.format(CPU_ICON, CPU_USAGE)

def ping():
    return '{}{:.0f}ms'.format(LIGHTING_BOLT_ICON, PING)

def clock():
    return '{}{}'.format(CLOCK_ICON, datetime.datetime.now().strftime('%H:%M %a %b %d'))

def bitcoin_usd():
    bitcoin_usd_s = '{}{:.0f}${:+.0f}%%'.format(BITCOIN_USD_ICON, BITCOIN_USD, BITCOIN_USD_CHANGE)
    bitcoin_usd_s = '%{A:chromium cryptowat.ch/gdax/btcusd:}' + bitcoin_usd_s + '%{A}'
    return bitcoin_usd_s

def disk_usage():
    disk_usage_s = '-1%'
    output = subprocess.check_output(['df'])
    for line in output.splitlines():
        parts = line.decode('utf-8').split()
        if parts[0] == '/dev/sda4':
            disk_usage_s = parts[-2]
    return '{}{}'.format(DISK_USAGE_ICON, disk_usage_s)

def desktop(name, icon, description):
    desktop_s = ' {} {} '.format(icon, description)
    if name in DESKTOPS_FOCUSED:
        desktop_s = '%{+u}%{B#aa111111}%{U#aaffffff}' + desktop_s + '%{U-}%{B-}%{-u}'
    return desktop_s

def left_panel_left():
    left_panel_left_s = '%{l}'
    left_panel_left_s += desktop('I', BROWSER_ICON, 'Browser')
    left_panel_left_s += desktop('II', MISC_ICON, 'Misc')
    return left_panel_left_s

def right_panel_left():
    right_panel_left_s = '%{l}'
    right_panel_left_s += desktop('III', CODE_ICON, 'Code')
    right_panel_left_s += desktop('IV', TERMINAL_ICON, 'Terminals')
    return right_panel_left_s

def panel_right():
    return '%{r}' + ' '.join([bitcoin_usd(), ping(), cpu(), disk_usage(), clock()]) + '  '

def panel():
    right = panel_right()
    left_final = left_panel_left() + right
    right_final = right_panel_left() + right
    return '%{S0}' + left_final + '%{S1}' + right_final

def print_panel():
    print(panel())
    sys.stdout.flush()

def bspc_subscriber():
    global DESKTOPS_FOCUSED
    process = subprocess.Popen(['bspc', 'subscribe', 'report'], stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, ''):
        desktops_focused = set()
        parts = str(line).split(':')
        for part in parts:
            evt_type = part[0]
            desktop_name = part[1:]
            if evt_type.lower() == 'o' or evt_type.lower() == 'f':
                focused = evt_type.isupper()
                if focused:
                    desktops_focused.add(desktop_name)
        if desktops_focused != DESKTOPS_FOCUSED:
            DESKTOPS_FOCUSED = desktops_focused
            print_panel()

threading.Thread(target=bspc_subscriber).start()

while True:
    time.sleep(1)
    print_panel()
