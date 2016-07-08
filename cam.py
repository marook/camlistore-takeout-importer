import json
import subprocess

def camget(*args):
    args_list = list(args)
    args_list.insert(0, 'camget')
    return camexec(*args_list)

def camput(*args):
    args_list = list(args)
    args_list.insert(0, 'camput')
    return [line.strip() for line in subprocess.check_output(args_list).split('\n')]

def camtool(*args):
    args_list = list(args)
    args_list.insert(0, 'camtool')
    return camexec(*args_list)

def camexec(*args):
    out = subprocess.check_output(args)
    if(out == ''):
        return None
    return json.loads(out)
