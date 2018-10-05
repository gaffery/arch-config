# blender
# Autogenerated from man page /usr/share/man/man1/blender.1.gz
complete -c blender -s b -l background --description 'br Run in background (often used for UI-less rendering). br.'
complete -c blender -s a -l render-anim --description 'br Render frames from start to end (inclusive). br.'
complete -c blender -s S -l scene --description 'br Set the active scene <name> for rendering. br.'
complete -c blender -s f -l render-frame --description 'br Render frame <frame> and save it. br.'
complete -c blender -o '<frame>' --description 'br * A comma separated list of frames can also be used (no spaces).'
complete -c blender -s s -l frame-start --description 'br Set start to frame <frame>, supports +/- for relative frames too. br.'
complete -c blender -s e -l frame-end --description 'br Set end to frame <frame>, supports +/- for relative frames too. br.'
complete -c blender -s j -l frame-jump --description 'br Set number of frames to step forward after each rendered frame. br.'
complete -c blender -s o -l render-output --description 'br Set the render path and file name.'
complete -c blender -s E -l engine --description 'br Specify the render engine. br Use -E help to list available engines. br.'
complete -c blender -s t -l threads --description 'br Use amount of <threads> for rendering and other operations .'
complete -c blender -s F -l render-format --description 'br Set the render format.'
complete -c blender -s x -l use-extension --description 'br Set option to add the file extension to the end of the file. br.'
complete -c blender -s w -l window-border --description 'br Force opening with borders. br.'
complete -c blender -s W -l window-borderless --description 'br Force opening without borders. br.'
complete -c blender -s p -l window-geometry --description 'br Open with lower left corner at <sx>, <sy> and width and height as <w>, <h>.'
complete -c blender -o con -l start-console --description 'br Start with the console window open (ignored if -b is set), (Windows only).'
complete -c blender -l no-native-pixels --description 'br Do not use native pixel size, for high resolution displays (MacBook \'Retin…'
complete -c blender -s g --description 'br.'
complete -c blender -s y -l enable-autoexec --description 'br Enable automatic Python script execution. br.'
complete -c blender -s Y -l disable-autoexec --description 'br Disable automatic Python script execution (pydrivers & startup scripts), (…'
complete -c blender -s P -l python --description 'br Run the given Python script file. br.'
complete -c blender -l python-text --description 'br Run the given Python script text block. br.'
complete -c blender -l python-expr --description 'br Run the given expression as a Python script. br.'
complete -c blender -l python-console --description 'br Run Blender with an interactive console. br.'
complete -c blender -l python-exit-code --description 'br Set the exit-code in [0. 255] to exit if a Python exception is raised .'
complete -c blender -l addons --description 'br Comma separated list of add-ons (no spaces). br.'
complete -c blender -s d -l debug --description 'br Turn debugging on. br.'
complete -c blender -l debug-value --description 'br Set debug value of <value> on startup. br.'
complete -c blender -l debug-events --description 'br Enable debug messages for the event system. br.'
complete -c blender -l debug-ffmpeg --description 'br Enable debug messages from FFmpeg library. br.'
complete -c blender -l debug-handlers --description 'br Enable debug messages for event handling. br.'
complete -c blender -l debug-libmv --description 'br Enable debug messages from libmv library. br.'
complete -c blender -l debug-cycles --description 'br Enable debug messages from Cycles. br.'
complete -c blender -l debug-memory --description 'br Enable fully guarded memory allocation and debugging. br.'
complete -c blender -l debug-jobs --description 'br Enable time profiling for background jobs. br.'
complete -c blender -l debug-python --description 'br Enable debug messages for Python. br.'
complete -c blender -l debug-depsgraph --description 'br Enable debug messages from dependency graph. br.'
complete -c blender -l debug-depsgraph-no-threads --description 'br Switch dependency graph to a single threaded evaluation. br.'
complete -c blender -l debug-gpumem --description 'br Enable GPU memory stats in status bar. br.'
complete -c blender -l debug-wm --description 'br Enable debug messages for the window manager, also prints every operator c…'
complete -c blender -l debug-all --description 'br Enable all debug messages. br.'
complete -c blender -l debug-io --description 'br Enable debug messages for I/O (collada, . ). br.'
complete -c blender -l debug-fpe --description 'br Enable floating point exceptions. br.'
complete -c blender -l disable-crash-handler --description 'br Disable the crash handler. br.'
complete -c blender -l factory-startup --description 'br Skip reading the BLENDER_STARTUP_FILE in the users home directory. br.'
complete -c blender -l env-system-datafiles --description 'br Set the BLENDER_SYSTEM_DATAFILES environment variable. br.'
complete -c blender -l env-system-scripts --description 'br Set the BLENDER_SYSTEM_SCRIPTS environment variable. br.'
complete -c blender -l env-system-python --description 'br Set the BLENDER_SYSTEM_PYTHON environment variable. br.'
complete -c blender -o nojoystick --description 'br Disable joystick support. br.'
complete -c blender -o noglsl --description 'br Disable GLSL shading. br.'
complete -c blender -o noaudio --description 'br Force sound system to None. br.'
complete -c blender -o setaudio --description 'br Force sound system to a specific device. br \'NULL\' \'SDL\' \'OPENAL\' \'JACK\'.'
complete -c blender -s h -l help --description 'br Print this help text and exit. br.'
complete -c blender -s v -l version --description 'br Print Blender version and exit. br.'
complete -c blender -l enable-new-depsgraph --description 'br Use new dependency graph. br.'
complete -c blender -l enable-new-basic-shader-glsl --description 'br Use new GLSL basic shader. br.'
complete -c blender -l disable-abort-handler --description 'br Disable the abort handler. br.'
complete -c blender -l debug-freestyle --description 'br Enable debug messages for FreeStyle. br.'
complete -c blender -l debug-gpu --description 'br Enable gpu debug context and information for OpenGL 4. 3+. br.'
complete -c blender -l verbose --description 'br Set logging verbosity level. br.'
complete -c blender -s R --description 'br Register blend-file extension, then exit (Windows only). br.'
complete -c blender -s r --description 'br Silently register blend-file extension, then exit (Windows only). br.'
complete -c blender -s m --description '.'

