import sublime
from sublime_plugin import WindowCommand

from .base_command import BaseCommand


ALL_REMOTES = "All remotes."


class GgFetchCommand(WindowCommand, BaseCommand):

    def run(self):
        self.remotes = list(self.get_remotes().keys())
        if not self.remotes:
            self.window.show_quick_panel(["There are no remotes available."], None)
        else:
            if len(self.remotes) > 1:
                self.remotes.push(ALL_REMOTES)
            self.window.show_quick_panel(self.remotes, self.on_selection, sublime.MONOSPACE_FONT)

    def on_selection(self, remotes_index):
        if remotes_index == -1:
            return

        remote = self.remotes[remotes_index]
        if remote == ALL_REMOTES:
            sublime.set_timeout_async(lambda: self.do_fetch())
        else:
            sublime.set_timeout_async(lambda: self.do_fetch(remote))

    def do_fetch(self, remote=None):
        sublime.status_message("Starting fetch...")
        self.fetch(remote)
        sublime.status_message("Fetch complete.")