# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:44:00 2022
@authors: Jan K. Legind, NHMD;
Copyright 2022 Natural History Museum of Denmark (NHMD)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
- Code for monitoring and renaming new csv files coming into the N:\SCI-SNM-DigitalCollections\DaSSCo\DigiApp\Data\0.ForChecking shared directory.
"""

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import monitor_event_handling as meh


class OnMyWatch:
    # Set the directory on watch
    watchDirectory = r'N:\SCI-SNM-DigitalCollections\DaSSCo\DigiApp\Data\0.ForChecking'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        path = event.src_path
        # print(event)
        # print('event type==', event.event_type)
        # print('type of event object', type(event))
        # suff = path.split('.')[-1]
        # print('tHE path is:::', path, 'w suffix=', suff)
        meh.eventProcessor(event)

        if event.is_directory:
            return None

        # elif event.event_type == 'created':
        #     # Event is created, you can process it now
        #     # print("Watchdog received created event - % s." % event.src_path)
        #     meh.eventProcessor(event)
        # elif event.event_type == 'modified':
        #     # Event is modified, you can process it now
        #     print("Watchdog received modified event - % s." % event.src_path)


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
