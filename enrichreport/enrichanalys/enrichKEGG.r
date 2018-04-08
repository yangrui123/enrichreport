#! /usr/bin/env Rscript
library(clusterProfiler)
library(org.Hs.eg.db)

args = commandArgs(T)
filename = args[1]
prefix = args[2]
dt = read.table(filename, sep='\t', header=T, fill=TRUE)
x = bitr(dt$Gene, fromType="SYMBOL", toType="ENTREZID", OrgDb="org.Hs.eg.db")
# KEGG enrich analysis
kk_all = enrichMKEGG(x$ENTREZID, organism = 'hsa',pvalueCutoff = 1.0,pAdjustMethod = 'BH',qvalueCutoff = 1.0)
row_nums = dim(as.data.frame(kk_all))[1]
if(row_nums > 0){
    write.csv(kk_all, paste(prefix, 'KEGG.enrich.all.csv', sep='.'), row.names=FALSE)
}

kk = enrichMKEGG(x$ENTREZID, organism = 'hsa',pvalueCutoff = 0.05,pAdjustMethod = 'BH',qvalueCutoff = 0.1)
row_nums = dim(as.data.frame(kk))[1]
if(row_nums > 0){
    write.csv(kk, paste(prefix, 'KEGG.enrich.csv', sep='.'), row.names=FALSE)
    pdf(paste(prefix,"KEGG.enrich.pdf",sep='.'))
    print(dotplot(kk,showCategory=20))
    dev.off()
}
