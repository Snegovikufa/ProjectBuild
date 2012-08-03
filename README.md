ProjectBuild
============

ProjectBuild is a Sublime Text 2 plugin for running build command with variable arguments selection.


Install
-------

Download the latest source from [GitHub](https://github.com/Snegovikufa/ProjectBuild) and copy *ProjectBuild* folder to your ST2 "Packages" directory.

Or clone the repository to your ST2 "Packages" directory:

    git clone https://github.com/Snegovikufa/ProjectBuild.git


The "Packages" directory is located at:

* OS X:

        ~/Library/Application Support/Sublime Text 2/Packages/

* Linux:

        ~/.config/sublime-text-2/Packages/

* Windows:

        %APPDATA%/Sublime Text 2/Packages/

Features / Usage
----------------

 * Edit your key bindings like this:

        [
          { "keys": ["shift+f10"], "command" : "project_build"}
        ]
 * Run Preferences - Package Settings - Project Build - Settings. Edit like this: 

        {
            "cmd" : "/home/user/sandbox/mycommand",
            "build_args" : {
                "MyBuild" : ["/home/user/sandbox/test-models/Test1/test1.dat"],
                "AwesomeBuild" : ["/home/user/sandbox/test-models/Test2/test2.DAT"]
            },
            "dir" : "/home/user/sandbox/"
        }


 * Hit Shift + F10 and select arguments for build.

![Error list](http://img844.imageshack.us/img844/7721/201208031142312960x1050.png)

