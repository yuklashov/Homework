"""Локальная модель: файлы + SQLite, не WordPress/MySQL/ispmanager."""
from pathlib import Path
import tempfile, sqlite3, shutil, hashlib, json

def digest(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(path.rglob('*')) if p.is_file()}

def main():
    result = {'mode': 'учебная локальная модель, не запуск ispmanager', 'steps': []}
    with tempfile.TemporaryDirectory(prefix='netology-restore-') as tmp:
        root = Path(tmp)
        live = root / 'netology'; live.mkdir()
        site = live / 'site'; site.mkdir()
        (site / 'index.html').write_text('<h1>Local restore exercise</h1>')
        db = sqlite3.connect(live / 'demo.sqlite')
        db.execute('CREATE TABLE posts(id INTEGER PRIMARY KEY, title TEXT)')
        db.execute('INSERT INTO posts VALUES (1, ?)', ('Recovery exercise',)); db.commit()
        dump = '\n'.join(db.iterdump()); db.close()
        (root / 'database.sql').write_text(dump)
        shutil.make_archive(str(root / 'site'), 'zip', site)
        before = digest(live)
        site_before = digest(site)
        shutil.copytree(live, root / 'system-backup')
        result['steps'].append('Файлы, SQL-дамп и отдельная системная копия модели созданы')
        shutil.rmtree(site); (live / 'demo.sqlite').unlink()
        result['steps'].append('Первый сбой смоделирован только во временном каталоге')
        site.mkdir(); shutil.unpack_archive(root / 'site.zip', site)
        db = sqlite3.connect(live / 'demo.sqlite'); db.executescript(dump)
        assert db.execute('SELECT title FROM posts WHERE id=1').fetchone()[0] == 'Recovery exercise'
        assert "\n".join(db.iterdump()) == dump
        db.close(); assert digest(site) == site_before
        result['steps'].append('Восстановление из файлов+дампа: контрольные суммы и SELECT совпали')
        live.rename(root / 'ispmanager')
        assert not live.exists() and (root / 'ispmanager/site/index.html').exists()
        result['steps'].append('Модель смены владельца: netology -> ispmanager (перемещение каталога)')
        shutil.rmtree(root / 'ispmanager')
        shutil.copytree(root / 'system-backup', live)
        assert digest(live) == before
        result['steps'].append('Второй сбой и восстановление из системной копии: исходный владелец/данные')
        result['checks'] = {'restore_from_dump': True, 'restore_from_system_copy': True, 'original_owner': 'netology'}
    return result

if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
