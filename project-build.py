import sublime
import sublime_plugin
import json
import sys
import os

class ProjectBuildCommand(sublime_plugin.TextCommand):
    def run(self, edit=None):
        try:
            ############################################
            # 
            # Getting current Build System automatically
            # 
            ____workspace_file = ""
            ____root_folders = self.view.window().folders()
            for ____dir in ____root_folders :
                # DEBUG  print ____dir
                for ____dir_item in os.listdir(____dir):
                    if  ____dir_item.endswith('.sublime-workspace'):
                        if  ____workspace_file == "":
                            ____workspace_file = os.path.join(____dir,____dir_item)
                        else:
                            raise Exception('Must be only one ".sublime-workspace" file of project in root project folders.','Plugin find "'+____workspace_file+'" and "'+os.path.join(____dir,____dir_item)+'".')
            if  ____workspace_file == "":
                raise Exception('Missing ".sublime-workspace" file.','There are no ".sublime-workspace" file in any root folder of project.')                
            # DEBUG print ____workspace_file            
            f = open(____workspace_file)
            workspace_json_data = json.load(f, strict=False)
            f.close()            
            if not('build_system' in workspace_json_data):
                raise Exception('Choose Build and save project.','There are no saved "build_system" value in "'+____workspace_file+'".')                
            ____current_build_system_file_name = workspace_json_data['build_system']
            ____current_build_system_file =  os.path.join(os.path.dirname(sublime.packages_path()),____current_build_system_file_name)
            # 
            # DEBUG print ____current_build_system_file_name
            #  
            ############################################             
                        
            ############################################
            # 
            # Appending dictionary of current Build System variants
            # Now ProjectBuild does not support platform-specific data in the Build System. May be we fix this later.
            #             
            f = open(____current_build_system_file)
            json_data = json.load(f)
            f.close()
            self.____build_variants = {}
            if ('cmd' in json_data):
                self.____build_variants['Default'] = " ".join (json_data['cmd'])
            if ('variants' in json_data):
                for k in json_data['variants'] :
                    self.____build_variants[k['name']] = " ".join (k['cmd'])
            # 
            ############################################

            # Save file if dirty
            if self.view.is_dirty():
                self.view.run_command('save')

            # Run selected Build System variant
            def run (selected):
                if (selected >= 0):
                    self.execute_variant(self.____build_variants.items()[selected][0])

            # Show panel with current Build System variants
            self.view.window().show_quick_panel (self.____build_variants.keys(), run)
        except IOError as err:
            print "I/O error:\n{0}\n{1}".format(err.errno, err.strerror)
        except Exception as exc:
            print "Exception:\n{0}\n{1}".format(exc.args[0], exc.args[1])
        except:
            print "Error:", sys.exc_info()[0]

    def execute_variant (self, variant_name):
        self.view.window().run_command("build", {"variant": variant_name})
