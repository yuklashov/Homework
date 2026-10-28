"""Математическая модель, не HAProxy и не сетевой тест."""
from collections import Counter
import json

def schedule(weights, n):
    current = [0] * len(weights)
    out = []
    for _ in range(n):
        current = [x+w for x,w in zip(current,weights)]
        i = max(range(len(weights)), key=current.__getitem__)
        current[i] -= sum(weights)
        out.append('web'+str(i+1))
    return Counter(out)

def allowed(host):
    return host.lower().split(':',1)[0] == 'example.local'

if __name__ == '__main__':
    even = schedule([1,1], 20); weighted = schedule([2,3,4],90)
    assert even == {'web1':10,'web2':10}
    assert weighted == {'web1':20,'web2':30,'web3':40}
    assert allowed('example.local') and allowed('EXAMPLE.local:8081')
    assert not allowed('127.0.0.1:8081') and not allowed('example.local.evil')
    print(json.dumps({'mode':'учебная модель, не HAProxy','l4_model':dict(even),
                      'l7_model':dict(weighted),'host_acl_cases':4},ensure_ascii=False,indent=2))
