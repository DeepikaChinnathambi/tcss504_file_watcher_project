"""
intending this to be the main script housing the tkinter gui and controller logic
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext
import copy

from FileWatcher import *
from FileWatcherModel import FileModel


class View():
    def __init__(self, directory=None):
        # Initialize the Tkinter root window
        self.event_display = None
        self.root = tk.Tk()
        self.root.title("File Watcher")
        self.root.geometry("600x400")

        # Directory selection
        self.directory_path = tk.StringVar()
        self.create_widgets()

        # Model and FileWatcher
        self.model = FileModel()
        self.file_watcher = None  # Will be initialized when monitoring starts

    def create_widgets(self):
        """Create and arrange Tkinter widgets."""
        # Directory selection frame
        dir_frame = tk.Frame(self.root)
        dir_frame.pack(pady=10)

        tk.Label(dir_frame, text="Select Directory:").pack(side=tk.LEFT, padx=5)
        tk.Entry(dir_frame, textvariable=self.directory_path, width=40).pack(side=tk.LEFT, padx=5)
        tk.Button(dir_frame, text="Browse", command=self.browse_directory).pack(side=tk.LEFT, padx=5)

        # Start monitoring button
        tk.Button(self.root, text="Start Monitoring", command=self.start_monitoring).pack(pady=10)

        # Text box to display events
        self.event_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=20)
        self.event_display.pack(padx=10, pady=10)

        # Quit button
        tk.Button(self.root, text="Quit", command=self.root.quit).pack(pady=10)

    def browse_directory(self):
        """Open a directory dialog and set the selected directory path."""
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.directory_path.set(selected_dir)

    def start_monitoring(self):
        """Start monitoring the selected directory."""
        directory = self.directory_path.get()
        if directory:
            self.display_event(f"Started monitoring: {directory}")
            # Initialize and start the FileWatcher
            self.file_watcher = FileWatcher(directory, self.model, self)
            self.file_watcher.start_watchdog_for_directory() # Start the watcher in a separate thread
        else:
            self.display_event("Please select a directory first.")

    def display_event(self, message):
        """Display a file event in the text box."""
        print("Display event called")
        if not isinstance(message, str):
            message = str(message)  # Convert to string if it's not already
        self.event_display.insert(tk.END, message + "\n")
        self.event_display.yview(tk.END)  # Auto-scroll to the bottom

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()

    # def configure_run(self):
    #     self.root = tk.Tk()
    #     self.root.geometry("600x750")
    #     self.root.title("Configure Dog Watcher")
    #     topFrame = tk.Frame(self.root)
    #     topLeftFrame = tk.Frame(topFrame)
    #     topRightFrame = tk.Frame(topFrame)
    #     bottomFrame = tk.Frame(self.root)
    #     bottomLeftFrame = tk.Frame(bottomFrame)
    #     bottomRightFrame = tk.Frame(bottomFrame)
    #
    #     # create subsection labels and make the text wrap
    #     titleTop = tk.Label(self.root,
    #                         text="Add directory to watch")
    #     titleTop.bind('<Configure>', lambda e: titleTop.config(wraplength=titleTop.winfo_width()))
    #     titleBottom = tk.Label(self.root,
    #                            text="Event History")
    #     titleBottom.bind('<Configure>', lambda e: titleBottom.config(wraplength=titleBottom.winfo_width()))
    #
    #     # add the subsection labels and frames to the GUI
    #     titleTop.pack()
    #     topFrame.pack()
    #     titleBottom.pack()
    #     bottomFrame.pack()
    #     topLeftFrame.pack(side=tk.LEFT)
    #     topRightFrame.pack(side=tk.RIGHT)
    #     bottomLeftFrame.pack(side=tk.LEFT)
    #     bottomRightFrame.pack(side=tk.RIGHT)

        # # define callback functions for button and list events
        # def onDisplayListSelect(event):
        #     selection = event.widget.curselection()
        #     if selection:
        #         index = selection[0]
        #         data = event.widget.selection_get().split('\n')
        #         displayBox.configure(text=data)
        #     else:  # if nothing is selected, clear the box
        #         displayBox.configure(text="")
        #
        # def onAddButtonClick():
        #     addVal = displayBox.selection_get().split('\n')
        #     if addVal != "":
        #         for a in addVal:
        #             addedList.insert(addedList.size(), a)  # add selected engine to end of addedList
        #
        # def onAddButtonClickManual():
        #     addVal = displayBox_manual.get("1.0", tk.END)
        #     if addVal != "":
        #         addVal = addVal
        #         addedList.insert(addedList.size(), addVal)
        #
        # def onRemoveButtonClick():
        #     selectedItem = addedList.curselection()
        #     if selectedItem:
        #         addedList.delete(selectedItem[0])
        #
        # def onUseButtonClick(rList):
        #     # get all selected_engines in addList and add them to rList
        #     rList['vals'] = []
        #     vals = addedList.get(0, tk.END)
        #     for val in vals:
        #         rList['vals'].append(val)
        #     self.root.destroy()  # close GUI
        #
        # # create list to display engine and a scrollbar
        # displayList = tk.Listbox(bottomLeftFrame, height=25, selectmode='multiple')
        # displayList.bind("<<ListboxSelect>>", onDisplayListSelect)
        # scrollbar = tk.Scrollbar(bottomLeftFrame)
        #
        # # create list for added engine and a scrollbar
        # addedList = tk.Listbox(bottomRightFrame, height=25, selectmode='multiple')
        # scrollbar2 = tk.Scrollbar(bottomRightFrame)
        #
        # # add list and scrollbar to frame division on the correct sides
        # displayList.pack(side=tk.LEFT)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        # # attach the scrollbar to the side of the list
        # displayList.config(yscrollcommand=scrollbar.set)
        # scrollbar.config(command=displayList.yview)
        #
        #
        # # create a box to display the currently selected engine size and a button to finish selecting it
        # displayBox = tk.Label(topLeftFrame, height=1, width=20, borderwidth=1, relief="solid", bg="white")
        # addButton = tk.Button(topLeftFrame, height=1, width=15, text="Add engine(s)", command=onAddButtonClick)
        #
        # # create box and display to manually enter selected_engines
        # displayBox_manual = tk.Label(topLeftFrame, height=1, width=20, borderwidth=1, relief="solid", bg="white")
        # addButton_manual = tk.Button(topLeftFrame, height=1, width=20, text="Add non-listed engine",
        #                              command=onAddButtonClickManual)
        #
        # # add elements for custom enteres engine list
        # displayBox_manual.pack(side=tk.TOP, padx=10, pady=10)
        # addButton_manual.pack(side=tk.TOP, padx=10, pady=10)
        #
        # # add elements to the display from engine list
        # displayBox.pack(side=tk.TOP, padx=10, pady=10)
        # addButton.pack(side=tk.TOP, padx=10, pady=10)
        #
        #
        # # add list and scrollbar to frame division on the correct sides
        # addedList.pack(side=tk.LEFT, pady=5)
        # scrollbar2.pack(side=tk.RIGHT, fill=tk.BOTH, pady=5)
        # addedList.config(yscrollcommand=scrollbar2.set)
        # scrollbar2.config(command=addedList.yview)
        #
        # # dictionary to contain the list of selected selected_engines. Is a dictionary so that when it is passed to onUseButtonClick, it can be edited by the
        # # function (tkinter doesn't support returning values from a callback function for some reason so I had to get creative)
        # dir_events = {'vals': []}
        #
        # # define buttons to remove selected_engines from the added list, and to export the selected selected_engines and close the GUI
        # useButton = tk.Button(topRightFrame, height=1, width=15, text="Run",
        #                       command=lambda: onUseButtonClick(dir_events))
        # removeButton = tk.Button(topRightFrame, height=1, width=15, text="Remove engine", command=onRemoveButtonClick)
        # removeButton.pack(side=tk.TOP, padx=10, pady=10)
        # useButton.pack(side=tk.BOTTOM, padx=10, pady=10)
        #
        # self.root.attributes('-topmost', True)
        # self.root.after(50, lambda: self.root.focus_force())
        # self.root.after(60, lambda: self.root.after_idle(self.root.attributes, '-topmost', False))
        #
        # # run the GUI
        # self.root.mainloop()
        #
        #
        # selected_engines = dict((k, v) for k, v in self.masterDict.items() if k in dir_events['vals'])
        #
        # return selected_engines



if __name__ == "__main__":
    view = View()
    view.run()

