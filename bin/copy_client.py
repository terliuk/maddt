#! /usr/bin/env python

# FIXME: add gpl...
# This software is distrubuted under the terms of the GPL
#

import multiprocessing as mult

from optparse import OptionParser
from time import sleep,time

import sys
import logging
import os


# modify our pythonpath
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maddt.settings")

import gridcopy.gridftpcopy as copy
cfg = copy.configure()


# configure logging
LOG_FORMAT='%(asctime)s:%(levelname)s:%(process)d:%(module)s:%(funcName)s:%(lineno)d:%(message)s'
logging.basicConfig(format=LOG_FORMAT,level=cfg.getint("logging","loglevel"))
 
import warnings


def safe_copy(files_to_copy):
    """
    Catch Non-picklable Exceptions during copy as they might
    cause multiprocessing.Pool.join() to hang
    """



    #try:
    copy.delete_obsolete_files() # set as default
    return copy.copy(files_to_copy,cfg)
    #except Exception as e:
        #logging.warn('Catching copy error! %s' %e.__repr__() )    
        #return None

def main(cfg):
   
    files_to_copy = [True] 
    while len(files_to_copy) > 0:     
        
        jobstarttime = time()  
        copy.get_afs_token()
        files_to_copy = copy.get_files(cfg)
        # DEBUG
        #for index,i in enumerate(files_to_copy):
        #    print index,i.name,i.transferstate

        sys.stdout.flush()
        
        results = []


        assert(opts.jobs > 0)

        if opts.jobs == 1:
            # no need for pool
            results.append(safe_copy(files_to_copy))
       
        else: 
            def manager(result):
                results.append(result)

            ## slice our list in x files per job
            maxfiles = cfg.getint("job_management","files_per_job")
            slices   = len(files_to_copy)/maxfiles + 1

            workload   = [sli for sli in copy.list_slicer(files_to_copy,slices) if len(sli) > 0]
            workforce  = mult.Pool(int(opts.jobs))#,None,None,1) # set number of task per worker to 1, then it is deleted and a new worker si started

            # Try different methods of Pool
            #for work in workload:
            #   workforce.apply_async(safe_copy,args=(work,cfg),callback = manager)

            # next try
            iter_res = workforce.imap(safe_copy,workload,1)            
            workforce.close()
            logging.info("Workforce starts to work...")

            casualties = 0
            for index in range(len(workload)):
                if casualties > 1:
                    # kill also the rest!
                    logging.warn("Killing all pool workes!")
                    workforce.terminate()
                    break
                try:
                    results.append(iter_res.next(timeout=300))        
                except mult.TimeoutError:
                    casualties += 1
                logging.warn("A worker died! We have %i casualties Continuing..." %casualties) 

        #workforce.join()
        
        # global monitoring
        passed_time  = time() - jobstarttime 
        copied_data  = 0
        copied_files = 0


        for jobresult in results:
            if jobresult is not None:
                copied_data  += jobresult["datavolume"]
                copied_files += jobresult["copied_files"]
        
        speed = (copied_data/passed_time)/1000000 # MB/s
        logging.info("Average transferspeed %4.2f MB/s " %(speed) )
        logging.info("Copy requested for %i files, and %i files were actually copied" %(len(files_to_copy),copied_files))
        logging.info("Elapsed time %4.2f" %passed_time) 
   
        # DEBUG
        #break

if __name__ == "__main__":
    

    usage  = """python copy_client OPTIONS
             This script is dedicated for an automated
             datatransfer to backup L2 and PoleFilter data
             from Madison to Tier1 datacenter at DESY (Zeuthen)
             """

    
    parser = OptionParser(usage=usage)
    settings = parser.add_option_group("settings")
    settings.add_option("-C","--configfile",dest="configfile",default=None,help="specify a configfile")
    settings.add_option("-j","--jobs",dest="jobs",default=5,help="number of jobs",type=int)
    opts,args = parser.parse_args()

    #mult.log_to_stderr(logging.DEBUG)
    
    if opts.configfile is None:
        cfg = copy.configure()
    else:
        cfg = copy.configure(configfile=opts.configfile)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore",RuntimeWarning)
        main(cfg)    

