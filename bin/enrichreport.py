#!/usr/bin/env python
import sys
import os
dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"../")
sys.path.insert(0,dirpath)
from enrichreport.enrichanalys.enrich import enrich
from enrichreport.arranger.arrange import arrange
from enrichreport.reporter.report import report 
import yaml
from jbiot import jbiotWorker

# entrypoint function
def enrichreport(params):

    # call worker1
    #
    enrich_res = enrich(params) 

    # call arrange
    #
    arr_res = arrange(enrich_res)

    # call report
    #
    outdict = report(arr_res)
    
    return outdict

# mulit-omics platform
class enrichreportWorker(jbiotWorker):
    def handle_task(self,key,params):
        self.execute(enrichreport,params)


# main function
def main(yml):
    #1. read yaml 
    out_dict = enrichreport({"yaml": yml})
    

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
