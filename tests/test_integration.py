#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 10:27:44 2020

@author: usingh

Test various pyrpipe modules used with each other
"""

from pyrpipe import sra,qc,mapping,assembly,quant,tools
from testingEnvironment import testSpecs
import os


testVars=testSpecs()
fq1=testVars.fq1
fq2=testVars.fq2
rRNAfasta=testVars.rRNAfa

#srr='ERR3770564' #single end arabidopsis data
#srr='SRR978414' #small a thal paired end data
srr='SRR4113368'
workingDir=testVars.testDir




#create objects
bbdOpts={"ktrim":"r","k":"23","mink":"11","qtrim":"'rl'","trimq":"10","ref":testVars.bbdukAdapters}
bbdOb=qc.BBmap(None,**bbdOpts)
tg=qc.Trimgalore()
bt=mapping.Bowtie2(index=testVars.testDir+"/btIndex",genome=testVars.genome)
hsOpts={"--dta-cufflinks":"","-p":"8"}
hs=mapping.Hisat2(index=testVars.testDir+"/hisatindex",genome=testVars.genome,**hsOpts)
star=mapping.Star(index=os.path.join(testVars.testDir,"starIndex"),genome=testVars.genome)
samOb=tools.Samtools()
stie=assembly.Stringtie()
cl=assembly.Cufflinks()
kl=quant.Kallisto(index=testVars.testDir+"/kallistoIndex/kalIndex",transcriptome=testVars.cdna)
sl=quant.Salmon(index=testVars.testDir+"/salmonIndex/salIndex",transcriptome=testVars.cdna_big)

#sra ob 
sraOb=sra.SRA(srr,workingDir)
st=sraOb.fastq_exists()
assert st==True,"fasterq-dump failed"


def test_pipeline1():    
    st=sraOb.trim(bbdOb).align(hs).assemble(stie).quant(kl)   
    assert st!=None,"pipeline 1 failed"
    
def test_pipeline2():    
    st=sraOb.trim(tg).align(hs).assemble(stie).quant(kl)   
    assert st!=None,"pipeline 1 failed"

  
def test_pipeline3():    
    st=sraOb.trim(tg).align(star).assemble(stie).quant(sl)   
    assert st!=None,"pipeline 1 failed"

    
def test_pipeline4():    
    st=sraOb.quant(sl).quant(kl).align(star)
    assert st!=None,"pipeline 1 failed"

def test_pipeline5():    
    st=sraOb.quant(sl).quant(kl).align(bt).assemble(cl).assemble(stie)
    assert st!=None,"pipeline 1 failed"
    
    
    
