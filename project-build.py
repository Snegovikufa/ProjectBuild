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
            workspace_json_data = json.load (f, strict = False)

        if not 'build_system' in workspace_json_data :
            sublime.error_message (
                'ProjectBuild:\n\n'
                'There are no "build_system" value in %s file.\n'
                'Choose build and save project''' % workspace_file)

        build_filename = workspace_json_data['build_system']
        build_sys_file = os.path.join (os.path.dirname (sublime.packages_path ()), build_filename)
        ############################################

        ############################################
        #
        # Creating a dictionary with build system
        # variants. Currently ProjectBuild does not
        # support platform-specific data in the
        # Build System. It may be fixed later.
        #
        with open (build_sys_file) as f :
            json_data = json.load (f)

        build_variants = {}
        if 'cmd' in json_data :
            build_variants['Default'] = " ".join (json_data['cmd'])
        if 'variants' in json_data :
            for k in json_data['variants'] :
                build_variants[k['name']] = " ".join (k['cmd'])
        ############################################


        ############################################
        #
        # Creating and showing quick panel with 
        # build variants.
        def run (selected) :
            if (selected >= 0) :
                self.execute_variant (build_variants.items ()[selected][0])

        self.view.window ().show_quick_panel (build_variants.keys(), run)
        ######################################################

    def execute_variant (self, variant_name) :
        self.view.window ().run_command ("build", {"variant": variant_name})
