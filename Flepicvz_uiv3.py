import tkinter as tk
from tkinter import ttk
import os, time, random
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Flepicvz-UI")
root.attributes("-fullscreen", True)

style = ttk.Style(root)
style.theme_use("clam")

style.configure("TFrame", background="black")
style.configure("TLabel", background="black", foreground="#00FF00", font=("Courier", 12))
style.configure("TButton", background="black", foreground="#00FF00", font=("Courier", 10))

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Flepicvz-ui")
logo_path = os.path.join(desktop_path, "logo.png")
folder_icon_path = os.path.join(desktop_path, "Folder.png")

current_path = desktop_path

back_stack = []
forward_stack = []

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

text_id = canvas.create_text(
    20,
    screen_h + 300,
    text="",
    fill="#00FF00",
    font=("Courier", 16),
    justify="left",
    anchor="nw"
)

messages = [
    "POWER ON SEQUENCE INITIATED...",
    "CHECKING HARDWARE LAYERS...",
    "CPU: ONLINE",
    "MEMORY: OK",
    "STORAGE: DETECTED",
    "SCANNING BOOT VOLUMES...",
    "VALIDATING SYSTEM SIGNATURE...",
    "LOADING KERNEL CORE...",
    "MOUNTING ROOT FILESYSTEM...",
    "LOADING SECURITY MODULES...",
    "ENCRYPTION: ACTIVE",
    "INITIALIZING GRAPHICS PIPELINE...",
    "CALIBRATING DISPLAY MATRIX...",
    "ALIGNING PIXEL GRID...",
    "LOADING DISPLAY DRIVERS...",
    "STARTING NETWORK STACK...",
    "NETWORK: CONNECTED",
    "LOADING FLEPICVZ ASSETS...",
    "INITIALIZING TERMINAL EMULATOR...",
    "SYNCING USER ENVIRONMENT...",
    "MAPPING FILESYSTEM...",
    "BUILDING UI LAYERS...",
    "HANDING CONTROL TO FLEPICVZ-UI...",
    "SYSTEM BOOT COMPLETE."
]

current_text = ""

def add_message(i=0):
    global current_text
    if i < len(messages):
        current_text += ">> " + messages[i] + "\n"
        canvas.itemconfig(text_id, text=current_text)
        canvas.move(text_id, 0, -30)
        root.after(260, add_message, i + 1)
    else:
        root.after(900, show_logo)

def show_logo():
    canvas.delete("all")
    if not os.path.exists(logo_path):
        canvas.create_text(
            screen_w//2,
            screen_h//2,
            text="LOGO NOT FOUND",
            fill="red",
            font=("Courier", 20)
        )
    else:
        img = Image.open(logo_path)
        w, h = img.size
        scale = min(520/w, 520/h)
        img = img.resize((int(w*scale), int(h*scale)))
        logo = ImageTk.PhotoImage(img)
        canvas.image = logo
        canvas.create_image(screen_w//2, screen_h//2 - 80, image=logo)

    canvas.create_text(
        screen_w//2,
        screen_h//2 + 200,
        text="FLEPICVZ-UI ONLINE",
        fill="#00FF00",
        font=("Courier", 22)
    )
    root.after(1200, build_ui)

def build_ui():
    global current_path
    canvas.destroy()
    main = ttk.Frame(root)
    main.pack(fill="both", expand=True)

    topbar = ttk.Frame(main)
    topbar.place(x=0, y=-120, width=screen_w, height=90)

    clock_label = ttk.Label(topbar, font=("Courier", 22))
    clock_label.place(x=30, y=25)

    net_label = ttk.Label(topbar, font=("Courier", 12))
    net_label.place(x=screen_w-340, y=30)

    terminal_frame = ttk.Frame(main)
    terminal_frame.place(x=50, y=screen_h, width=screen_w-100, height=screen_h-450)

    terminal = tk.Text(
        terminal_frame,
        bg="black",
        fg="#00FF00",
        insertbackground="#00FF00",
        font=("Courier", 14)
    )
    terminal.pack(fill="both", expand=True)
    terminal.insert("end", "FLEPICVZ-UI TERMINAL\nType here...\n\n> ")

    bottom = ttk.Frame(main)
    bottom.place(x=0, y=screen_h+260, width=screen_w, height=260)

    folder_frame = ttk.Frame(bottom)
    folder_frame.place(x=-600, y=20, width=580, height=220)

    header = ttk.Frame(folder_frame)
    header.pack(fill="x")

    back_btn = ttk.Button(header, text="◀ Back")
    back_btn.pack(side="left", padx=5)

    forward_btn = ttk.Button(header, text="Forward ▶")
    forward_btn.pack(side="left", padx=5)

    path_label = ttk.Label(header, text=current_path, font=("Courier", 10))
    path_label.pack(side="left", padx=10)

    sc_canvas = tk.Canvas(folder_frame, bg="#001a00", highlightthickness=0)
    scrollbar = ttk.Scrollbar(folder_frame, orient="vertical", command=sc_canvas.yview)
    sc_canvas.configure(yscrollcommand=scrollbar.set)
    sc_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scroll_frame = ttk.Frame(sc_canvas)
    sc_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def configure_scroll(event):
        sc_canvas.configure(scrollregion=sc_canvas.bbox("all"))
    scroll_frame.bind("<Configure>", configure_scroll)

    def on_mouse_wheel(event):
        sc_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    sc_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    if os.path.exists(folder_icon_path):
        raw_icon = Image.open(folder_icon_path).resize((64, 64))
        folder_icon = ImageTk.PhotoImage(raw_icon)
    else:
        folder_icon = None

    def open_item(path):
        global current_path, back_stack, forward_stack
        if os.path.isdir(path):
            back_stack.append(current_path)
            forward_stack.clear()
            current_path = path
            refresh_files()
        else:
            os.startfile(path)

    def go_back():
        global current_path
        if back_stack:
            forward_stack.append(current_path)
            current_path = back_stack.pop()
            refresh_files()

    def go_forward():
        global current_path
        if forward_stack:
            back_stack.append(current_path)
            current_path = forward_stack.pop()
            refresh_files()

    back_btn.config(command=go_back)
    forward_btn.config(command=go_forward)

    def refresh_files():
        for w in scroll_frame.winfo_children():
            w.destroy()
        path_label.config(text=current_path)
        try:
            files = os.listdir(current_path)
        except:
            files = []
        
        cols = 4
        r, c = 0, 0
        for name in files:
            full_path = os.path.join(current_path, name)
            item = ttk.Frame(scroll_frame)
            item.grid(row=r, column=c, padx=12, pady=12)
            if folder_icon:
                lbl = ttk.Label(item, image=folder_icon)
                lbl.image = folder_icon
                lbl.pack()
            name_lbl = ttk.Label(item, text=name, wraplength=90, justify="center")
            name_lbl.pack()
            item.bind("<Double-Button-1>", lambda e, p=full_path: open_item(p))
            name_lbl.bind("<Double-Button-1>", lambda e, p=full_path: open_item(p))
            c += 1
            if c >= cols:
                c = 0
                r += 1

    refresh_files()

    kb_canvas = tk.Canvas(bottom, width=420, height=200, bg="black", highlightthickness=0)
    kb_canvas.place(x=screen_w+450, y=60)
    kb_canvas.create_rectangle(5, 5, 415, 195, outline="#00FF00", width=2)

    key_size = 35
    gap = 8
    key_positions = {}
    start_x, start_y = 30, 40
    rows = [list("QWERTYUIOP"), list("ASDFGHJKL"), list("ZXCVBNM")]

    for r, row in enumerate(rows):
        x = start_x + r*20
        y = start_y + r*(key_size + gap)
        for k in row:
            key_positions[k.lower()] = (x, y)
            kb_canvas.create_rectangle(x, y, x + key_size, y + key_size, outline="#00FF00", width=1)
            kb_canvas.create_text(x + key_size/2, y + key_size/2, text=k, fill="#00FF00", font=("Courier", 10))
            x += key_size + gap

    key_positions["space"] = (90, 150)
    kb_canvas.create_rectangle(90, 150, 330, 180, outline="#00FF00", width=1)
    kb_canvas.create_text(210, 165, text="SPACE", fill="#00FF00", font=("Courier", 10))

    def flash_key(x, y, w=35, h=35):
        glow = kb_canvas.create_rectangle(x, y, x+w, y+h, outline="#00FF00", width=3)
        root.after(120, lambda: kb_canvas.delete(glow))

    def on_key_press(event):
        key = event.keysym.lower()
        if key in key_positions:
            x, y = key_positions[key]
            flash_key(x, y)
    root.bind("<KeyPress>", on_key_press)

    def animate_topbar(y=-120):
        if y < 0:
            topbar.place(y=y)
            root.after(12, animate_topbar, y+4)
        else:
            topbar.place(y=0)

    def animate_terminal(y=screen_h):
        if y > 90:
            terminal_frame.place(y=y)
            root.after(10, animate_terminal, y-10)

    def animate_bottom(y=screen_h+260):
        target = screen_h-260
        if y > target:
            bottom.place(y=y)
            root.after(10, animate_bottom, y-10)

    def animate_files(x=-600):
        if x < 20:
            folder_frame.place(x=x)
            root.after(12, animate_files, x+18)
        else:
            folder_frame.place(x=20)

    def animate_keyboard(x=screen_w+450):
        if x > screen_w-420:
            kb_canvas.place(x=x)
            root.after(12, animate_keyboard, x-18)

    animate_topbar()
    animate_terminal()
    animate_bottom()
    animate_files()
    animate_keyboard()

    def update_clock():
        clock_label.config(text=time.strftime("%H:%M:%S"))
        root.after(1000, update_clock)

    def update_network():
        strength = random.choice(["INTERNET: EXCELLENT", "INTERNET: GOOD", "INTERNET: STABLE", "INTERNET: SLIGHT LATENCY"])
        net_label.config(text=strength)
        root.after(2000, update_network)

    root.after(500, update_clock)
    root.after(700, update_network)

add_message()
root.mainloop()