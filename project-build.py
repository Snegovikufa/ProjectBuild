import sublime
import sublime_plugin
import json
import sys
import os

# If you want use Non-ASCII characters 
# (for example, Russian) in comments here
# you must save this file in UTF-8 encoding with BOM

class ProjectBuildCommand (sublime_plugin.TextCommand) :
    def run (self, edit = None) :
        # Save file if dirty
        if self.view.is_dirty () :
            self.view.run_command ('save')

        ############################################
        # 
        # Detecting workspace file
        #
        workspace_file = None
        root_folders = self.view.window ().folders ()
        for dir_ in root_folders :
            for dir_item in os.listdir (dir_) :
                if  dir_item.endswith ('.sublime-workspace') :
                    if  workspace_file == None :
                        workspace_file = os.path.join (os.path.normpath(dir_), dir_item)
                    else :
                        self.showError (
                            'Must be only one ".sublime-workspace" file in project root folder.\n'
                            'Plugin found %s and %s files.' %
                            (workspace_file, os.path.join (dir_, dir_item)))
                        return
        if workspace_file == None :
            self.showError (
                'There are no ".sublime-workspace" file in any root folder of project.')
            return
        self.debug(workspace_file) 
        # 
        ############################################

        ############################################
        #
        # Get build system filename 
        # from workspace file
        #
        with open (workspace_file) as f :
            try:
                workspace_json_data = json.load (f, strict = False)
            except Exception, e:
                self.showError (
                    'File .sublime-workspace is empty or has incorrect json data')
                return
        if not 'build_system' in workspace_json_data :
            self.showError (
                'There are no "build_system" value in %s file.\n'
                'Choose Build System and save project.' % workspace_file)
            return
        build_filename = workspace_json_data['build_system']
        self.debug(build_filename)         
        # 
        ############################################
        
        ############################################
        #
        # Detect Build System file
        # 
        # "build_system" variable have mask-pattern of its value like 
        # "Packages/User/{YourOwnBuildSystem}.sublime-build" or
        # "Packages/{SomePackage}/{SomePackageBulidSystem}.sublime-build" or
	# "" - empty      
	#
	# Sublime Text 2 documentation:         
        # "Build systems must be located somewhere 
	# under the Packages folder (e.g. Packages/User).
	# Many packages include their own build systems."
	#
        # so full path to Build System file is uniquely determined

        build_filename_fullpath = os.path.normpath(os.path.join(os.path.dirname(sublime.packages_path()),build_filename))
	# it must be exist and it must be a file
        if not(os.path.isfile(build_filename_fullpath)):
            self.showError (
                'Plugin could not find Build System file: "%s".' %
                build_filename_fullpath)
            return        
        self.debug(build_filename_fullpath)         
        # 
        ############################################

        ############################################
        #
        # Load data from Build System file
        #
        with open (build_filename_fullpath) as f :
            try:
                json_data = json.load (f)
            except Exception, e:
                self.showError (
                    'File %s is empty or has incorrect json data' %
		     build_filename_fullpath)
                return
        #
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
        #
        ############################################
 
        ############################################
        #
        # Creating and showing quick panel with 
        # build variants.
        # 
        def run (selected) :
            if (selected >= 0) :
                self.execute_variant (build_variants[selected][0])

        names = [name for name, args in build_variants]
        self.view.window ().show_quick_panel (names, run)
        #
        ############################################

    def execute_variant (self, variant_name) :
        self.view.window ().run_command ("build", {"variant": variant_name})

    def showError (self, err) :
        # sometime error_message does not be shown
        sublime.error_message ('ProjectBuild:\n\n%s' % err)
        
    def debug (self, message) :
        # change True to False or vice versa
        if (False): print message
        

