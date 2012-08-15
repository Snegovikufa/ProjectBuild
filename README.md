ProjectBuild
============

ProjectBuild is a Sublime Text 2 plugin for running Build command with its variants.
Just choose Build System "Tools"->"Build System" (it can be standart or your own), 
save Sublime project in some root folder of your project, press "Shift+F10" so you can see 
quickpanel with Build System variants. Also you can use standart "F7", "Ctrl+B" and "Ctrl+Shift+B"
key bindings.
Now ProjectBuild does not support platform-specific data in the Build System. May be we fix this later.


Authors
-------

 * Snegovikufa (Rustam Safin) (https://github.com/Snegovikufa)
 * BorisPlus (Borisov ILYA) (https://github.com/BorisPlus)


Install
-------

Download the latest source from [GitHub](https://github.com/Snegovikufa/ProjectBuild) and copy *ProjectBuild* folder to your Sublime Text 2 "Packages" directory.

Or clone the repository to your Sublime Text 2 "Packages" directory:

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

 * Edit your key bindings "Preferences"->"Key Bindings - User" like this:

        [
          { "keys": ["shift+f10"], "command" : "project_build"}
        ]

 * Create your own Build System "Tools"->"Build System"->"New Build System", for example with Ant using - "AntBuildSystem", like this:
	
        {
            "cmd": ["ant.bat"],
            "working_dir": "${project_path}",
            "variants" : [
                {
                    "name": "Init",
                    "cmd": ["ant.bat", "init"]
                },
                {
                    "name": "Run",
                    "cmd": ["ant.bat", "trial"]
                }
            ]
        }

 After that don't foget to choose this Build System in Sublime Text 2. Of course you can use anyone standart Build System.

 * Just save Sublime project in some root folder of your project «Project»->«Save Project As...». So automatically  "<name>.sublime-workspace" file must be created with json-content like this:

        ...
            "build-system" : "Packages/User/AntBuildSystem.sublime-build"
        ...

 * Press "Shift+F10" and select arguments for build.

![Error list](http://img844.imageshack.us/img844/7721/201208031142312960x1050.png)

![Comment](https://raw.github.com/Snegovikufa/ProjectBuild/master/ProjectBuild%20with%20comment.png)

