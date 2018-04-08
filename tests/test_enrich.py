#! /usr/bin/env python
import sys,os
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cwd,'../'))

from enrichreport.enrichanalys.enrich import enrich

parms = {'yaml': 'parms.yaml'}

def test_enrich():
    res = enrich(parms)
    assert res['yaml']


if __name__ == '__main__':
    test_enrich()
