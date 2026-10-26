"""Run the five macOS commands and save only public hardware/OS fields."""
from pathlib import Path
import argparse
import json
import platform
import subprocess

BASE = Path(__file__).resolve().parents[1]
COMMANDS = [
    ('01-sw-vers', ['/usr/bin/sw_vers']),
    ('02-uname', ['/usr/bin/uname', '-a']),
    ('03-system-profiler', ['/usr/sbin/system_profiler']),
    ('04-cpu', ['/usr/sbin/sysctl', '-n', 'machdep.cpu.brand_string']),
    ('05-hardware', ['/usr/sbin/system_profiler', 'SPHardwareDataType']),
]
FIELDS = {'Model Name','Model Identifier','Model Number','Chip','Processor Name',
          'Processor Speed','Total Number of Cores','Number of Processors',
          'Memory','System Firmware Version','OS Loader Version','System Version',
          'Kernel Version','Boot Mode'}

def safe_summary(text):
    section = None
    lines = []
    for line in text.splitlines():
        if line and not line[0].isspace() and line.endswith(':'):
            section = line[:-1]
        if section in {'Hardware', 'Software'} and ':' in line and line.strip().split(':',1)[0] in FIELDS:
            lines.append(line)
    return '\n'.join(lines)

def collect():
    if platform.system() != 'Darwin':
        raise SystemExit('This assignment variant requires macOS.')
    dest=BASE/'evidence'
    dest.mkdir(exist_ok=True)
    manifest=[]
    for stem,args in COMMANDS:
        result=subprocess.run(args,capture_output=True,text=True,timeout=180,check=True)
        output=result.stdout.strip()
        if stem in {'03-system-profiler','05-hardware'}:
            output=safe_summary(output)
        if stem=='02-uname':
            output=output.replace(platform.node(),'[hostname]')
        if not output:
            raise RuntimeError(f'Empty output: {stem}')
        display='$ '+' '.join(Path(a).name if i==0 else a for i,a in enumerate(args))+'\n'+output+'\n'
        if stem in {'03-system-profiler','05-hardware'}:
            display+='\n[Only OS and hardware fields retained; private identifiers omitted.]\n'
        (dest/(stem+'.txt')).write_text(display)
        manifest.append({'command':args,'exit_code':result.returncode,'file':stem+'.txt'})
    (dest/'commands.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Saved five command results with private identifiers excluded.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--show',type=int,choices=range(1,6))
    args=parser.parse_args()
    if args.show:
        print('\033[2J\033[H',end='')
        print((BASE/'evidence'/(COMMANDS[args.show-1][0]+'.txt')).read_text())
    else:
        collect()
