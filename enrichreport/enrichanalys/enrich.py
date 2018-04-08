#! /usr/bin/env python

import config

from jbiot import log
from jbiot import jbiotWorker
from jbiot import yamladd
import sys,os
import yaml

cwd = os.path.dirname(os.path.abspath(__file__))

funcAnnoGO = os.path.join(cwd, 'funcAnnoGO.r')
if not os.path.exists(funcAnnoGO):
    funcAnnoGO = "/opt/funcAnnoGO.r"

enrichGO = os.path.join(cwd, 'enrichGO.r')
if not os.path.exists(enrichGO):
    enrichGO = "/opt/enrichGO.r"

enrichKEGG = os.path.join(cwd, 'enrichKEGG.r') 
if not os.path.exists(enrichKEGG):
    enrichKEGG = "/opt/enrichKEGG.r"

csv2xls = os.path.join(cwd, 'csv2xls.py')
if not os.path.exists(csv2xls):
    csv2xls = "/opt/csv2xls.py"


def enrich(parms):
    '''Gene GO functional annotation, GO enrichment and KEGG enrichment

    Args:
        parms (dict) : which has the following keys::
            
            {
                yaml : a yaml file including parms for gene enrich analysis
            }

    Returns:
        dict : ``{"yaml": yamlfile for arrange and report}``
    '''
    
    yaml_file = parms["yaml"]
    fp = open(yaml_file)
    enrich_dict = yaml.load(fp.read())
    fp.close()
    
    files = enrich_dict['enrichFiles']
    func_pdfs, func_csvs, func_xls = [], [], []
    go_dot_pdfs, go_net_pdfs, go_csvs, go_csvs_all, go_xls, go_xls_all = [], [], [], [], [], []
    kegg_pdfs, kegg_csvs, kegg_csvs_all, kegg_xls, kegg_xls_all = [], [], [], [], []      
    id_files = []

    for prefix, enrichFile in files.items():
        # check file
        #
        with open(enrichFile, 'r') as f:
            head = f.readline().split('\t')
            try: 
                gidx = head.index("Gene")
            except ValueError:
                print("\n\nInput file: {} need the head include 'Gene'.\n\n".format(enrichFile))
            
        # functation annotation
        #
        cmd = "%s %s %s"%(funcAnnoGO, enrichFile, prefix)
        log.run('func annotation', cmd, i=[enrichFile])
        
        # GO enrich analysis
        #
        cmd = "%s %s %s"%(enrichGO, enrichFile, prefix)
        log.run('GO enrich analysis', cmd)
        
        # KEGG enrich analysis
        #
        cmd = "%s %s %s"%(enrichKEGG, enrichFile, prefix)
        log.run('KEGG enrich analysis', cmd)
        
        for item in ['CC', 'BP', 'MF']:
            func_pdfs.append('{prefix}.go.{item}.bar.func.pdf'.format(prefix = prefix, item = item))
            func_csvs.append('{prefix}.go.{item}.func.csv'.format(prefix = prefix, item = item))
            func_xls.append('{prefix}.go.{item}.func.xls'.format(prefix = prefix, item = item))
        
            go_dot_pdfs.append('{prefix}.go.{item}.dot.enrich.pdf'.format(prefix = prefix, item = item))

            go_net_pdfs.append('{prefix}.go.{item}.net.enrich.pdf'.format(prefix = prefix, item = item))
            
            go_csvs.append('{prefix}.go.{item}.enrich.csv'.format(prefix = prefix, item = item))
            go_csvs_all.append('{prefix}.go.{item}.enrich.all.csv'.format(prefix = prefix, item = item))
            go_xls.append('{prefix}.go.{item}.enrich.xls'.format(prefix = prefix, item = item))
            go_xls_all.append('{prefix}.go.{item}.enrich.all.xls'.format(prefix = prefix, item = item))

        id_files.append("{}.gene_id.csv".format(prefix))
        kegg_pdfs.append('{}.KEGG.enrich.pdf'.format(prefix))
        kegg_csvs.append('{}.KEGG.enrich.csv'.format(prefix))  
        kegg_csvs_all.append('{}.KEGG.enrich.all.csv'.format(prefix))   
        kegg_xls.append('{}.KEGG.enrich.xls'.format(prefix))   
        kegg_xls_all.append('{}.KEGG.enrich.all.xls'.format(prefix))   

    out_dict = {'func_pdfs':func_pdfs, 'go_dot_pdfs':go_dot_pdfs, 'go_net_pdfs': go_net_pdfs, 'kegg_pdfs':kegg_pdfs, \
            'func_csvs': func_csvs, 'func_xls': func_xls, 'go_csvs': go_csvs, 'go_xls': go_xls, 'go_csvs_all': go_csvs_all, 'go_xls_all': go_xls_all, 'kegg_csvs': kegg_csvs , \
            'kegg_csvs_all': kegg_csvs_all, 'kegg_xls': kegg_xls, 'kegg_xls_all': kegg_xls_all}
        
    res = yamladd(yaml_file, out_dict) 
    
    # csv2xls
    #
    cmd = "{csv2xls} {yamlfile}".format(csv2xls=csv2xls, yamlfile=yaml_file)
    log.run('csv2xls', cmd)
        
    return res



class EnrichWorker(jbiotWorker):
    def handle_task(self, key, params):
        self.execMyfunc(enrich, params)

