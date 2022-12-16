# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 12:13:49 2022

@author: dludwinski
"""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from PySimpleGUI import popup


class MonitorFolder(PatternMatchingEventHandler):
    """Watch for creation of a new file or modifiction of an existing file."""

    def __init__(self,
                 watch_dir,
                 search_pattern,
                 ignore_patterns,
                 ignore_directories,
                 case_sensitive,
                 recursive=False):
        """
        Initialize MonitorFolder class to watch for file create or change.

        Parameters
        ----------
        watch_dir : STR
            String for directory path to search for matching patterns in.
        patterns : LIST
            String patterns to look for in file name.
        ignore_patterns : LIST
            String patterns to ignore in file name.
        ignore_directories : LIST
            Directories to ignore when recursive is set to True.
        case_sensitive : BOOL
            Set True if using strict capitalization requirements.
        recursive : BOOL
            Set True if search requires checking children of parent directory
        Returns
        -------
        None.

        """
        super().__init__()
        self.watch_dir = watch_dir
        self.recursive = recursive
        self._handler = MyHandler(search_pattern,
                                  ignore_patterns,
                                  ignore_directories,
                                  case_sensitive,
                                  )
        self.observer = MyObserver()
        self._monitor_func()

    def _monitor_func(self):
        self.observer.schedule(
            self._handler.my_event_handler,
            self.watch_dir,
            recursive=self.recursive,
        )
        self.observer.start()
        try:
            while True:
                time.sleep(60)
        except:
            self.observer.stop()
        self.observer.join()


class MyObserver(Observer):
    """Subclasses observer object and sets the daemon value to True."""

    def __init__(self):
        """
        Initialize Observer class and sets daemon value to True.

        Returns
        -------
        None.

        """
        super().__init__()
        self.daemon = True


class MyHandler(PatternMatchingEventHandler):
    """Subclass of PatternMatchingEventHandler and adds on_any_event action."""

    def __init__(self,
                 patterns,
                 ignore_patterns,
                 ignore_directories,
                 case_sensitive):
        """
        Create MyHandler object for user wih Observer object.

        Parameters
        ----------
        patterns : List of Strings
            String patterns to look for in file name.
        ignore_patterns : List of Strings
            String patterns to ignore in file name.
        ignore_directories : List of Strings
            Directories to ignore when recursive is set to True.
        case_sensitive : Boolean
            Set True if using strict capitalization requirements.

        Returns
        -------
        None.

        """
        super().__init__()
        self.my_event_handler = PatternMatchingEventHandler(
            patterns,
            ignore_patterns,
            ignore_directories,
            case_sensitive,
        )
        self.my_event_handler.on_any_event = on_any_event


def on_any_event(event) -> None:
    """
    Catches all event_types and handle appropriately.

    Parameters
    ----------
    event : watchdog.EventHandler.event

    Returns
    -------
    None.

    """
    if event.event_type == 'created':
        time.sleep(20)
        popup(
            f'{event.src_path}',
            title=f'New File In {Path(event.src_path).parent}',
            grab_anywhere=True,
        )
        time.sleep(60)
    elif event.event_type == 'modified':
        time.sleep(20)
        popup(
            f'{event.src_path} has been modified',
            title=f'Modified File in {Path(event.src_path).parent}',
            grab_anywhere=True,
        )
        time.sleep(60)
    else:
        pass


def main():
    """Watchdog watcher app main function."""
    # Change "watch_dir" to monitor alt directory, or leave monitor where run
    watch_dir = str(Path(__file__).parent)
    # Pattern(s) to search for within directory - accepts regex
    search_pat = ["*"]
    # Patterns to ignore within directory - accepts regex
    ignore_pats = None
    # Ignore directories when recursive set to True
    ignore_dir = False
    # Restrict pattern seach to case sensitive
    case_lock = False
    try:
        watch_f = MonitorFolder(
            watch_dir,
            search_pat,
            ignore_pats,
            ignore_dir,
            case_lock,
            recursive=True,  # Change to False to ignore child directories
        )
    except FileNotFoundError:
        popup(
            'New notifications will not Pop Up until your next restart',
            title=f'You are not connected to {watch_dir}',
            grab_anywhere=True,
        )
    except KeyboardInterrupt:
        return None


if __name__ == '__main__':
    main()
