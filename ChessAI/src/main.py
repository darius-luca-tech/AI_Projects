import tkinter as tk
import manager

def main():
    master = tk.Tk()
    master.title("Chess")
    master.geometry("+20+20")
    master.configure(bg="#FFFFFF")
    
    manager.Manager( master )
    master.mainloop()
    
    
if(__name__ == "__main__"):
    main()