"""
intending this to be the main script housing the tkinter gui and controller logic
"""
import os
import tkinter as tk
from email.policy import default
from tkinter import filedialog, scrolledtext, ttk,Menu,messagebox
import copy
import csv

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
        # self.root.resizable(False, False)

        # Directory selection
        self.directory_path = tk.StringVar()
        self.create_widgets()

        # Model and FileWatcher
        self.model = FileModel()
        self.file_watcher = None  # Will be initialized when monitoring starts


    def create_widgets(self):
            """Create and arrange Tkinter widgets."""

            # Create menu bar
            menu_bar = Menu(self.root)
            self.root.config(menu=menu_bar)

            # File Menu
            file_menu = Menu(menu_bar, tearoff=0)
            file_menu.add_command(label="Query Database", command=self.query_database, accelerator="Ctrl+Q")
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+X")
            menu_bar.add_cascade(label="File", menu=file_menu, accelerator="Ctrl+F")

            # Edit Menu
            edit_menu = Menu(menu_bar, tearoff=0)
            edit_menu.add_command(label="Preferences")
            menu_bar.add_cascade(label="Edit", menu=edit_menu)

            # Help Menu
            help_menu = Menu(menu_bar, tearoff=0)
            help_menu.add_command(label="About",command=self.show_about, accelerator="Ctrl+A")
            menu_bar.add_cascade(label="Help", menu=help_menu)

            # Bind Keyboard Shortcuts
            self.root.bind("<Control-q>", lambda event: self.query_database())
            self.root.bind("<Control-x>", lambda event: self.root.quit())
            self.root.bind("<Control-a>", lambda event: self.show_about())

            # create main containers
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
            # bottomFrame.columnconfigure(2, weight=1)

            self.run_status_var = tk.StringVar()
            self.run_status_var.set("Idle . . .")
            self.saved_db = tk.StringVar()
            # self.saved_db.set('No Database Saved . . .')
            run_status_label = tk.Label(topFrame, textvariable=self.run_status_var, wraplength=700).grid(row=3, column=0, sticky=tk.W,  padx=5, pady=5)
            saved_db_label = tk.Label(topFrame, textvariable=self.saved_db).grid(row=3, column=2, sticky=tk.EW,  padx=5, pady=5)

           # tk.Label(topFrame, text="Select a File Extension, a directory and click start monitoring button to watch :").grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
            # Label spanning across two columns
            header_label = tk.Label(topFrame, text="Select a File Extension, a directory and click start monitoring button to watch.", font=("Arial", 9, "bold"))
            header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)  # Spans across 2 columns


            tk.Label(topFrame, text="Monitor By Extension :").grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)
            tk.Label(topFrame, text="Select Directory:").grid(row=1, column=1, sticky=tk.NSEW,  padx=5, pady=5)

            options = ["All", ".txt", ".docx", ".bmp"]
            combobox = ttk.Combobox(topFrame, values=options, width=10)
            combobox.grid(row=2, column=0, sticky=tk.NSEW,  padx=5, pady=5)
            combobox.set("ALL")

            tk.Entry(topFrame, textvariable=self.directory_path, width=10).grid(row=2, column=1, sticky=tk.NSEW,  padx=5, pady=5)
            tk.Button(topFrame, text="Browse", command=self.browse_directory, width=15).grid(row=2, column=2, padx=5, pady=5,)

            # Start monitoring button
            self.startbutton = tk.Button(topFrame, text="Start Monitoring", command=self.start_monitoring, width=15, bg='lightgreen')
            self.startbutton.grid(row=0, column=3, padx=5, pady=5)
            # Quit button
            self.quitbutton = tk.Button(topFrame, text="Stop Monitoring", command=self.stop_monitoring, width=15, bg="salmon", state=tk.DISABLED)
            self.quitbutton.grid(row=1, column=3, padx=5, pady=5)
            # Save button
            self.savebutton = tk.Button(topFrame, text="Save", command=self.save_log, width=15, bg='dodgerblue', state=tk.ACTIVE)
            self.savebutton.grid(row=2, column=3, padx=5, pady=5)

            # Text box to display events
            self.event_display = ttk.Treeview(middleFrame, columns=("ext","event", "date", "time"), selectmode="browse")
            self.event_display.heading("#0", text="File")
            self.event_display.heading("ext", text="Extension")
            self.event_display.heading("event", text="Event")
            self.event_display.heading("date", text="Date")
            self.event_display.heading("time", text="Time")
            self.event_display.grid(row=0, columnspan=5,  padx=5, pady=5, sticky=tk.NSEW)

            # Adjust column widths
            self.event_display.column("#0", width=150, minwidth=100, stretch=True)  # File column
            self.event_display.column("ext", width=80, minwidth=50, stretch=True)  # Extension column
            self.event_display.column("event", width=120, minwidth=100, stretch=True)  # Event column
            self.event_display.column("date", width=100, minwidth=80, stretch=True)  # Date column
            self.event_display.column("time", width=100, minwidth=80, stretch=True)  # Time column

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
            self.quit_savebutton = tk.Button(bottomFrame, text="Stop and Save", command=self.quit_and_save, width=15, bg='dodgerblue')
            self.quit_savebutton.grid(row=0, column=0, padx=25, pady=5, sticky=tk.EW)

            # Save button
            self.alert_button = tk.Button(bottomFrame, text="Alert Security Team", command=self.alert_security, width=15, bg='salmon')
            self.alert_button.grid(row=0, column=1, padx=25, pady=5, sticky=tk.EW)

    def show_about(self): # TODO:
        messagebox.showinfo("About", "Developer: Your Name\nVersion: 1.0\nDescription: This is a sample application.")

    def query_database(self):
        """Function to query database and display results in a table."""
        query_window = tk.Toplevel(self.root)
        query_window.title("Database Query")
        query_window.geometry("700x300")

        # Create a Frame to hold the button and table
        top_frame = tk.Frame(query_window)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        # Function to export data to CSV
        def export_to_csv():
            filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                    filetypes=[("CSV files", "*.csv")],
                                                    title="Save file as")
            if filename:
                try:
                    with open(filename, "w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(["File", "Extension", "Event", "Date", "Time"])  # Column headers
                        writer.writerows(file_data)
                    messagebox.showinfo("Success", "Data successfully exported to CSV!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {e}")

        # Add Export to CSV Button at the top
        export_button = tk.Button(top_frame, text="Export to CSV", command=export_to_csv)
        export_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Treeview Widget inside a Frame
        tree_frame = tk.Frame(query_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tree = ttk.Treeview(tree_frame, columns=("File", "Ext", "Event", "Date", "Time"), show='headings')
        tree.heading("File", text="File")
        tree.heading("Ext", text="Extension")
        tree.heading("Event", text="Event")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.pack(fill=tk.BOTH, expand=True)




        tree.column("File", width=150, minwidth=100, stretch=True)  # File column
        tree.column("Ext", width=80, minwidth=50, stretch=True)  # Extension column
        tree.column("Event", width=120, minwidth=100, stretch=True)  # Event column
        tree.column("Date", width=100, minwidth=80, stretch=True)  # Date column
        tree.column("Time", width=100, minwidth=80, stretch=True)  # Time column

        files = self.model.get_all_files()
        print(files)
        # Convert FileClass instances to tuples
        file_data = [(file.file_name, file.file_extension, file.event_type, file.date, file.time) for file in files]

        # Insert into treeview
        for row in file_data:
            tree.insert("", "end", values=row)


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
            #self.model.set_table_name(directory_name)
            all_files = self.model.get_all_files()
            for file in all_files:
                print(file.file_name, file.file_extension, file.event_type, file.date, file.time)
                self.display_event(file.file_name, file.file_extension, file.event_type, file.date, file.time)
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


    def display_event(self, file_name, file_extension, event_type, date, time):
        """Display a file event in the text box."""
        # print("Display event called")
        # if not isinstance(file_path, str):
        #     message = str(message)  # Convert to string if it's not already

        self.event_display.insert("", tk.END, text=file_name, values=(file_extension, event_type, date, time))
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


    def alert_security(self):
        pass





if __name__ == "__main__":
    view = View()
    view.run()

