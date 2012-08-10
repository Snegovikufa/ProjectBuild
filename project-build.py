import sublime
import sublime_plugin

settings = sublime.load_settings("ProjectBuild.sublime-settings")


class ProjectBuildCommand(sublime_plugin.TextCommand):
    def run(self, edit=None):
        filename = self.view.file_name()

        if not filename:
            return

        # Save file if dirty
        if self.view.is_dirty():
            self.view.run_command('save')

        def run (selected):
            self.execute_cmd (keys[selected])

        f = settings.get('file')
        self._buildSettings = sublime.load_settings (f)
        self._variants = {}
        for variant in self._buildSettings.get ('variants') :
            key = variant['name']
            self._variants[key] = variant['cmd']

        keys = []
        keys = sorted (self._variants.keys())

        self.view.window ().show_quick_panel (keys, run)

    def execute_cmd (self, variant):
        self.view.window().run_command("build", {"variant" : variant})
