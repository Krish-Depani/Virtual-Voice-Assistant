import math
import psutil
import time
from random import randint
import subprocess
import AppOpener
from pynput.keyboard import Key, Controller
from PIL import ImageGrab
import wmi


class SystemTasks:
    def __init__(self):
        self.keyboard = Controller()

    def write(self, text):
        self.keyboard.type(text)

    def select(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('a')
        self.keyboard.release('a')
        self.keyboard.release(Key.ctrl)

    def hitEnter(self):
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def delete(self):
        self.select()
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.backspace)

    def copy(self):
        self.select()
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('c')
        self.keyboard.release('c')
        self.keyboard.release(Key.ctrl)

    def paste(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('v')
        self.keyboard.release('v')
        self.keyboard.release(Key.ctrl)

    def new_file(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('n')
        self.keyboard.release('n')
        self.keyboard.release(Key.ctrl)

    def save(self, name):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('s')
        self.keyboard.release('s')
        self.keyboard.release(Key.ctrl)
        time.sleep(0.2)
        self.write(name)
        self.hitEnter()


class TabOpt:
    def __init__(self):
        self.keyboard = Controller()

    def switchTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.release(Key.ctrl)

    def closeTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('w')
        self.keyboard.release('w')
        self.keyboard.release(Key.ctrl)

    def newTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('t')
        self.keyboard.release('t')
        self.keyboard.release(Key.ctrl)


class WindowOpt:
    def __init__(self):
        self.keyboard = Controller()

    def closeWindow(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.f4)
        self.keyboard.release(Key.f4)
        self.keyboard.release(Key.alt_l)

    def minimizeWindow(self):
        for i in range(2):
            self.keyboard.press(Key.cmd)
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)
            self.keyboard.release(Key.cmd)
            time.sleep(0.05)

    def maximizeWindow(self):
        self.keyboard.press(Key.cmd)
        self.keyboard.press(Key.up)
        self.keyboard.release(Key.up)
        self.keyboard.release(Key.cmd)

    def switchWindow(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.release(Key.alt_l)

    def Screen_Shot(self):
        im = ImageGrab.grab()
        im.save(f'../Data/Screenshots/ss_{randint(1, 100)}.jpg')


def systemInfo():
    c = wmi.WMI()
    my_system_1 = c.Win32_LogicalDisk()[0]
    my_system_2 = c.Win32_ComputerSystem()[0]
    info = f"Total Disk Space: {round(int(my_system_1.Size)/(1024**3),2)} GB\n" \
           f"Free Disk Space: {round(int(my_system_1.Freespace)/(1024**3),2)} GB\n" \
           f"Manufacturer: {my_system_2.Manufacturer}\n" \
           f"Model: {my_system_2. Model}\n" \
           f"Owner: {my_system_2.PrimaryOwnerName}\n" \
           f"Number of Processors: {psutil.cpu_count()}\n" \
           f"System Type: {my_system_2.SystemType}"
    return info


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def system_stats():
    cpu_stats = str(psutil.cpu_percent())
    battery_percent = psutil.sensors_battery().percent
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)
    stats = f"Currently {cpu_stats} percent of CPU, {memory_in_use} of RAM out of total {total_memory} is being used and " \
                f"battery level is at {battery_percent}%"
    return stats


def app_path(app):
    app_paths = {'access': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\ACCICONS.exe',
                 'powerpoint': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\POWERPNT.exe',
                 'word': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\WINWORD.exe',
                 'excel': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\EXCEL.exe',
                 'outlook': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\OUTLOOK.exe',
                 'onenote': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\ONENOTE.exe',
                 'publisher': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\MSPUB.exe',
                 'sharepoint': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\GROOVE.exe',
                 'infopath designer': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\INFOPATH.exe',
                 'infopath filler': 'C:\\Program Files (x86)\\Microsoft Office\\Office14\\INFOPATH.exe'}
    try:
        return app_paths[app]
    except KeyError:
        return None


def open_app(query):
    ms_office = ('access', 'powerpoint', 'word', 'excel', 'outlook', 'onenote', 'publisher', 'sharepoint', 'infopath designer',
                 'infopath filler')
    for app in ms_office:
        if app in query:
            path = app_path(app)
            subprocess.Popen(path)
            return True
    AppOpener.run(query[5:])
    return True

def take_note(note):
    open_app("open notepad")
    time.sleep(0.2)
    sys_task = SystemTasks()
    sys_task.write(note)
    sys_task.save(f'note_{randint(1, 100)}')