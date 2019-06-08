import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="The Lost Cowboy Adventures"
    options = {"build_exe": {"packages":["pygame"], "include_files":["racecar.png"]}},
    executables = executables

)