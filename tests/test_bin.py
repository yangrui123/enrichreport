import sys,os
cwd = os.path.dirname(os.path.abspath(__file__))
enrich_report = os.path.join(cwd, '../bin/enrichreport.py')

parms = '/home/testData/geneEnrich_report/data/parms.yaml'

def test_bin():
    cmd = 'python %s  -c %s'%(enrich_report, parms)
    os.system(cmd)

if __name__ == '__main__':
    test_bin()
