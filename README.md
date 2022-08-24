# Requirements:
    OpenCV

# Adding OpenCV To Path (Windows)
    Advanced system settings > Environment Variables > Path > Edit > New > Add the path that looks like: "C:\opencv\build\x64\vc14\bin" to the PATH

# Instructions for OpenCV Configuration For Visual Studio:
    1. Project Properties > C/C++ > General > Add what looks like: "C:\opencv\build\include" to Additional Include Directories 
    2. Project Properties > Linker > General > Add what looks like: "C:\opencv\build\x64\vc14\lib" to Additional Library Directories
    3. Under Linker Again > Input > Add what looks like: "opencv_world341d.lib" (it should have a d at the end) to Additional Dependencies



