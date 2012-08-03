import sublime
import sublime_plugin
import subprocess
import sys
import threading

settings = sublime.load_settings("ProjectBuild.sublime-settings")


class LogThread(threading.Thread):
    def __init__ (self, proc) :
        super (LogThread, self).__init__()
        self._proc = proc

    def run(self):
        proc = self._proc
        while proc.poll () is None:
            inline = proc.stderr.readline()
            if not inline:
                break
            sys.stderr.write(inline)
            sys.stderr.flush()


class ProjectBuildCommand(sublime_plugin.TextCommand):
    def run(self, edit=None):
        filename = self.view.file_name()

        if not filename:
            return

        # Save file if dirty
        if self.view.is_dirty():
            self.view.run_command('save')

        def run (selected):
            self.execute_cmd (values[selected])

        args = settings.get('build_args')
        keys = sorted ([key for key in args])
        values = [args[key] for key in keys]

        self.view.window ().show_quick_panel (keys, run)

    def execute_cmd (self, args):
        cmd = " ".join ([settings.get ('cmd')] + args)
        proc = subprocess.Popen(
            cmd, shell=True,
            bufsize=1024,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        LogThread (proc).start ()
