import tkinter as tk
import const

class PromotionDialog:
	def __init__(self):
		self.master = tk.Toplevel()
		self.master.title("Promotion")
		self.master.resizable(False, False)
		
		label = tk.Label(self.master, text="Promoting to: ")
		label.grid( row= 0, column= 0 )
		
		OPTIONS = const.FIGURE_NAME[2:6]
		
		self.optionVar = tk.StringVar(self.master)
		self.optionVar.set(OPTIONS[-1])
		
		optionMenu = tk.OptionMenu( self.master, self.optionVar, *OPTIONS )
		optionMenu.grid(row= 0, column= 1)
		
		but = tk.Button( self.master, text= "Ok", command= self.callback )
		but.grid( row= 1, columnspan=2, sticky=tk.W+tk.E )
		
		self.result = 5
		
		self.master.grab_set()
		
		self.master.focus()
		self.master.wait_window(self.master)
		
		
	def callback(self):
		val = self.optionVar.get()
		
		for i, name in enumerate(const.FIGURE_NAME):
			if(name==val):
				self.result= i-2
		
		self.master.destroy()
		