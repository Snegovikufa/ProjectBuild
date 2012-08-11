import sublime
import sublime_plugin
import json
import sys
import os

class ProjectBuildCommand (sublime_plugin.TextCommand) :
    def run (self, edit = None) :
        # Save file if dirty
        if self.view.is_dirty () :
            self.view.run_command ('save')

        ############################################
        # 
        # Detecting build system file
        #
        workspace_file = ""
        root_folders = self.view.window ().folders ()
        for dir_ in root_folders :
            for dir_item in os.listdir (dir_) :
                if  dir_item.endswith ('.sublime-workspace') :
                    if  workspace_file == "" :
                        workspace_file = os.path.join (dir_, dir_item)
                    else :
                        sublime.error_message (
                            'ProjectBuild:\n\n'
                            'Must be only one ".sublime-workspace" file in project root folder.\n'
                            'Plugin found %s and %s files.' %
                            (workspace_file, os.path.join (dir_, dir_item)))
                        return

        if workspace_file == "" :
            sublime.error_message (
                'ProjectBuild:\n\n'
                'Missing ".sublime-workspace" file.\n'
                'There are no ".sublime-workspace" file in any root folder of project.')
            return
        ############################################

        ############################################
        #
        # Loading build system from workspace_file
        #
        with open (workspace_file) as f :
            try:
                workspace_json_data = json.load (f, strict = False)
            except Exception, e:
                sublime.error_message (
                    'ProjectBuild:\n\n'
                    'File .sublime-workspace is empty or has incorrect json data')
                return

        if not 'build_system' in workspace_json_data :
            sublime.error_message (
                'ProjectBuild:\n\n'
                'There are no "build_system" value in %s file.\n'
                'Choose build and save project''' % workspace_file)
            return

        build_filename = workspace_json_data['build_system']

        candidates = [
            os.path.join (sublime.packages_path (), build_filename),
            os.path.join (sublime.packages_path (), "User", build_filename),
            os.path.join (sublime.packages_path (), "ProjectBuild", build_filename)]
        build_sys_file = None
        for candidate in candidates :
            if os.path.exists (candidate) :
                build_sys_file = candidate
                break

        if build_sys_file is None :
            sublime.error_message (
                'ProjectBuild:\n\n'
                'No such file or directory: %s'
                % build_sys_file)
            return

        with open (build_sys_file) as f :
            try:
                json_data = json.load (f)
            except Exception, e:
                sublime.error_message (
                    'ProjectBuild:\n\n'
                    'File %s is empty or has incorrect json data'
                    % build_sys_file)
                return
        ############################################

        ############################################
        #
        # Creating a dictionary with build system
        # variants. Currently ProjectBuild does not
        # support platform-specific data in the
        # Build System. It may be fixed later.
        #
        build_variants = []

        if "cmd" in json_data:
            build_variants.append (['Default', " ".join (json_data["cmd"])])

        for variant in json_data.get ("variants", {}) :
            build_variants.append (
                [variant['name'], " ".join (variant['cmd'])])
        ############################################


        ############################################
        #
        # Creating and showing quick panel with 
        # build variants.
        def run (selected) :
            if (selected >= 0) :
                self.execute_variant (build_variants[selected][0])

        names = [name for name, args in build_variants]
        self.view.window ().show_quick_panel (names, run)
        ######################################################

    def execute_variant (self, variant_name) :
        self.view.window ().run_command ("build", {"variant": variant_name})
