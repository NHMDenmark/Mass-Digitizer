[app]

# title of your application
title = DaSSCo Mass Digitizer

# project directory. the general assumption is that project_dir is the parent directory
# of input_file
project_dir = C:\Users\vsb582\Documents\Work\Dev\Code\Mass-Digitizer\MassDigitizer

# source file path
input_file = C:\Users\vsb582\Documents\Work\Dev\Code\Mass-Digitizer\MassDigitizer\DaSSCo.py

# directory where the executable output is generated
exec_directory = .

# path to .pyproject project file
project_file = 

# application icon
icon = C:\Users\vsb582\Documents\Work\Dev\Code\Mass-Digitizer\MassDigitizer\.venv\Lib\site-packages\PySide6\scripts\deploy_lib\pyside_icon.ico

[python]

# python path
python_path = C:\Users\vsb582\Documents\Work\Dev\Code\Mass-Digitizer\MassDigitizer\.venv\Scripts\python.exe

# python packages to install
packages = Nuitka==2.5.1

# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# comma separated path to qml files required
# normally all the qml files required by the project are added automatically
qml_files = 

# excluded qml plugin binaries
excluded_qml_plugins = 

# qt modules used. comma separated
modules = UiTools,Widgets,Core,Gui

# qt plugins used by the application. only relevant for desktop deployment. for qt plugins used
# in android application see [android][plugins]
plugins = platforminputcontexts,platforms,platformthemes,egldeviceintegrations,iconengines,imageformats,accessiblebridge,xcbglintegrations,platforms/darwin,styles,generic

[android]

# path to pyside wheel
wheel_pyside = 

# path to shiboken wheel
wheel_shiboken = 

# plugins to be copied to libs folder of the packaged application. comma separated
plugins = 

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 

# mode of using nuitka. accepts standalone or onefile. default is onefile.
mode = onefile

# (str) specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations

[buildozer]

# build mode
# possible options = [release, debug]
# release creates an aab, while debug creates an apk
mode = debug

# contrains path to pyside6 and shiboken6 recipe dir
recipe_dir = 

# path to extra qt android jars to be loaded by the application
jars_dir = 

# if empty uses default ndk path downloaded by buildozer
ndk_path = 

# if empty uses default sdk path downloaded by buildozer
sdk_path = 

# other libraries to be loaded. comma separated.
# loaded at app startup
local_libs = 

# architecture of deployed platform
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
arch = 

