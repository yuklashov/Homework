"""Настоящий rsync на временных файлах Mac; logger подменён локальным журналом модели."""
from pathlib import Path
import tempfile, subprocess, os, json

def run(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, **kwargs)

def main():
    script = Path(__file__).resolve().parents[1] / 'src/home-backup.sh'
    with tempfile.TemporaryDirectory(prefix='netology-rsync-') as tmp:
        root = Path(tmp); source = root/'source'; target=root/'target'; source.mkdir();target.mkdir()
        (source/'visible.txt').write_text('AAAA'); (source/'.profile').write_text('dot file')
        (source/'.hidden').mkdir();(source/'.hidden/data').write_text('sample')
        (source/'nested').mkdir();(source/'nested/.cache').mkdir();(source/'nested/.cache/data').write_text('sample')
        command=['rsync','-a','--checksum','--delete','--exclude=.*/','--',str(source)+'/',str(target)+'/']
        first=run(command);assert first.returncode==0, first.stderr
        assert (target/'.profile').exists() and not (target/'.hidden').exists() and not (target/'nested/.cache').exists()
        stamp=(source/'visible.txt').stat()
        (source/'visible.txt').write_text('BBBB');os.utime(source/'visible.txt',ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
        (target/'obsolete.txt').write_text('obsolete')
        second=run(command);assert second.returncode==0, second.stderr
        assert (target/'visible.txt').read_text()=='BBBB' and not (target/'obsolete.txt').exists()
        tools=root/'tools';tools.mkdir(); log=root/'model-syslog.txt'
        logger=tools/'logger';logger.write_text('#!/bin/sh\nprintf "%s\n" "$*" >> "$MODEL_LOG"\n');logger.chmod(0o700)
        env=dict(os.environ,PATH=str(tools)+os.pathsep+os.environ['PATH'],MODEL_LOG=str(log),BACKUP_SOURCE_DIR=str(source),BACKUP_TARGET_DIR=str(root/'full'))
        good=run(['bash',str(script)],env=env);assert good.returncode==0, good.stderr
        assert (root/'full/.hidden/data').read_text()=='sample'
        env['BACKUP_SOURCE_DIR']=str(root/'missing')
        failed=run(['bash',str(script)],env=env);assert failed.returncode!=0
        env['BACKUP_SOURCE_DIR']=str(source);env['BACKUP_TARGET_DIR']=str(source/'nested-target')
        overlap=run(['bash',str(script)],env=env);assert overlap.returncode!=0
        content=log.read_text();assert 'SUCCESS rc=0' in content and 'FAIL rc=' in content
        return {'mode':'реальные временные файлы Mac + rsync; logger является тестовой заменой',
                'checks':{'hidden_directories_excluded':True,'dotfile_kept':True,
                          'same_size_mtime_change_detected':True,'obsolete_deleted':True,
                          'daily_full_includes_hidden':True,'success_and_failure_logged_to_model':True,
                          'overlapping_paths_refused':True},'cron_installed':False,'linux_syslog_verified':False}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
