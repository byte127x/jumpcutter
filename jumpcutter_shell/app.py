from tkinter import *
from tkinter import ttk, filedialog
from datetime import datetime
import ttkbootstrap as ttk
import os, subprocess, threading, time

root = Tk()
root.geometry('450x350')
root.title('Jumpcutter Shell')

# Functions and Classes
class LabeledWidget(ttk.Frame):
	def __init__(self, parent, text, widget, widget_args=(), widget_kwargs={},*args, **kwargs):
		super().__init__(parent, *args, **kwargs)

		ttk.Label(self, text=text).pack(side=LEFT, padx=2)
		widget(self, *widget_args, **widget_kwargs).pack(side=RIGHT, padx=2)

class SpinboxAndButton(ttk.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.spin = ttk.Spinbox(self, from_=0, to=999999, increment=.05, width=10)
		self.spin.pack(side=TOP)

		btm_frame = ttk.Frame(self)
		btm_frame.pack(side=BOTTOM)

		ttk.Button(btm_frame, text='Min', width=4, command=self.min).pack(side=LEFT)
		ttk.Button(btm_frame, text='Max', width=4, command=self.max).pack(side=RIGHT)

	def max(self):
		self.spin.set(f'{self.spin["to"]}.00')

	def min(self):
		self.spin.set(f'{self.spin["from"]}.00')

	def get(self):
		return self.spin.get()

def now():
	return datetime.today().strftime("%m/%d/%Y  %I:%M:%S %p")

def workhorse(*args):
	orig_time = time.time()
	add_to_text(f'Starting \'jumpcutter.exe\' at {now()}\n')
	s = subprocess.run(['jumpcutter.exe', '-h'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	add_to_text(s.stdout)
	time_diff = time.time()-orig_time
	add_to_text(f'\nProcess Completed in {time_diff} seconds!')
	run_btn['state'] = 'enabled'

def add_to_text(stuff):
	text_data.insert(END, stuff)

def on_log_closing():
	log.withdraw()

def run():
	run_btn['state'] = DISABLED
	log.deiconify()

	threading.Thread(target=workhorse, args=(None,)).start()

def edit():
	f = filedialog.asksaveasfilename(defaultextension='.mp4', filetypes=(('MPEG-4 Video', '*.mp4 *.m4v *.mov'), ('Maktrosa Video', '*.mkv'), ('Flash Video', '*.flv *.f4v *.swf'), ('WEBM Video', '*.webm'), ('Audio-Video Interleave', '*.avi'), ('Windows Media Audio/Video', '*.wmv')))
	if f == '':
		return

	idx = out_lb.index(ANCHOR)
	out_lb.delete(idx)
	out_lb.insert(idx, f)

def add_file():
	f = filedialog.askopenfilenames(filetypes=(('MPEG-4 Video', '*.mp4 *.m4v *.mov'), ('Maktrosa Video', '*.mkv'), ('Flash Video', '*.flv *.f4v *.swf'), ('WEBM Video', '*.webm'), ('Audio-Video Interleave', '*.avi'), ('Windows Media Audio/Video', '*.wmv')))
	if f == '':
		return

	for x in f:
		add_lb.insert(END, x)
		out_lb.insert(END, os.getcwd().replace('\\', '/')+'/NEW - '+x.split('/')[-1])

def remv_file():
	out_lb.delete(add_lb.index(ANCHOR))
	add_lb.delete(ANCHOR)

def box_yviews(*args):
	add_lb.yview(*args)
	out_lb.yview(*args)

# Log Setup
log = Toplevel(root)
log.withdraw()
log.title('Log')
log.protocol("WM_DELETE_WINDOW", on_log_closing)

text_data = Text(log)
text_data.insert(END, f'Log Started: {now()}\n\n')
text_data.pack(fill='both', expand=1)

# Baseline GUI
ttk.Label(root, text='Jumpcutter GUI').pack(pady=(5, 10))
bottom_frame = ttk.Frame(root)
bottom_frame.pack(fill='both', expand=1)

bottom_left = Frame(bottom_frame)
bottom_right = Frame(bottom_frame)
bottom_left.pack(side=LEFT, expand=1, fill='both')
bottom_right.pack(side=RIGHT, expand=1, fill='both')

# Bottom Left
bottom_left_top = ttk.Frame(bottom_left)
bottom_left_top.pack(fill=X, padx=4)
ttk.Label(bottom_left_top, text='Add').pack(pady=2, side=LEFT)
ttk.Button(bottom_left_top, text='-', command=remv_file, width=3).pack(pady=2, side=RIGHT)
ttk.Button(bottom_left_top, text='+', command=add_file, width=3).pack(pady=2, side=RIGHT)

add_lb = Listbox(bottom_left)
add_lb.pack(fill='both', expand=1)

# Bottom Right
bottom_right_top = ttk.Frame(bottom_right)
bottom_right_top.pack(fill=X, padx=4)
ttk.Label(bottom_right_top, text='Output Files').pack(pady=2, side=LEFT)
ttk.Button(bottom_right_top, text='Edit', width=5, command=edit).pack(pady=2, side=RIGHT)

out_lb = Listbox(bottom_right)
out_lb.pack(fill='both', expand=1, side=LEFT)
scr = ttk.Scrollbar(bottom_right, command=box_yviews, orient=VERTICAL)
scr.pack(side=RIGHT, fill=Y)

out_lb['yscrollcommand'] = scr.set
add_lb['yscrollcommand'] = scr.set

# Configuration Options
config_frame = ttk.Frame(root)
config_frame.pack(pady=5)

LabeledWidget(config_frame, text='Silent Speed: ', widget=SpinboxAndButton).pack(pady=5)

run_btn = ttk.Button(config_frame, text='Run', command=run)
run_btn.pack()

# Mainloop and Event Bindings
root.mainloop()