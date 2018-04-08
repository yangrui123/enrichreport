try:
    from config import render
    from config import md2html
except:
    render = "render.py"
    md2html = "md2html.py"
from jbiot import log
import os
from jbiot import jbiotWorker
from jbiot import get_template
from jbiot import yamladd
import yaml

def report(params):
    """ enrichreport to markdown file and html file

    Args: report input dict, key is `yaml`, value is yaml file path::

            "xx": path of xx.

    Returns:
        dict : key is `yaml`,value is yaml file path
    """
    # handle input
    yamlin = params["yaml"]
    indict = yaml.load(open(yamlin))

    enrichreportl = get_template("enrichreport")
    out = "enrichreport.md"
    cmd = "%s -t %s -j %s -o %s -y" % (render,enrichreportl,yamlin,out)
    log.run("render enrichreport template",cmd)
    
    cmd = "%s %s" % (md2html,out)
    log.run("md2html enrichreport ",cmd, o=["html.tgz"])
    outdict = {}
    outdict["enrichreport"] = out
    yamlout = yamladd(yamlin,outdict)
    yamlout["enrichreport_outdir"] = os.getcwd()
    return yamlout

class reportWorker(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(report,params)
