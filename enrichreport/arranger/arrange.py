import os
import yaml

try:
    import config
except:
    pass

from jbiot import jbiotWorker
from jbiot import yamladd
from jbiot import log


def arrange(params):
    """ arrange outfile to destination directory and output json file for reporter

    Args:
        params (dict):  arrange input dict::

            {yaml : a yaml file including files to arrange}

    Returns:
        dict : output dict::

            {
                "yaml": yamlfile for report
            }

    """
    yamlfile = params['yaml']
    fp = open(yamlfile, 'r')
    indict = yaml.load(fp.read())
    fp.close()
    func_pdfs = indict['func_pdfs']
    func_xls = indict['func_xls']
    go_dot_pdfs = indict['go_dot_pdfs'] 
    go_net_pdfs = indict['go_net_pdfs']
    go_xls = indict['go_xls']
    go_xls_all = indict['go_xls_all']
    kegg_pdfs = indict['kegg_pdfs']
    kegg_xls = indict['kegg_xls']
    kegg_xls_all = indict['kegg_xls_all']

    funcDir = 'report/enrichAnalysis/GO/function'
    goDir = 'report/enrichAnalysis/GO/enrich'
    keggDir = 'report/enrichAnalysis/KEGG'
    
    log.move(func_pdfs, funcDir) 
    log.move(func_xls, funcDir)
    log.move(go_dot_pdfs, goDir)
    log.move(go_net_pdfs, goDir)
    log.move(go_xls, goDir)
    log.move(go_xls_all, goDir)
    log.move(kegg_xls, keggDir)
    log.move(kegg_pdfs, keggDir)
    log.move(kegg_xls_all, keggDir)
    return params


class enrichreportArranger(jbiotWorker):
    def handle_task(self,key,params):
        self.execMyfunc(arrange,params)
