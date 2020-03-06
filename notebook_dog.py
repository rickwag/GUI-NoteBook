import sys
import tkinter as tk
from tkinter import scrolledtext

from NoteBK.NoteBook import Notebook

from datetime import datetime

class NotebookGui:

    def __init__(self):
        self.win = tk.Tk()
        # win.geometry("1366x768+0+0")
        self.win.resizable(False,False)
        self.win.title("NOTSY")
        self.notebook = Notebook()

        self.title = tk.StringVar()
        self.date = tk.StringVar()
        self.displaying_note = None
        self.buttons = []

        self.add_widgets()

        # self.displaying = False

    def delete_note(self):
        if self.displaying_note is not None:
            id = self.displaying_note
            self.notebook.delete_note(id)
            self.new_note()

    def new_note(self):
        self.displaying_note=None
        self.title.set("")
        self.date.set(datetime.today().date())
        self.scroll.delete("1.0",tk.END)

    def add_note(self):
        # memo = input("Enter a memo: ")
        # tag = input("Enter a tag: ")
        note_id = self.displaying_note
        memo = self.scroll.get("1.0", "end-1c")
        if self.displaying_note is not None:
            self.modify_memo(note_id,memo)
        else:
            if memo is not "":
                tag = self.title.get()
                if tag is "":
                    self.title.set("No title")
                else:
                    self.notebook.new_note(memo,tag)
                    self.displaying_note = self.notebook.notes[-1].id

    def modify_memo(self, note_id, memo):
        '''find the note with the given id and
        modify its memo'''
        note = self.notebook._find_note(note_id)
        if note:
            note.memo = memo
            return True
        return False

    def update_file(self):
        with open("notebook", "w") as file:
            for value in self.notebook.notes:
                file.write(value.tag + "|" + value.memo + "|" + value.creation_date + "\n")

        sys.exit(0)

    def display_notes(self,event):
        for note in self.notebook.notes:
            note_id = int(event.widget.cget("text").strip()[0])

            if note.id == note_id: #and not self.displaying:
                self.scroll.delete(1.0,tk.END)
                self.scroll.insert(1.0,note.memo)
                self.title.set(note.tag)
                self.date.set(note.creation_date)
                # self.displaying = True
                self.displaying_note = note.id

    def show_notes(self,notes = None):
        if notes is None:
            notes = self.notebook.notes

        column = 1
        row = 0
        if len(self.buttons) == 0:
            for note in notes:
                #create buttons

                note_button = tk.Button(self.notes_frame,
                                        text=str(note.id)+" "+note.tag,
                                        relief=tk.RIDGE,
                                        bg="goldenrod",
                                        font=("ariel","10","italic"))

                note_button.grid(row=row,column=column,padx=5)
                note_button.bind("<Button-1>",self.display_notes)

                self.buttons.append(note_button)

                if column > 12:
                    column = 1
                    row += 1
                else:
                    column+=1
        else:
            for button in self.buttons:
                button.grid_remove()
                button.destroy()
            self.buttons.clear()

    def add_widgets(self):
        self.date.set(datetime.today().date())

        self.writting_frame = tk.LabelFrame(self.win,
                                        text="A BIT NOTSY",
                                        bg="powder blue",
                                        font=("ariel","50","bold"))
        self.writting_frame.grid(row=0,column=0,padx=5,pady=5)

        self.date_label = tk.Label(self.writting_frame,
                              text="Date",
                              font=("ariel", "30", "bold"),
                                bg="orchid")
        self.date_entry = tk.Entry(self.writting_frame,
                              font=("ariel", "30", "italic",),
                              width=20,
                                textvariable=self.date)

        self.title_label = tk.Label(self.writting_frame,
                                text="Title",
                                bg="teal",
                                fg="lime",
                                font=("ariel","30","bold"))

        self.title_entry = tk.Entry(self.writting_frame,
                               width=20,
                               font=("ariel","30","italic"),
                                    textvariable=self.title)
        self.title_entry.focus()
        self.scroll = scrolledtext.ScrolledText(self.writting_frame,
                                           width=60,
                                           height=5,
                                           wrap=tk.WORD,
                                           bg="lightyellow",
                                           font=("ariel","20"))
        count = 0
        for child in self.writting_frame.winfo_children():
            child.grid(row=count,column=0,sticky=tk.W,padx=5,pady=5)
            count+=1



        self.notes_frame = tk.LabelFrame(self.win,
                                    text="Records",
                                    font=("ariel","30","bold"),
                                    bg="cadetblue")
        self.notes_frame.grid(row=1,column=0,sticky=tk.W)

        self.notes_Button = tk.Button(self.notes_frame,
                               text="notes",
                               font=("ariel","15","italic"),
                               bg="goldenrod",
                                command=self.show_notes)

        for child in self.notes_frame.winfo_children():
            child.grid(row=0,column=0,padx=5,pady=5,sticky=tk.W)


        self.buttons_frame = tk.LabelFrame(self.win,
                                      bg="skyblue")
        self.buttons_frame.grid(row=0,column=1,sticky=tk.N)

        self.new_button = tk.Button(self.buttons_frame,
                               text="New",
                               bg="powderblue",
                               relief=tk.RAISED,
                               font=("ariel","30","bold"),
                               width=6,bd=6,
                                command=self.new_note)
        self.delete_button = tk.Button(self.buttons_frame,
                                  text="Delete",
                                  bg="powderblue",
                                  relief=tk.RAISED,
                                  font=("ariel","30","bold"),
                                  width=6,bd=6,
                                   command=self.delete_note)
        self.save_button = tk.Button(self.buttons_frame,
                                text="Save",
                                bg="powderblue",
                                relief=tk.RAISED,
                                font=("ariel","30","bold"),
                                width=6,bd=6,
                                command=self.add_note)
        count = 0
        for child in self.buttons_frame.winfo_children():
            child.grid(row=count,column=0,padx=5,pady=5,sticky=tk.W)
            count+=1

noteGui = NotebookGui()
noteGui.win.protocol("WM_DELETE_WINDOW",noteGui.update_file)
noteGui.win.mainloop()