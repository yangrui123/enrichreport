#! /usr/bin/env Rscript

library(clusterProfiler)
library(org.Hs.eg.db)

args = commandArgs(T)
filename = args[1]
prefix = args[2]
dt = read.table(filename, sep='\t', header=T, fill=TRUE)
x = bitr(dt$Gene, fromType="SYMBOL", toType="ENTREZID", OrgDb="org.Hs.eg.db")
write.csv(x, paste(prefix,"gene_id.csv",sep='.'), row.names=FALSE)

# GO enrich analysis
#
# All
ego_all = enrichGO(gene = x$ENTREZID, OrgDb = org.Hs.eg.db,ont = "CC",pAdjustMethod = 'BH',pvalueCutoff = 1.0,qvalueCutoff = 1.0)
if(dim(as.data.frame(ego_all))[1] > 0){
    write.csv(ego_all, paste(prefix,"go.CC.enrich.all.csv",sep='.'), row.names=FALSE)
}

ego_all = enrichGO(gene = x$ENTREZID, OrgDb = org.Hs.eg.db,ont = "MF",pAdjustMethod = 'BH',pvalueCutoff = 1.0,qvalueCutoff = 1.0)
if(dim(as.data.frame(ego_all))[1] > 0){
    write.csv(ego_all, paste(prefix,"go.MF.enrich.all.csv",sep='.'), row.names=FALSE)
}

ego_all = enrichGO(gene = x$ENTREZID, OrgDb = org.Hs.eg.db,ont = "BP",pAdjustMethod = 'BH',pvalueCutoff = 1.0,qvalueCutoff = 1.0)
if(dim(as.data.frame(ego_all))[1] > 0){
    write.csv(ego_all, paste(prefix,"go.BP.enrich.all.csv",sep='.'), row.names=FALSE)
}

# CC
ego = enrichGO(gene = x$ENTREZIP, OrgDb = org.Hs.eg.db,ont = "CC",pAdjustMethod = 'BH',pvalueCutoff = 0.05,qvalueCutoff = 0.1)
# network
if(dim(as.data.frame(ego))[1] > 0){
    #
    write.csv(ego, paste(prefix,"go.CC.enrich.csv",sep='.'), row.names=FALSE)
    #
    pdf(paste(prefix,"go.CC.net.enrich.pdf",sep='.'))
    print(plotGOgraph(ego))
    dev.off()
    # dotplot
    pdf(paste(prefix,"go.CC.dot.enrich.pdf",sep='.'))
    print(dotplot(ego))
    dev.off()
}
# MF
ego = enrichGO(gene = x$ENTREZID,OrgDb = org.Hs.eg.db,ont = 'MF',pAdjustMethod = 'BH',pvalueCutoff = 0.05,qvalueCutoff = 0.1)
if(dim(as.data.frame(ego))[1] > 0){
    #
    write.csv(ego, paste(prefix,"go.MF.enrich.csv",sep='.'), row.names=FALSE)
    #
    pdf(paste(prefix,"go.MF.net.enrich.pdf",sep='.'))
    print(plotGOgraph(ego))
    dev.off()
    # dotplot
    pdf(paste(prefix,"go.MF.dot.enrich.pdf",sep='.'))
    print(dotplot(ego))
    dev.off()
}
#BP
ego = enrichGO(gene = x$ENTREZID,OrgDb = org.Hs.eg.db,ont = 'BP',pAdjustMethod = 'BH',pvalueCutoff = 0.05,qvalueCutoff = 0.1)
if(dim(as.data.frame(ego))[1] > 0){
    write.csv(ego, paste(prefix,"go.BP.enrich.csv",sep='.'), row.names=FALSE)
    pdf(paste(prefix,"go.BP.net.enrich.pdf",sep='.'))
    print(plotGOgraph(ego))
    dev.off()
    # dotplot
    pdf(paste(prefix,"go.BP.dot.enrich.pdf",sep='.'))
    print(dotplot(ego))
    dev.off()
}


