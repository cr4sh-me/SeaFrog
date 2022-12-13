import time
import random
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
# from modules.banner import *
from tkinter import filedialog as fd
from modules.views import viewUrl
import threading
from modules.data import useragent_path, proxies_path

# Create variables
success = 0
fails = 0
useragent = 'loading...'
proxies = 'loading...'
running = True

# Functions
def btns_disable():
    StartBtnTabOne["state"] = "disabled"
    ClearAll["state"] = "disabled"
    ResetProxy["state"] = "disabled"
    ThreadingTabOne["state"] = "disabled"
    UrlTabOne["state"] = "disabled"
    TimesTabOne["state"] = "disabled"

def btns_enable():
    StartBtnTabOne["state"] = "enabled"
    ClearAll["state"] = "normal"
    ResetProxy["state"] = "normal"
    ThreadingTabOne["state"] = "normal"
    UrlTabOne["state"] = "normal"
    TimesTabOne["state"] = "normal"

def clearAll():
    UrlTabOne.delete(0, tk.END)
    TimesTabOne.delete(0, tk.END)

def resetProxy():
    global useragent, proxies
    with open(useragent_path , encoding="utf-8") as f:
        useragent = random.choice(f.readlines()).split("\n")[0]

    with open("./files/proxies.txt" , encoding="utf-8") as f:
        proxies = random.choice(f.readlines()).split("\n")[0]

    ProxyStatus['text'] = 'Proxy: %s' % proxies

def finishRun(x):        
    timer = round((time.time() - x) ,2)
    TimeCount['text'] = 'Time: %ss' % timer
    ProgressStatus['text'] = 'Status: Finished!' 
    btns_enable()

def checkViewUrl():

    global success, fails

    # Validate user input
    if len(UrlTabOne.get()) == 0 or len(TimesTabOne.get()) == 0: 
        messagebox.showwarning("Dumb alert!", "Empty input... Use brain!")
        return False

    # Reset these
    success = 0
    fails = 0
    TextSuccess['text'] = 'Success: 0'
    TextFailed['text'] = 'Failed: 0'
    TimeCount['text'] = 'Time: Measurement...'
    ProgessBarTabOne['value'] = 0

    ProgressStatus['text'] = 'Progress: Preparing...'

    # Disable buttons
    btns_disable() 

    # Setup
    limit = int(TimesTabOne.get())
    ProgessBarTabOne['maximum'] = limit
    ProxyStatus['text'] = 'Proxy: %s' % proxies

 
    # Check for threading option
    if checkVar.get() == 0:
        ProgressStatus['text'] = 'Status: Running...' 
        start_time = time.time()
        for i in range(limit):
            cmd = viewUrl(UrlTabOne.get(), useragent, proxies)
            if cmd == True:
                success = success + 1
                TextSuccess['text'] = 'Success: %s' % success
                ProgessBarTabOne['value'] = success
                root.update()
            else:
                fails = fails + 1
                TextFailed['text'] = 'Fails: %s' % fails
                ProgessBarTabOne['value'] += 1
                root.update()
        finishRun(start_time)
    else:
        cmd = viewUrl(UrlTabOne.get(), useragent, proxies)
        threads = []
        start_time = time.time()
        ProgressStatus['text'] = 'Status: Running threads...' 
        
        for i in range(limit):
            threads.append(threading.Thread(target=viewUrl, args=(UrlTabOne.get(), useragent, proxies)))
            if cmd == True:
                success = success + 1
                TextSuccess['text'] = 'Success: %s' % success
                ProgessBarTabOne['value'] = success
                root.update()
            else:
                fails = fails + 1
                TextFailed['text'] = 'Fails: %s' % fails
                ProgessBarTabOne['value'] += 1
                root.update()
            

        for thread in threads:
            thread.start()
        finishRun(start_time)

root = tk.Tk()
style = ttk.Style()
root.iconbitmap("./icon/seeker_icon.ico")
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

root.title('SeaFrog v1.0')
root.geometry("850x650")
root.resizable(False, False)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Views bot')
tabControl.add(tab2, text='About')

Banner = ImageTk.PhotoImage(Image.open('./icon/banner.png'))
LabelImage = ttk.Label(tab1, image=Banner)
UrlLabelTabOne = ttk.Label(tab1, text='Enter Your URL:')
UrlTabOne = ttk.Entry(tab1, width=50)
UrlTabOne.insert(0, 'https://example.com') # Placeholder 
TimesLabelTabOne = ttk.Label(tab1, text='Views:')
TimesTabOne = ttk.Entry(tab1, width=10)
TimesTabOne.insert(1, '100') # Placeholder 

checkVar = tk.IntVar()
ThreadingTabOne = ttk.Checkbutton(tab1, text='Multi-Threading (beta)', onvalue=1, offvalue=0, variable=checkVar)

ClearAll = ttk.Button(tab1, text='Clear', command=clearAll)
StartBtnTabOne = ttk.Button(tab1, text='Start', command=checkViewUrl)
ResetProxy = ttk.Button(tab1, text='Reset proxy', command=resetProxy)

ProgessBarTabOne = ttk.Progressbar(tab1, orient='horizontal', mode='determinate', length=400, value=0)
TextFailed = ttk.Label(tab1, text='Failed: 0')
TextSuccess = ttk.Label(tab1, text='Success: 0')
TimeCount = ttk.Label(tab1, text='Time: none')
ProgressStatus = ttk.Label(tab1, text='Status: none')
ProxyStatus = ttk.Label(tab1, text=f'Proxy: {proxies}')

LabelImage.place(relx=.5, rely=.1, anchor="center")

UrlLabelTabOne.place(relx=.3, rely=.3, anchor="center")
UrlTabOne.place(relx=.6, rely=.3, anchor="center")

TimesLabelTabOne.place(relx=.3, rely=.4, anchor="center")
TimesTabOne.place(relx=.6, rely=.4, anchor="center")

ThreadingTabOne.place(relx=.5, rely=.5, anchor="center")

ClearAll.place(relx=.4, rely=.6, anchor="center")
StartBtnTabOne.place(relx=.5, rely=.6, anchor="center")
ResetProxy.place(relx=.6, rely=.6, anchor="center")

ProgessBarTabOne.place(relx=.5, rely=.7, anchor="center")

TextFailed.place(relx=.4, rely=.8, anchor="center")
TextSuccess.place(relx=.6, rely=.8, anchor="center")
TimeCount.place(relx=.3, rely=.9, anchor="center")
ProgressStatus.place(relx=.5, rely=.9, anchor="center")
ProxyStatus.place(relx=.7, rely=.9, anchor="center")

# Second tab

nowarranty = '''No Warranty. LICENSOR PROVIDES THE LICENSED PROPERTY AND LICENSED IP ON AN "AS IS" BASIS WITHOUT WARRANTY OF ANY KIND. LICENSOR EXPRESSLY DISCLAIMS ALL WARRANTIES AND CONDITIONS, EITHER EXPRESS OR IMPLIED, WITH RESPECT TO THE LICENSED PROPERTY AND LICENSED IP, INCLUDING ALL IMPLIED WARRANTIES AND CONDITIONS OF MERCHANTABILITY, NONINFRINGEMENT, TITLE AND FITNESS FOR A PARTICULAR PURPOSE, OR ARISING OUT OF A COURSE OF DEALING, USAGE OR TRADE PRACTICE. LICENSOR SPECIFICALLY DISCLAIMS ANY WARRANTY THAT THE FUNCTIONS CONTAINED IN THE IT PROPERTY WILL MEET ASPENTECH'S REQUIREMENTS OR WILL OPERATE IN COMBINATIONS OR IN A MANNER SELECTED FOR USE BY ASPENTECH, OR THAT THE OPERATION OF ANY LICENSED PROPERTY WILL BE UNINTERRUPTED OR ERROR FREE.'''

Info = ttk.Label(tab2, text='Created by @cr4sh https://github.com/cr4sh/seafrog')
Warranty = tk.Text(tab2, height=8, width=80)
scroll_bar = tk.Scrollbar(tab2)

Warranty.config(state='normal')
Warranty.insert(tk.END, nowarranty)
Warranty.config(state='disabled')

scroll_bar.config(command=Warranty.yview)

Info.place(relx=.5, rely=.2, anchor="center")
Warranty.place(relx=.5, rely=.5, anchor="center")
scroll_bar.place(relx=.9, rely=.5, anchor="center")



tabControl.pack(expand=1, fill='both')

# Set proxy and useragent for the first time
resetProxy()

root.mainloop()  