from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import json
from tkinter.colorchooser import askcolor
import sys
import shutil

# get data stuff
def get_resource_path(filename):
    if getattr(sys, 'frozen', False):

        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, filename)


def open_game(): 
    folder = filedialog.askdirectory()
    if not folder:
        return
    global gamefile
    gamefile = get_resource_path(os.path.join(folder, "game.json"))
    if not os.path.exists(gamefile):
        messagebox.showerror('Error', langdata['nojson'])
        return
    global bi
    bi = {}
    load()

def load():
    global f
    with open(gamefile, 'r+', encoding="utf-8") as f:
        global data
        data = json.load(f)
        count = 1
    # there may be buttons that are already there, so I will use this.
    button_deleter(root)
    for i in data['sprites'].values():
        global button
        button = ttk.Button(root, text=i['name'])
        bi[i['name']] = button
        count += 1
        button.pack(anchor='w')
        button.configure(command=lambda name = i['name']: set(name))
    ttk.Button(root, text='+', command=add_sprite).pack(anchor='w')
    ttk.Button(root, text=langdata['openbt1'], command=delete).pack(anchor='w')
    ttk.Button(root, text=langdata['openbt2'], command=TextEditor).pack(anchor='w')
    ttk.Button(root, text=langdata['openbt3']).pack(anchor='w')
    # print(data) - debugging stuff yea

def add_sprite():
    global asktab
    asktab = Toplevel(root)
    asktab.geometry('200x300')
    Label(asktab, text=langdata['asktab1']).pack()
    nameentry = Entry(asktab)
    nameentry.pack(anchor='w')
    def txt_selected():
        global type
        type = 'text'
    def img_selected():
        global type
        type = 'image'
    type = 'text'
    txt = ttk.Radiobutton(asktab, text=langdata['asktab2'], command=txt_selected, value=1)
    img = ttk.Radiobutton(asktab, text=langdata['asktab3'], command=img_selected, value=2)
    txt.pack(anchor='w')
    img.pack(anchor='w')
    Label(asktab, text=langdata['asktab4']).pack()
    xentry = ttk.Entry(asktab)
    xentry.pack(anchor='w')
    Label(asktab, text=langdata['asktab5']).pack()
    yentry = ttk.Entry(asktab)
    yentry.pack(anchor='w')
    Label(asktab, text=langdata['asktab6']).pack()
    dataentry = ttk.Entry(asktab)
    dataentry.pack(anchor='w')
    ttk.Button(asktab, text=langdata['asktab7'], command=lambda: create_sprite(nameentry.get(), type, dataentry.get(), xentry.get(), yentry.get())).pack()

def create_sprite(name, type, data2, xloc, yloc):
    data['sprites'][name] = {
        "name": name,
        "type": type,
        "data": data2,
        "xloc": int(xloc),
        "yloc": int(yloc),
        "position": 1}
    asktab.destroy()
    button = ttk.Button(root, text=name)
    bi[name] = button
    button.pack(anchor='w')
    button.configure(command=lambda name=name: set(name))
    save()


def set(name):
    global buttonset
    buttonset = name


def delete():
    bi[buttonset].destroy()
    del bi[buttonset]
    del data['sprites'][buttonset]
    save()

def credit():
    ct = Toplevel(root)
    ct.geometry('200x300')
    Label(ct, text='GMAKER', font=('Arial', 16)).pack()
    Label(ct, text=langdata['credittext']).pack()
    try:
        imgfile = get_resource_path(os.path.join('Graphics', 'Logo.png'))
        img = Image.open(imgfile).resize((200, 200))
        photo = ImageTk.PhotoImage(img)
        Label(ct, image=photo).pack()
        ct.image = photo
    except:
        Label(ct, text="(Logo missing)").pack()

def new_project():
    global project_path
    project_path = filedialog.askdirectory()

    if not project_path:
        return
    

    f = 'data'
    os.makedirs(os.path.join(project_path, f), exist_ok=True)
    
    
    game_template = {
        "name": "NewGame",
        "width": 1280,
        "height": 720,

        "bg": {
            "color": "white"
        },

        "sprites": 
        {
        }
    }

    with open(os.path.join(project_path, "game.json"), "w", encoding="utf-8") as f:
        json.dump(game_template, f, indent=4)
    shutil.copy(get_resource_path(os.path.join('engine', 'data', 'Font.ttf')), os.path.join(project_path, 'data', 'Font.ttf'))
    shutil.copy(get_resource_path(os.path.join('engine', 'engine.exe')), os.path.join(project_path, 'engine.exe'))
    print("complete:", project_path)
    
# this place was for paint app, but deleted cuz its useless(for now)
def button_deleter(tab):
    for widget in tab.winfo_children():
        if isinstance(widget, ttk.Button):
            widget.destroy()
            
# this is the main element of coding thing
class TextEditor:
    def __init__(self):
        self.root = Toplevel()
        self.root.title("Text Editor")
        self.root.geometry("600x500")

        cm = Menu(self.root)
        cc = Menu(cm, tearoff=0)
        cm.add_cascade(label=langdata['code2'], menu=cc)
        self.root.config(menu=cm)
        
        # widget
        self.text_area = Text(self.root, wrap='word')
        self.text_area.pack(expand=True, fill='both')

        # scrollbar
        self.scrollbar = ttk.Scrollbar(self.text_area)
        self.scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        # file menu
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="파일", menu=self.file_menu)
        # self.file_menu.add_command(label="열기", command=self.open_file)
        self.file_menu.add_command(label=langdata['save'], command=self.save_file)
        # self.file_menu.add_command(label="종료", command=self.root.quit)

    def open_file(self, file_path):
        self.text_area.delete("1.0", END)
        with open(file_path, "r", encoding="utf-8") as file:
            self.text_area.insert("1.0", file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get("1.0", END))
            self.root.title(f"텍스트 에디터 - {file_path}")

# def code():
#     global ct
#     ct = Toplevel()
#     ct.geometry('500x300')
#     cm = Menu(ct)
#     cc = Menu(cm, tearoff=0)
#     cm.add_cascade(label=langdata['code1'], menu=cc)
#     cc.add_command(label=langdata['code2'], command=logic)
#     cc.add_command(label=langdata['code3'], command=game)
#     ct.config(menu=cm)
#     global category
#     category = ttk.Label(ct, text=langdata['code2'])
#     category.pack()


# all the buttons in the diffrent categories will be deleted
# def logic():
#     button_deleter(ct)
#     category.config(text=langdata['code2'])
#     # remember to add the command for the buttons later!
#     ttk.Button(ct, text=langdata['code5'], command=ifcode).pack()

# def game():
#     button_deleter(ct)
#     category.config(text=langdata['code3'])
#     ttk.Button(ct, text=langdata['code6']).pack()

# def ifcode():
#     pass

    

def save():
    try:
        with open(gamefile, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            print(data)
    except Exception:
        messagebox.showerror('Error', str(langdata['saveerror']))


def lang_select(lang):
    global language
    language = lang
    with open(get_resource_path(os.path.join('lang', f'{language}.json')), 'r', encoding='utf-8') as f:
        global langdata
        langdata = json.load(f)




def start_main():
    global root
    root = Tk()
    root.title("GMAKER")
    # try to set a window icon; iconbitmap only works reliably on Windows
    icofile = get_resource_path(os.path.join('Graphics', 'Logo.ico'))
    if os.path.exists(icofile):
        try:
            # on Windows this will set the icon; on Linux/Tk, ICO may raise TclError
            root.iconbitmap(icofile)
        except Exception:
            # fallback: use a PNG image via iconphoto which is cross‑platform
            pngfile = get_resource_path(os.path.join('Graphics', 'Logo.png'))
            if os.path.exists(pngfile):
                try:
                    img = ImageTk.PhotoImage(file=pngfile)
                    root.iconphoto(True, img)
                    # keep a reference so Tk doesn't garbage collect it
                    root._iconimg = img
                except Exception:
                    pass
    else:
        # if the ico file isn't present or accessible, attempt the png fallback
        pngfile = get_resource_path(os.path.join('Graphics', 'Logo.png'))
        if os.path.exists(pngfile):
            try:
                img = ImageTk.PhotoImage(file=pngfile)
                root.iconphoto(True, img)
                root._iconimg = img
            except Exception:
                pass
    root.geometry('300x300')
    menubar = Menu(root)
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label=langdata['open'], command=open_game)
    editmenu.add_command(label=langdata['new'], command=new_project)
    editmenu.add_command(label=langdata['credit'], command=credit)
    editmenu.add_command(label=langdata['save'], command=save)
        # editmenu.add_command(label='Paint', command=Paint)
    # editmenu.add_command(label='Code', command=open_webview)
    # used before for devlelopment but not now
    menubar.add_cascade(label=langdata['menu'], menu=editmenu)
    root.config(menu=menubar)

    root.mainloop()
with open(get_resource_path('setting.json'), 'r', encoding='utf-8') as f:
    settingdata = json.load(f)
lang_select(settingdata['language'])
start_main()