import sys,os
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(cwd, '../'))

from enrichreport.arranger.arrange import arrange


def test_arrange():
    res = arrange({"yaml": "parms.yaml"})
    assert res["yaml"]


if __name__ == '__main__':
    test_arrange()
