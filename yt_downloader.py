from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube

dir = ""

def openLocation():
    global dir
    dir = filedialog.askdirectory()
    if len(dir) > 1:  # a valid directory is selected
        saveLabel.config(text=("Location:    " + dir))       

def DownloadVideo():
    choice = ytdchoices.get()
    url = ytdEntry.get()
    if len(url) > 1:
        global select, size
        select = False
        try: # entry has correct youtube url
            yt = YouTube(url)
            # selecting a quality
            if choice == choices[1]:
                select = yt.streams.filter(progressive=True).first()
                size = str(round((select.filesize/1024000),2))+"MB"
            elif choice == choices[2]:
                select = yt.streams.filter(progressive=True,file_extension='mp4').last()
                size = str(round((select.filesize/1024000),2))+"MB"    
            vidTitle = yt.title
            # checking errors - no quality selected, no directory selected
            if dir == "":
                messagebox.showerror("Error","Select a directory")
            elif select == False:
                 messagebox.showerror("Error","Select a quality")
            else:
                try:
                    select.download(dir)
                    messagebox.showinfo("Success",("Downloaded - \""+vidTitle+"\" ["+size+"]"))
                except:
                    messagebox.showerror("Error","No internet connection")
        except: # entry has some value but it is not a valid youtube url
            messagebox.showerror("Error","Enter a valid YouTube URL")
    else:  # url entry did not get any value
        messagebox.showerror("Error","Please enter a YouTube URL")

root = Tk()
root.title("YouTube Downloader")
root.geometry("345x100")
root.configure(background="#383838")
root.columnconfigure(0,weight=1)
root.resizable(False, False)
root.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))

#url label
ytdLabel = Label(root,fg="#fff",bg="#383838",text="URL: ")
ytdLabel.place(x=10,y=10)
#url entry widget
ytdEntryVar = StringVar()
ytdEntry = Entry(root,width=47,textvariable=ytdEntryVar)
ytdEntry.place(x=48, y=10)
#location label
saveLabel = Label(root,fg="#fff",bg="#383838",text="Location:    No location selected")
saveLabel.place(x=10, y=40)
#select location button
saveEntry = Button(root,width=10,fg="#fff",bg="#383838",text="Select",command=openLocation)
saveEntry.place(x=255, y=36)
#quality label
ytdQuality = Label(root,fg="#fff",bg="#383838",text="Select Quality: ")
ytdQuality.place(x=10, y=70)
#combobox
choices = [" Select a quality"," 720p"," 360p"]
ytdchoices = ttk.Combobox(root,values=choices)
ytdchoices.place(x=100, y=70)
ytdchoices.current(0)
#download button
downloadbtn = Button(root,fg="#fff",bg="#383838",width=10,text="Download",command=DownloadVideo)
downloadbtn.place(x=255, y=66)

root.mainloop()
