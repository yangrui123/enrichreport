import sys,os
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cwd,'../'))

from enrichreport.reporter.report import report


def test_report():
    report({"yaml": "parms.yaml"})


if __name__ == '__main__':
    test_report()
