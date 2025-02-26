from watchdog.observers import Observer
import time

class WatchDogImpl:
    def __init__(self, directory_to_watch, event_handler, fw_view):
        self.watch_directory = directory_to_watch
        self.event_handler = event_handler
        self.watchdogObserver = Observer()
        self.running = False  # Flag to control the loop
        self.view = fw_view

    def watch(self):
        self.watchdogObserver.schedule(self.event_handler, self.watch_directory, recursive=True)
        self.watchdogObserver.start()
        self.view.run()
        self.running = True
        print(f"Started watching: {self.watch_directory}")
        try:
            while self.running:  # Use a flag to control the loop
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Received KeyboardInterrupt. Stopping watchdog...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.stop()

    def stop(self):
        """Stop watching the directory."""
        if self.running:
            self.running = False
            self.watchdogObserver.stop()
            self.watchdogObserver.join()
            print("watchdogObserver Stopped")