#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 00:19:22 2020

@author: usingh
"""

import sys
import os
import argparse
from pyrpipe import pyrpipe_utils as pu
from pyrpipe import reports
from pyrpipe import test_sratools,buildtools



def report():
    """
    Entry point for report subcommand

    Returns
    -------
    None.

    """
    
    parser = argparse.ArgumentParser(
   
            description='pyrpipe diagnostic utility\nGenerate analysis report.',
            
            usage='''pyrpipe_diagnostic report [<args>] <logfile>
                    
                    ''')    
    parser.add_argument('-o', help='out file \ndefault: same as input logfile',action="store")
    parser.add_argument('-s','--summary', help='Print quick summary and exit',default=False,dest='summary', action='store_true')
    parser.add_argument('-e', help='report output type: [md,pdf,html] \ndefault: pdf',default='pdf',action="store")
    parser.add_argument('-c',help='Report options [(f)ull,fa(i)l,(p)ass]\ndefault: f',default='f',action="store")
    parser.add_argument('-v',help='verbose',action="store_true")
    parser.add_argument('logfile', help='The log file generated by pyrpipe',action="store")
    args = parser.parse_args(sys.argv[2:])
    
    logFile=args.logfile
    envLog=reports.checkEnvLog(logFile)    
    #parse args
    if args.summary:
        #print summary
        reports.generate_summary(logFile,envLog,coverage='a')
        return
    
    vFlag=args.v
    if vFlag:
        print("Generating report")
        
        
    outFile=""
    if args.o is None:
        outFile=pu.get_file_basename(args.logfile)
    else:
        outFile=args.o
    outFile+='.'+args.e
    
    if args.e in ['pdf','html','md']:
        htmlReport=reports.generateHTMLReport('simpleDiv.html',logFile,envLog,coverage=args.c)
        if args.e=='pdf':
            reports.writeHtmlToPdf(htmlReport,outFile)
        elif args.e=='html':
            reports.writeHtml(htmlReport,outFile)
        elif args.e == 'md':
            reports.writeHtmlToMarkdown(htmlReport,outFile)
    else:
        pu.print_boldred("unknown extension:"+args.e+". Exiting")
    
    
    
def shell():
    """
    Entry point for shell command

    Returns
    -------
    None.

    """
    parser = argparse.ArgumentParser(
   
            description='pyrpipe diagnostic utility\nGenerate shell script.',
            
            usage='''pyrpipe_diagnostic report [<args>] <logfile>
                    
                    ''')    
    parser.add_argument('-o', help='out file \ndefault: same as input logfile',action="store")
    parser.add_argument('-c',help='Dump command options [(a)ll,fa(i)l,(p)ass]\ndefault: a',default='a',action="store")
    parser.add_argument('-v',help='verbose',action="store_true")
    parser.add_argument('-f',help='Filter by programs. Provide a comma-separated list e.g., prefetch,STAR,bowtie2 \ndefault None')
    parser.add_argument('logfile', help='The log file generated by pyrpipe',action="store")
    args = parser.parse_args(sys.argv[2:])
    
    logFile=args.logfile  
    #parse args
    vFlag=args.v
    if vFlag:
        print("Generating report")
    outFile=""
    if args.o is None:
        outFile=pu.get_file_basename(logFile)
    else:
        outFile=args.o
    outFile+='.sh'
    
    filters=[]
    if args.f is not None:
        filters= args.f.split(',')
    
    reports.generateBashScript(logFile,outFile,filters,args.c)
    

def benchmark():
    """
    Entry point for benchmark subcommand

    Returns
    -------
    None.

    """
    parser = argparse.ArgumentParser(
   
            description='pyrpipe diagnostic utility\nGenerate benchmark report.',
            
            usage='''pyrpipe_diagnostic report [<args>] <logfile>
                    
                    ''')    
    parser.add_argument('-o', help='out file \ndefault: same as input logfile',action="store")
    parser.add_argument('-e', help='report output type: [MD,PDF,HTML] \ndefault: PDF',default='PDF',action="store")
    parser.add_argument('-v',help='verbose',action="store_true")
    parser.add_argument('-f',help='Filter by programs. Provide a comma-separated list e.g., prefetch,STAR,bowtie2 \ndefault None')
    parser.add_argument('-t',help='Temporary directory. \ndefault ./tmp',action="store")
    parser.add_argument('logfile', help='The log file generated by pyrpipe',action="store")
    args = parser.parse_args(sys.argv[2:])
    
    logFile=args.logfile
    envLog=reports.checkEnvLog(logFile)    
    #parse args
    vFlag=args.v
    if vFlag:
        print("Generating benchmarks")
    outFile=""
    if args.o is None:
        outFile=pu.get_file_basename(args.logfile)
    else:
        outFile=args.o
    outFile+='.'+args.e
    
    filters=[]
    if args.f is not None:
        filters= args.f.split(',')
    #create temp dir
    tempDir=""
    if args.t is not None:
        tempDir= args.t
    else:
        tempDir=os.path.join(os.getcwd(),"tmp")
    #create tmp dir
    if not pu.check_paths_exist(tempDir):
        pu.mkdir(tempDir)
        
    reports.generateBenchmarkReport(logFile,envLog,filters,tempDir,outFile=outFile,verbose=args.v)

    
def multiqc():
    """
    Entry point for multiqc subcommand

    Returns
    -------
    None.

    """
    
    parser = argparse.ArgumentParser(
   
            description='pyrpipe diagnostic utility\nGenerate report with multiqc.',
            
            usage='''pyrpipe_diagnostic multiqc [<args>] <logfile>
                    
                    ''')    
    parser.add_argument('-o', help='out directory \ndefault: <./>',action="store")
    parser.add_argument('-c',help='Dump command options [(a)ll,fa(i)l,(p)ass]\ndefault: a',default='a',action="store")
    parser.add_argument('-v',help='verbose',action="store_true")
    parser.add_argument('-f',help='Filter by programs. Provide a comma-separated list e.g., prefetch,STAR,bowtie2 \ndefault None')
    parser.add_argument('-t',help='Temporary directory. \ndefault ./tmp',action="store")
    parser.add_argument('-r',help='Remove stdout files after processing. \ndefault ./tmp',action="store_true")
    parser.add_argument('logfile', help='The log file generated by pyrpipe or root directory to search available logs',action="store")
    args = parser.parse_args(sys.argv[2:])
    
    logFile=args.logfile
    
    #parse args
    vFlag=args.v
    if vFlag:
        print("Generating MutiQC report")
    outDir=""
    if args.o is None:
        outDir=os.getcwd()
    else:
        outDir=args.o
    
    
    filters=[]
    if args.f is not None:
        filters= args.f.split(',')
    
    #create temp dir
    tempDir=""
    if args.t is not None:
        tempDir= args.t
    else:
        tempDir=os.path.join(os.getcwd(),"tmp")
    #create tmp dir
    if not pu.check_paths_exist(tempDir):
        pu.mkdir(tempDir) 
    
    #run multiqc
    #if log file is used
    if pu.check_files_exist(logFile):
        reports.generate_multiqc_from_log(logFile,filters,tempDir,outDir=outDir,coverage=args.c,verbose=args.v,cleanup=args.r)
    else:
        reports.generate_multiqc(logFile,tempDir,outDir=outDir,coverage=args.c,verbose=args.v,cleanup=args.r)

def testsra():
    test_sratools.runtest()
    
def installtools():
    buildtools.build_tools()
    
    
def main():
    ##Start parsing
    subcommands=['report','shell','benchmark','multiqc','test','build-tools']
    parser = argparse.ArgumentParser(
                
                description='pyrpipe diagnostic utility',
                
                usage='''pyrpipe_diagnostic <command> [<args>] <logfile>
                        The commands are:
                        report     Generate analysis report
                        shell      Generate all commands to shell (bash) script
                        benchmark Generate bemchmarks
                        multiqc Generate HTML report using multiqc
                        test Test if NCBI-SRA-Tools is working with pyrpipe
                        build-tools Install the tools required by pyrpipe via  bioconda. pyrpipe must be installed under conda environment.
                        
                        ''')
    parser.add_argument('command', help='Subcommand to run report, shell,benchmark,multiqc,test')
    
    
    #parse first and last argument as subcommand and logfile 
    args = parser.parse_args(sys.argv[1:2])
    if args.command not in subcommands:
        print ('Unrecognized command')
        parser.print_help()
        exit(1)
    
    if args.command == 'report':
        report()
    elif args.command == 'shell':
        shell()
    elif args.command == 'benchmark':
        benchmark()
    elif args.command == 'multiqc':
        multiqc()
    elif args.command == 'test':
        testsra()
    elif args.command == 'build-tools':
        installtools()
        
    
