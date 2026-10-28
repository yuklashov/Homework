"""Syntax checks and Jinja rendering only. Never deploys to hosts."""
from pathlib import Path
import hashlib,json,os,subprocess,tempfile
import jinja2,yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

def main():
    records=[]
    env=os.environ.copy()
    with tempfile.TemporaryDirectory(prefix="netology-ansible-syntax-") as scratch:
        env["ANSIBLE_LOCAL_TEMP"]=scratch
        env["ANSIBLE_NOCOLOR"]="1"
        version=subprocess.run(["ansible-playbook","--version"],cwd=SRC,env=env,text=True,capture_output=True,check=True).stdout.splitlines()[0]
        for playbook in sorted(SRC.glob("[1-5]_*.yml")):
            run=subprocess.run(["ansible-playbook","-i","inventory.syntax.ini","--syntax-check",playbook.name],cwd=SRC,env=env,text=True,capture_output=True)
            records.append({"file":playbook.name,"exit_code":run.returncode,"stdout":run.stdout.strip(),"stderr":run.stderr.strip()})
            assert run.returncode==0,records[-1]
    yaml_files=list(SRC.rglob("*.yml"))
    for file in yaml_files:
        yaml.safe_load(file.read_text())
    for name in ["3_motd.yml", "4_motd_v2.yml"]:
        content = yaml.safe_load((SRC / name).read_text())[0]["tasks"][0]["ansible.builtin.copy"]["content"]
        assert content.endswith(chr(10)), "MOTD must end with an actual newline"
    task_files=list((SRC/"roles").rglob("tasks/*.yml"))+list(SRC.glob("[1-5]_*.yml"))
    for file in task_files:
        text=file.read_text()
        assert "ansible.builtin.shell:" not in text and "ansible.builtin.command:" not in text
    tasks=yaml.safe_load((SRC/"roles/apache_role/tasks/main.yml").read_text())
    notified=[t for t in tasks if "notify" in t]
    assert len(notified)==1 and notified[0]["ansible.builtin.template"]["src"]=="000-default.conf.j2"
    template=jinja2.Environment(undefined=jinja2.StrictUndefined).from_string((SRC/"roles/apache_role/templates/index.html.j2").read_text())
    cases=[]
    for name in ["sda","vda","nvme0n1",None]:
        facts={"hostname":"study-demo","default_ipv4":{"address":"192.0.2.10"},"processor_vcpus":2,"memtotal_mb":4096,"devices":{"loop0":{"size":"1.0 GB"}}}
        if name:facts["devices"][name]={"size":"40.00 GB"}
        html=template.render(ansible_facts=facts,apache_disk_name="")
        assert "192.0.2.10" in html and "4096" in html
        assert ("40.00 GB" if name else "Не определён") in html
        if name:assert f"Первый диск ({name})" in html
        cases.append({"device":name,"rendered":True})
        if name=="vda":
            banner='<aside style="padding:20px;background:#fff0c7">УЧЕБНЫЙ ПРИМЕР: локальный рендер Jinja с условными facts. Не страница реальной VM.</aside>'
            (ROOT/"examples").mkdir(exist_ok=True)
            (ROOT/"examples/apache-demo.html").write_text(html.replace("<body>","<body>"+banner))
    report={"checked_on":"2026-10-27","scope":"Local Mac syntax-check and synthetic-facts rendering only; no SSH, VM or Linux changes","ansible":version,"syntax_checks":records,"yaml_files":len(yaml_files),"jinja_cases":cases,"restart_notify_only_from_config":True,"forbidden_shell_command_modules_absent":True}
    (ROOT/"evidence/local-checks.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"syntax_checks":len(records),"jinja_cases":len(cases),"passed":True,"scope":report["scope"]},ensure_ascii=False))

if __name__=="__main__":
    main()
