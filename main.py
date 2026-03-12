from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import json
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
    deleter(root, ttk.Button)
    for i in data['sprites'].values():
        global button
        button = ttk.Button(root, text=i['name'])
        bi[i['name']] = button
        count += 1
        button.pack(anchor='w')
        button.configure(command=lambda name = i['name']: set(name))
    ttk.Button(root, text='+', command=add_sprite).pack(anchor='w')
    ttk.Button(root, text=langdata['delete'], command=delete).pack(anchor='w')
    ttk.Button(root, text=langdata['code'], command=TextEditor).pack(anchor='w')
    # ttk.Button(root, text=langdata['edit']).pack(anchor='w')

def add_sprite():
    global asktab
    asktab = Toplevel(root)
    asktab.geometry('200x300')
    Label(asktab, text=langdata['sprite_name']).pack()
    nameentry = Entry(asktab)
    nameentry.pack(anchor='w')
    global dataentry, type
    def txt_selected():
        global dataentry, type, data_text
        try:
            data_text.destroy()
            dataentry.destroy()
        except:
            pass
        type = 'text'
        data_text = Label(asktab, text=langdata['txtdata'])
        data_text.pack()
        dataentry = ttk.Entry(asktab)
        dataentry.pack(anchor='w')
    def img_selected():
        global dataentry, type, data_text
        try:
            data_text.destroy()
            dataentry.destroy()
        except:
            pass
        type = 'image'
        data_text = Label(asktab, text=langdata['imgdata'])
        data_text.pack()
        dataentry = ttk.Entry(asktab)
        dataentry.pack(anchor='w')
    type = 'text'
    txt = ttk.Radiobutton(asktab, text=langdata['text'], command=txt_selected, value=1)
    img = ttk.Radiobutton(asktab, text=langdata['image'], command=img_selected, value=2)
    txt.pack(anchor='w')
    img.pack(anchor='w')

    # checks if name uses only ascii
    
    ttk.Button(asktab, text=langdata['create'], command=lambda: create_sprite(nameentry.get(), type, dataentry.get())).pack()

def create_sprite(name, type, data2):
    if name.isascii() == True:
        data['sprites'][name] = {
            "name": name,
            "type": type,
            "data": data2,
            "code": f"{name} = Sprites('{type}', '{name}')"
        }
        asktab.destroy()
        button = ttk.Button(root, text=name)
        bi[name] = button
        button.pack(anchor='w')
        button.configure(command=lambda name=name: set(name))
        save()
    else:
        messagebox.showerror('Error.', langdata['ascii_error'])

def set(name):
    global button_set
    button_set = name


def delete():
    bi[button_set].destroy()
    del bi[button_set]
    del data['sprites'][button_set]
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
    shutil.copy(get_resource_path(os.path.join('engine', 'data', 'README.txt')), os.path.join(project_path, 'data', 'README.txt'))
    answer = messagebox.askquestion('Platform', langdata['platform'])
    if answer == 'yes':
        shutil.copy(get_resource_path(os.path.join('engine', 'engine.exe')), os.path.join(project_path, 'engine.exe'))
    if answer == 'no':
        shutil.copy(get_resource_path(os.path.join('engine', 'engine.sh')), os.path.join(project_path, 'engine.sh'))
    print("complete:", project_path)
def deleter(tab, widget_type):
    for widget in tab.winfo_children():
        if isinstance(widget, widget_type):
            widget.destroy()

# this is the main element of coding thing
class TextEditor:
    def __init__(self):
        self.root = Toplevel()
        self.root.title("Text Editor")
        self.root.geometry("600x500")
        # widget
        self.text_area = Text(self.root, wrap='word')
        self.text_area.pack(expand=True, fill='both')
        # scrollbar
        self.scrollbar = ttk.Scrollbar(self.text_area)
        self.scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
        try:
            self.text_area.insert("1.0", data['sprites'][button_set]['code'])
        except:
            pass


        # file menu
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.code_menu = Menu(self.menu_bar, tearoff=0)
        # movement
        self.menu_bar.add_cascade(label=langdata['code3'], menu=self.code_menu)
        # set xy
        self.code_menu.add_command(label=langdata['code6'], command=self.xy)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=langdata['file'], menu=self.file_menu)
        self.file_menu.add_command(label=langdata['save'], command=self.save_file)

    def save_file(self):
        data['sprites'][button_set]['code'] = self.text_area.get("1.0", "end-1c")
        save() 
    # xy
    def xy(self):
        xytab = Toplevel(self.root)
        ttk.Label(xytab, text=langdata['sprite_x']).pack()
        xentry = ttk.Entry(xytab)
        xentry.pack(anchor='w')
        ttk.Label(xytab, text=langdata['sprite_y']).pack()
        yentry = ttk.Entry(xytab)
        yentry.pack(anchor='w')
        ttk.Button(xytab, text=langdata['xy3'], command=lambda: self.set_xy(xentry.get(), yentry.get(), xytab)).pack()

    def set_xy(self, x, y, window):
        self.text_area.insert(INSERT, f"{button_set}.set_xy({x}, {y})\n")
        window.destroy()

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
    root.geometry('300x300')
    menubar = Menu(root)
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label=langdata['open'], command=open_game)
    editmenu.add_command(label=langdata['new'], command=new_project)
    editmenu.add_command(label=langdata['credit'], command=credit)
    editmenu.add_command(label=langdata['save'], command=save)
    menubar.add_cascade(label=langdata['menu'], menu=editmenu)
    root.config(menu=menubar)

    root.mainloop()
with open(get_resource_path('setting.json'), 'r', encoding='utf-8') as f:
    settingdata = json.load(f)
lang_select(settingdata['language'])
start_main()