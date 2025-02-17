"""
intending this to be the main script housing the tkinter gui and controller logic
"""

import tkinter as tk
import copy


class View():
    def __init__(self, directory=None):
        self.directory = directory



    def configure_run(self):
        root = tk.Tk()
        root.geometry("600x750")
        root.title("Configure Dog Watcher")
        topFrame = tk.Frame(root)
        topLeftFrame = tk.Frame(topFrame)
        topRightFrame = tk.Frame(topFrame)
        bottomFrame = tk.Frame(root)
        bottomLeftFrame = tk.Frame(bottomFrame)
        bottomRightFrame = tk.Frame(bottomFrame)

        # create subsection labels and make the text wrap
        titleTop = tk.Label(root,
                            text="Add directory to watch")
        titleTop.bind('<Configure>', lambda e: titleTop.config(wraplength=titleTop.winfo_width()))
        titleBottom = tk.Label(root,
                               text="Event History")
        titleBottom.bind('<Configure>', lambda e: titleBottom.config(wraplength=titleBottom.winfo_width()))

        # add the subsection labels and frames to the GUI
        titleTop.pack()
        topFrame.pack()
        titleBottom.pack()
        bottomFrame.pack()
        topLeftFrame.pack(side=tk.LEFT)
        topRightFrame.pack(side=tk.RIGHT)
        bottomLeftFrame.pack(side=tk.LEFT)
        bottomRightFrame.pack(side=tk.RIGHT)

        # define callback functions for button and list events
        def onDisplayListSelect(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                data = event.widget.selection_get().split('\n')
                displayBox.configure(text=data)
            else:  # if nothing is selected, clear the box
                displayBox.configure(text="")

        def onAddButtonClick():
            addVal = displayBox.selection_get().split('\n')
            if addVal != "":
                for a in addVal:
                    addedList.insert(addedList.size(), a)  # add selected engine to end of addedList

        def onAddButtonClickManual():
            addVal = displayBox_manual.get("1.0", tk.END)
            if addVal != "":
                addVal = addVal
                addedList.insert(addedList.size(), addVal)

        def onRemoveButtonClick():
            selectedItem = addedList.curselection()
            if selectedItem:
                addedList.delete(selectedItem[0])

        def onUseButtonClick(rList):
            # get all selected_engines in addList and add them to rList
            rList['vals'] = []
            vals = addedList.get(0, tk.END)
            for val in vals:
                rList['vals'].append(val)
            root.destroy()  # close GUI

        # create list to display engine and a scrollbar
        displayList = tk.Listbox(bottomLeftFrame, height=25, selectmode='multiple')
        displayList.bind("<<ListboxSelect>>", onDisplayListSelect)
        scrollbar = tk.Scrollbar(bottomLeftFrame)

        # create list for added engine and a scrollbar
        addedList = tk.Listbox(bottomRightFrame, height=25, selectmode='multiple')
        scrollbar2 = tk.Scrollbar(bottomRightFrame)

        # add list and scrollbar to frame division on the correct sides
        displayList.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        # attach the scrollbar to the side of the list
        displayList.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=displayList.yview)


        # create a box to display the currently selected engine size and a button to finish selecting it
        displayBox = tk.Label(topLeftFrame, height=1, width=20, borderwidth=1, relief="solid", bg="white")
        addButton = tk.Button(topLeftFrame, height=1, width=15, text="Add engine(s)", command=onAddButtonClick)

        # create box and display to manually enter selected_engines
        displayBox_manual = tk.Label(topLeftFrame, height=1, width=20, borderwidth=1, relief="solid", bg="white")
        addButton_manual = tk.Button(topLeftFrame, height=1, width=20, text="Add non-listed engine",
                                     command=onAddButtonClickManual)

        # add elements for custom enteres engine list
        displayBox_manual.pack(side=tk.TOP, padx=10, pady=10)
        addButton_manual.pack(side=tk.TOP, padx=10, pady=10)

        # add elements to the display from engine list
        displayBox.pack(side=tk.TOP, padx=10, pady=10)
        addButton.pack(side=tk.TOP, padx=10, pady=10)


        # add list and scrollbar to frame division on the correct sides
        addedList.pack(side=tk.LEFT, pady=5)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.BOTH, pady=5)
        addedList.config(yscrollcommand=scrollbar2.set)
        scrollbar2.config(command=addedList.yview)

        # dictionary to contain the list of selected selected_engines. Is a dictionary so that when it is passed to onUseButtonClick, it can be edited by the
        # function (tkinter doesn't support returning values from a callback function for some reason so I had to get creative)
        dir_events = {'vals': []}

        # define buttons to remove selected_engines from the added list, and to export the selected selected_engines and close the GUI
        useButton = tk.Button(topRightFrame, height=1, width=15, text="Run",
                              command=lambda: onUseButtonClick(dir_events))
        removeButton = tk.Button(topRightFrame, height=1, width=15, text="Remove engine", command=onRemoveButtonClick)
        removeButton.pack(side=tk.TOP, padx=10, pady=10)
        useButton.pack(side=tk.BOTTOM, padx=10, pady=10)

        root.attributes('-topmost', True)
        root.after(50, lambda: root.focus_force())
        root.after(60, lambda: root.after_idle(root.attributes, '-topmost', False))

        # run the GUI
        root.mainloop()


        selected_engines = dict((k, v) for k, v in self.masterDict.items() if k in dir_events['vals'])

        return selected_engines
