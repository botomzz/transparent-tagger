from typing import Generator, Iterable
from tagger.interrogator import Interrogator
from tagger.interrogators import interrogators
import pyautogui
import pyperclip
import time
from tkinter import ttk
import tkinter

image_path=""
#interrogator = interrogators['wd14-convnextv2.v1']
#interrogator = interrogators['wd-v1-4-convnext-tagger.v3']

#interrogator = interrogators['wd-vit-tagger-v3']
interrogator = interrogators['wd-vit-large-tagger-v3-q8']
#interrogator = interrogators['wd-swinv2-tagger-v3-quint8']
#interrogator = interrogators['z3d-e621-convnext-pugliathomas']
print(interrogators)

#replace tag keyword 
replace_str = {
    "recording":"",
    "user interface":"",
    "fake screenshot":"",
    "fake phone screenshot":"",
    "livestream":"",
    "gameplay mechanics":"",
    "traditional media":"fine media",
}


def tagger():
    tags = image_interrogate_fromBG(True,"")
    tags_str = ', '.join(tags.keys())
    for old in replace_str:
        tags_str=tags_str.replace(old,replace_str[old])
    print("\n\n")
    pyperclip.copy(tags_str)
    print(tags_str+"\n\n")

def capture_background():
    root.withdraw()  # little time disappear window
    time.sleep(0.1)  # waiting a secound
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    #screenshot.save("captured_area.png")
    root.deiconify()  # redisplay
    return screenshot

def image_interrogate_fromBG(tag_escape: bool, exclude_tags: Iterable[str]) -> dict[str, float]:
    im = capture_background()
    result = interrogator.interrogate(im)
    th = spinbox.get()
    if th != "":
        th = float(th)
    else:
        th = 0.1
    return Interrogator.postprocess_tags(
        result[1],
        threshold= th,
        escape_tag=tag_escape,
        replace_underscore=tag_escape,
        exclude_tags=exclude_tags)

root=tkinter.Tk()
root.title("transparent tagger")
root.attributes("-alpha",0.6)
ttk.Style().configure("TP.TFrame", background="white")
frame=ttk.Frame(master=root,style="TP.TFrame",width="500",height="500")#window size
root.attributes("-topmost", True)
spinbox = ttk.Spinbox(frame,from_=0.01,to=1.0,increment=0.01,width=18,font=18)

button = ttk.Button(frame, text="run" ,command=tagger)

spinbox.place(x=0,y=0)
button.place(x=0,y=24)
spinbox.set(0.1)
frame.pack()

root.mainloop()