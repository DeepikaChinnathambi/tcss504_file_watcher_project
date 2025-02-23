"""
eventually will need to have a spot you run the code from that activates the GUI.
"""

from FileWatcher import *



if __name__ == '__main__':
    model = FileModel()
    view = View()
    watcher1 = FileWatcher(r".\test", model,view)
    watcher1.start_watchdog_for_directory()


