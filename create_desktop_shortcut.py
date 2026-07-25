import os
import sys
import subprocess

def create_windows_desktop_shortcut():
    project_dir = os.path.abspath(os.path.dirname(__file__))
    target_script = os.path.join(project_dir, "launch_agri_ai_silent.vbs")
    
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop_dir, "AgriAI Agriculture Officer.lnk")
    
    esc_shortcut_path = shortcut_path.replace('\\', '\\\\')
    esc_target_script = target_script.replace('\\', '\\\\')
    esc_project_dir = project_dir.replace('\\', '\\\\')
    
    vbs_script = f'''
    Set WshShell = CreateObject("WScript.Shell")
    Set shortcut = WshShell.CreateShortcut("{esc_shortcut_path}")
    shortcut.TargetPath = "wscript.exe"
    shortcut.Arguments = """{esc_target_script}"""
    shortcut.WorkingDirectory = "{esc_project_dir}"
    shortcut.Description = "AgriAI - 24/7 Virtual Personal Agriculture Officer"
    shortcut.WindowStyle = 1
    shortcut.Save
    '''
    
    temp_vbs = os.path.join(project_dir, "temp_shortcut_creator.vbs")
    with open(temp_vbs, "w") as f:
        f.write(vbs_script)
        
    try:
        subprocess.run(["cscript", "//Nologo", temp_vbs], check=True)
        print(f"[SUCCESS] Desktop Shortcut created successfully at: {shortcut_path}")
    except Exception as e:
        print(f"[ERROR] Failed to create desktop shortcut: {e}")
    finally:
        if os.path.exists(temp_vbs):
            os.remove(temp_vbs)

if __name__ == "__main__":
    create_windows_desktop_shortcut()
