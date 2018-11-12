#!/usr/bin/pypy3
# -*- coding: utf-8 -*-

import funcs_forload.pyperclip as pyperclip
from tkinter.messagebox import showerror, showinfo
import p_youtube_loader, os, sys, _thread
from tkinter import *
from tkinter.filedialog import asksaveasfilename


# paste from clipboadr
def onPaste(self):
    try:
        self.text = pyperclip.paste()
        pp = self.text
        print(pp)
    except TclError:
        showerror('Youtube Downloader', 'Nothing to paste into URL-field from Clipboard')
        return
    self.content['video_url for download:'].insert(0, str(self.text))


#start download process video
def transfer(self, video_url, directory=None, file_name=None, quality_mode=None, ):
    try:
        self.do_transfer(video_url, directory, file_name, quality_mode)
        # print('saved in "%s"'  % (p_youtube_loader.tmp_dir))
    except:
        print('Download failed', end=' ')
        print(sys.exc_info()[0], sys.exc_info()[1])
        self.mutex.acquire()
        self.threads -= 1
        self.mutex.release()


#start
def onSubmit(self):
    #Form.onSubmit(self)
    # Collect all data from fields of form (databox)
    video_url = self.content['video_url for download:'].get()
    print(video_url)
    quality_mode  = int(self.content['quality_mode or press enter'].get())
    print("choosed quality_mode is ", quality_mode)

    directory = self.content['Saving_directory'].get()
    if directory == '': directory = None
    else: directory = os.path.normpath(directory)

    file_name = self.content['Saving_file_name'].get()
    if file_name == '':
        file_name = None
    else:
        extension=".mp4"
        if file_name[-4:]!=extension:
            file_name=str(file_name).replace(".","-")
            file_name+=extension
        print("choosed file name is ", file_name)

    self.mutex.acquire()
    self.threads += 1
    self.mutex.release()
    ftpargs = (video_url, directory, file_name, quality_mode)
    _thread.start_new_thread(self.transfer, ftpargs)
    showinfo(self.title, 'download of "%s" started' % (p_youtube_loader.tmp_filename))


# exit from program
def onCancel(self):
    if self.threads == 0:
        print("Bye!!!")
        Tk().quit()
    else:
        showinfo(self.title,'Cannot exit: %d threads running' % self.threads)



def onSave(self):  # save as file dialog
    save_as_file = asksaveasfilename()
    directory = os.path.dirname(save_as_file)
    file_name = os.path.basename(save_as_file)
    self.content['Saving_directory'].delete(0, END)
    self.content['Saving_directory'].insert(0, str(directory))
    self.content['Saving_file_name'].delete(0, END)
    self.content['Saving_file_name'].insert(0, str(file_name))


def closing(self): self.quality_modes.grid_forget()

def update_button(self):
    print('TEST2')
    tmp=self.content['quality_mode or press enter'].get()
    if tmp.isdigit(): self.var.set(tmp)
    else:
        self.var.set(1)
        self.content['quality_mode or press enter'].delete(0, END)
        self.content['quality_mode or press enter'].insert(0, 1)

    self.quality_modes.grid(row=0, column=2, rowspan=2, sticky=NSEW)
    self.children=self.quality_modes.winfo_children()
    print('children: ',self.children)
    for child in self.children[1:]:
        child.destroy()
    for key in self.content_modes:
        Radiobutton(self.quality_modes, text=self.content_modes[key], command=self.onPress, variable=self.var, value=key).pack(
                anchor=NW)
    #self.var.set(1)

    def funccommand(self=self):
        # func(self) <- this solution will not work in GUI_Download_start
        return eval("self.closing()")

    buttclosing=Button(self.quality_modes, text="<<<", command=funccommand)
    buttclosing.pack()

    self.quality_modes.update()


def add_quality(self):
    video_url = self.content['video_url for download:'].get()
    self.content_modes=p_youtube_loader.analise(video_url)
    content_modes=self.content_modes
    print(content_modes)
    self.update_button()





def onPress(self):
    pick=self.var.get()
    #print('you pressed ', pick)
    #print('result',self.content_modes[pick])
    self.content['quality_mode or press enter'].delete(0, END)
    self.content['quality_mode or press enter'].insert(0, pick)









