import os
import socket
import subprocess

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
shortcut_path = os.path.join(desktop_path, 'AI Student Attendance System.lnk')
target_path = os.path.abspath('launch_app.vbs')
work_dir = os.path.abspath('.')

vbs_code = f"""
Set WshShell = CreateObject("WScript.Shell")
Set oLink = WshShell.CreateShortcut("{shortcut_path}")
oLink.TargetPath = "{target_path}"
oLink.WorkingDirectory = "{work_dir}"
oLink.Description = "AI Student Facial Recognition Attendance System"
oLink.Save
"""

vbs_file = 'temp_shortcut.vbs'
with open(vbs_file, 'w') as f:
    f.write(vbs_code)

subprocess.run(['cscript', '//Nologo', vbs_file])

if os.path.exists(vbs_file):
    os.remove(vbs_file)

local_ip = get_local_ip()
print(f"Desktop shortcut created successfully at: {shortcut_path}")
print(f"Local PC Access URL:    http://localhost:5005")
print(f"Network (Wi-Fi) URL:    http://{local_ip}:5005")
