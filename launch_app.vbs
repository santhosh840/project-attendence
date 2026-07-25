Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strPath = fso.GetAbsolutePathName(".")
WshShell.Run "pythonw app.py", 0, False
WScript.Sleep 2500
WshShell.Run "http://localhost:5005", 1, False
