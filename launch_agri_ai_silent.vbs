Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & WshShell.CurrentDirectory & "\launch_agri_ai.bat" & Chr(34), 0
Set WshShell = Nothing
