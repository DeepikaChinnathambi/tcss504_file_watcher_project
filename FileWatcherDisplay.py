"""
intending this to be the main script housing the tkinter gui and controller logic
"""
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import copy

import FileWatcher
from FileWatcher import *
from FileWatcherModel import FileModel


class View():
    def __init__(self, directory=None):
        # Initialize the Tkinter root window
        self.event_display = None
        self.root = tk.Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.title("Guard Dog 🐶")
        self.root.geometry("750x500")
        self.root.resizable(False, False)

        # Directory selection
        self.directory_path = tk.StringVar()
        self.create_widgets()

        # Model and FileWatcher
        self.model = FileModel()
        self.file_watcher = None  # Will be initialized when monitoring starts


    def create_widgets(self):
        """Create and arrange Tkinter widgets."""
        # create main containters
        topFrame = tk.Frame(self.root)
        middleFrame = tk.Frame(self.root)
        bottomFrame = tk.Frame(self.root)

        # add subsections in grid format
        topFrame.grid(row=0, column=0, sticky=tk.NSEW)
        topFrame.columnconfigure(0, weight=1)
        topFrame.columnconfigure(1, weight=1)
        topFrame.columnconfigure(2, weight=1)

        middleFrame.grid(row=1, column=0,sticky=tk.NSEW)
        middleFrame.columnconfigure(0, weight=1)
        middleFrame.rowconfigure(0, weight=1)
        middleFrame.columnconfigure(1, weight=1)
        middleFrame.columnconfigure(2, weight=1)

        bottomFrame.grid(row=2, column=0,sticky=tk.NSEW)
        bottomFrame.columnconfigure(0, weight=1)
        bottomFrame.columnconfigure(1, weight=1)
        bottomFrame.columnconfigure(2, weight=1)

        self.run_status_var = tk.StringVar()
        self.run_status_var.set("Idle . . .")
        self.saved_db = tk.StringVar()
        # self.saved_db.set('No Database Saved . . .')
        run_status_label = tk.Label(topFrame, textvariable=self.run_status_var, wraplength=700).grid(row=2, column=0, sticky=tk.W,  padx=5, pady=5)
        saved_db_label = tk.Label(topFrame, textvariable=self.saved_db).grid(row=3, column=2, sticky=tk.EW,  padx=5, pady=5)
        tk.Label(topFrame, text="Select Directory:").grid(row=0, column=0, sticky=tk.NSEW,  padx=5, pady=5)
        tk.Entry(topFrame, textvariable=self.directory_path, width=50).grid(row=1, column=0, sticky=tk.NSEW,  padx=5, pady=5)
        tk.Button(topFrame, text="Browse", command=self.browse_directory, width=15).grid(row=1, column=1, padx=5, pady=5,)

        # Start monitoring button
        self.startbutton = tk.Button(topFrame, text="Start Monitoring", command=self.start_monitoring, width=15, bg='lightgreen')
        self.startbutton.grid(row=0, column=2, padx=5, pady=5)
        # Quit button
        self.quitbutton = tk.Button(topFrame, text="Stop Monitoring", command=self.stop_monitoring, width=15, bg="salmon", state=tk.DISABLED)
        self.quitbutton.grid(row=1, column=2, padx=5, pady=5)
        # Save button
        # self.savebutton = tk.Button(topFrame, text="Save", command=self.save_log, width=15, bg='dodgerblue', state=tk.ACTIVE)
        # self.savebutton.grid(row=2, column=2, padx=5, pady=5)

        # Text box to display events
        self.event_display = ttk.Treeview(middleFrame, columns=("event", "date", "time"), selectmode="browse")
        self.event_display.heading("#0", text="File")
        self.event_display.heading("event", text="Event")
        self.event_display.heading("date", text="Date")
        self.event_display.heading("time", text="Time")
        self.event_display.grid(row=0, columnspan=3,  padx=5, pady=5, sticky=tk.NSEW)

        # Constructing vertical scrollbar
        # with treeview
        verscrlbar = ttk.Scrollbar(middleFrame,
                                   orient ="vertical",
                                   command = self.event_display.yview)
        # Calling pack method w.r.to vertical
        # scrollbar
        verscrlbar.grid(row=0, column=3, sticky=tk.NS)
        self.event_display.configure(xscrollcommand=verscrlbar.set)


        # Save button
        # self.quit_savebutton = tk.Button(bottomFrame, text="Stop and Save", command=self.quit_and_save, width=15, bg='salmon')
        # self.quit_savebutton.grid(row=0, column=1, padx=25, pady=5, sticky=tk.EW)



    def browse_directory(self):
        """Open a directory dialog and set the selected directory path."""
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.directory_path.set(selected_dir)


    def start_monitoring(self):
        """Start monitoring the selected directory."""
        for row in self.event_display.get_children():
            self.event_display.delete(row)

        directory = self.directory_path.get()
        if directory:
            self.startbutton["state"] = tk.DISABLED
            self.quitbutton['state'] = tk.ACTIVE
            # self.savebutton['state'] = tk.ACTIVE
            self.run_status_var.set(f"Currently monitoring: {directory}")
            # Initialize and start the FileWatcher
            directory_name = os.path.basename(directory)
            self.model.set_table_name(directory_name)
            all_files = self.model.get_all_files()
            for file in all_files:
                print(file.file_name, file.event_type, file.date, file.time)
                self.display_event(file.file_name, file.event_type, file.date, file.time)
            self.file_watcher = FileWatcher(directory, self.model, self)
            self.file_watcher.start_watchdog_for_directory() # Start the watcher in a separate thread

        else:
            self.display_event("Please select a directory first.")


    def stop_monitoring(self):
        self.file_watcher.stop_watchdog()
        self.run_status_var.set(f"Stopped Monitoring: {self.directory_path.get()}")
        self.startbutton["state"] = tk.ACTIVE
        self.quitbutton['state'] = tk.DISABLED
        # self.savebutton["state"] = tk.ACTIVE


    def display_event(self, file_name, event_type, date, time):
        """Display a file event in the text box."""
        # print("Display event called")
        # if not isinstance(file_path, str):
        #     message = str(message)  # Convert to string if it's not already

        self.event_display.insert("", tk.END, text=file_name, values=(event_type, date, time))
        self.event_display.yview_moveto(1.0)  # Auto-scroll to the bottom


    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()


    def save_log(self):
        dbname = self.model.write_data()
        self.saved_db.set(f"DB saved:\n{dbname}")

    def quit_and_save(self):
        self.save_log()
        self.stop_monitoring()


if __name__ == "__main__":
    view = View()
    view.run()

