#! /usr/bin/env python
# coding = utf-8

import os
import json
import yaml
import xlwt
import csv

try:
    from config import tsv2xls
except:
    tsv2xls = 'tsv2xls.py'

from jbiot import yamladd


def arrange(arr_dict, yamlfile):
    
    func_pdfs_report = files_report(arr_dict['func_pdfs'])
    go_dot_pdfs_report = files_report(arr_dict['go_dot_pdfs'])
    go_net_pdfs_report = files_report(arr_dict['go_net_pdfs'])
    kegg_pdfs_report = files_report(arr_dict['kegg_pdfs'])

    func_xls_report = transfor(arr_dict['func_csvs'])
    go_xls_report = transfor(arr_dict['go_csvs'])
    go_xls_all = transfor(arr_dict['go_csvs_all'])
    kegg_xls_report = transfor(arr_dict['kegg_csvs'])
    kegg_xls_all = transfor(arr_dict['kegg_csvs_all'])
    
    if len(kegg_pdfs_report) == 0:
        kegg_pdf_report = ''
    else:
        kegg_pdf_report = kegg_pdfs_report[0]

    out_dict = {"func_pdfs_report": func_pdfs_report, "go_dot_pdfs_report": go_dot_pdfs_report, "go_net_pdfs_report": go_net_pdfs_report, \
                "kegg_pdf_report": kegg_pdf_report, "func_xls_report": func_xls_report, "go_xls_report": go_xls_report, "kegg_xls_report": kegg_xls_report}
    
    # report paramters
    #
    res = yamladd(yamlfile, out_dict)
    
    return res

def files_report(files):
    outs = {}
    for item in files:
        if os.path.exists(item):
            prefix = item.split('.')[0]
            try:
                outs[prefix].append(item)
            except KeyError:
                outs[prefix] = [item]
    out = [] 
    for key, value in outs.items():
        if len(value) == 3:
            out = value
            break
        elif len(value) == 2:
            out = value
            break
        elif len(value) == 1:
            out = value
            break
    return out


def readgeneid(filename):
    id_dict = {}
    with open(filename, 'r') as f:
        head = f.readline().strip().split(',')
        sidx, idx = head.index('"SYMBOL"'), head.index('"ENTREZID"')
        for line in f:
            li = line.strip().split(',')
            symbol, eid = li[sidx], li[idx]
            eid = eid.strip('"')
            id_dict[eid] = symbol.strip('"')
    return id_dict


def transfor(files):
    outs = []
    for item in files:
        if os.path.exists(item):
            prefix = item.split('.')[0]
            if 'func' in item:
                xlsfile = func2xls(item)
            else:
                id_dict = readgeneid(prefix+'.gene_id.csv')
                xlsfile = csv2xls(item, id_dict)
            outs.append(xlsfile)
    try:
        out = outs[0]
    except:
        out = ''
    return out


def func2xls(filename):
    output = filename.rstrip('csv') + 'xls'
    fwp = xlwt.Workbook()
    sheet1 = fwp.add_sheet('sheet1', cell_overwrite_ok=True)
    fp = open(filename, 'r')
    csv_file = csv.reader(fp)
    for i, line in enumerate(csv_file):
        for j in range(len(line)):
            sheet1.write(i, j, line[j])
    fwp.save(output)
    return output

            
def csv2xls(filename, id_dict):
    output = filename.rstrip('csv') + 'xls'
    fwp = xlwt.Workbook()
    sheet1 = fwp.add_sheet('sheet1', cell_overwrite_ok=True)
    fp = open(filename, 'r')
    csv_file = csv.reader(fp)
    for i, line in enumerate(csv_file):
        if i == 0:
            head = line
            idx = head.index('geneID')
            for j in range(len(head)):
                sheet1.write(i, j, head[j])
            sheet1.write(i, j+1, "SYMBOL")
        else:
            gid = line[idx].strip('"')
            if gid == "":
                symbols = ""
            else:
                ids = gid.split('/')
                symbols = '/'.join([id_dict[item] for item in ids])
            for j in range(len(line)):
                sheet1.write(i, j, line[j])
            sheet1.write(i, j+1, symbols)
    fwp.save(output)

    return output


if __name__ == '__main__':
    import sys
    yamlfile = sys.argv[1]
    fp = open(yamlfile)
    parms = yaml.load(fp.read())
    fp.close()
    arrange(parms, yamlfile)
