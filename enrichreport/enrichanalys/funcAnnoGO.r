#! /usr/bin/env Rscript

library(clusterProfiler)
library(org.Hs.eg.db)

args = commandArgs(T)
filename = args[1]
prefix = args[2]
dt = read.table(filename, sep='\t', header=T, fill=TRUE)
x = bitr(dt$Gene, fromType="SYMBOL", toType="ENTREZID", OrgDb="org.Hs.eg.db")
# CC
ggo = groupGO(gene=x$ENTREZID, OrgDb=org.Hs.eg.db, ont = 'CC', level=3, readable=TRUE)
pdf(paste(prefix,"go.CC.bar.func.pdf",sep='.'))
if (typeof(ggo)!='NULL'){
    write.csv(ggo, paste(prefix, 'go.CC.func.csv', sep='.'), row.names=FALSE)
    print(barplot(ggo, drop=TRUE, showCategory=12))
    dev.off()
}
# MF
ggo = groupGO(gene=x$ENTREZID, OrgDb=org.Hs.eg.db, ont = 'MF', level=3, readable=TRUE)
if(typeof(ggo)!='NULL'){
    write.csv(ggo, paste(prefix, 'go.MF.func.csv', sep='.'), row.names=FALSE)
    pdf(paste(prefix,"go.MF.bar.func.pdf",sep='.'))
    print(barplot(ggo, drop=TRUE, showCategory=12))
    dev.off()
}
# BP
ggo = groupGO(gene=x$ENTREZID, OrgDb=org.Hs.eg.db, ont = 'BP', level=3, readable=TRUE)
if(typeof(ggo)!='NULL'){
    write.csv(ggo, paste(prefix, 'go.BP.func.csv', sep='.'), row.names=FALSE)
    pdf(paste(prefix,"go.BP.bar.func.pdf",sep='.'))
    print(barplot(ggo, drop=TRUE, showCategory=12))
    dev.off()
}


