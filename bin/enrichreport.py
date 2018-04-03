#!/usr/bin/env python
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from enrichreport.arranger.arrange import arrange
from enrichreport.reporter.report import report 
import yaml
from jbiot import jbiotWorker

# entrypoint function
def enrichreport(params):

    # call worker1
    indict = {}
    pass 

    # call worker2
    indict = {}
    pass 

    # call arrange
    indict = {}
    outdict = arrange(indict)

    # call report
    indict = {}
    indict["render_json"] = outdict["render_json"]
    outdict = report(indict)
    # key and value need to write into main yaml
    output = {}
    
    return output

# mulit-omics platform
class enrichreportWorker(jbiotWorker):
    def handle_task(self,key,params):
        self.execute(enrichreport,params)


# main function
def main(yml):
    #1. read yaml 
    ymlstr = open(yml).read()
    params = yaml.load(ymlstr)
    outputdict = enrichreport(params)
    
    #2. write yaml
    ystr = yaml.dump(outputdict,default_flow_style=False)
    fp = open(yml,"w")
    fp.write(ymlstr)
    fp.write(ystr)
    fp.close()

if __name__ == "__main__":
    from docopt import docopt
    usage = """
    Usage:
       enrichreport.py -c <params> 

    Options:
        -c,--conf <params>    params in yaml format.

    """
    args = docopt(usage)
    yml = args["--conf"]
    main(yml)
