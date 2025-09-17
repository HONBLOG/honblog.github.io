import os
import sys
import win32api
import win32con
import win32security
import wmi

def get_process_privilleges(pid):
    try:
        hproc = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION, False, pid) # Get handle of the Process
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY) # Open Token
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges) # Get informations of the Token
        privileges = ''
        for priv_id, flags in privs:
            if flags == win32security.SE_PRIVILEGE_ENABLED|win32security.SE_PRIVILEGE_ENABLED_BY_DEFAULT:
                privileges += f'{win32security.LookupPrivilegeName(None, priv_id)}|'
    except Exception:
        privileges = 'N/A'
    return privileges
        
def log_to_file(message):
    with open('process_monitor_log.csv', 'a') as fd:
        fd.write(f'{message}\r\n')
        
def monitor():
    log_to_file('CommandLine, Time, Executable, Parent PID, PID, User, Privilleges')
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for('creation')
    while True:
        try:
            new_process = process_watcher()
            cmdline = new_process.CommandLine
            create_date = new_process.CreationDate
            executable = new_process.ExecutablePath
            parent_pid = new_process.ParentProcessId
            pid = new_process.ProcessId
            proc_owner = new_process.GetOwner()
            
            privilleges = get_process_privilleges(pid)
            process_log_message = (f'{cmdline} , {create_date} , {executable},'
                                   f'{parent_pid} , {pid} , {proc_owner} , {privilleges}')
            print(process_log_message)
            print()
            log_to_file(process_log_message)
        except KeyboardInterrupt:
            print("User Terminated")
            sys.exit()
    
if __name__ == '__main__':
    monitor()