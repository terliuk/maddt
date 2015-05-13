from os import mkdir
from os.path import join

import os
import subprocess
import logging
import re
import time
import datetime
import numpy as n
import json
import sys
import psutil

from math import fsum
from ConfigParser import ConfigParser


def configure(configfile="/afs/ifh.de/user/s/stoessl/scratch/ic86_transfer/maddt/gridcopy/config.cfg"):
    """
    Read the configfile
    """
    parser = ConfigParser()
    parser.read(configfile)
    return parser

cfg = configure()

# configure logging
LOG_FORMAT='%(asctime)s:%(levelname)s:%(process)d:%(module)s:%(funcName)s:%(lineno)d:%(message)s'
LOG_FILENAME=time.ctime().replace(" ","_").replace(":","_") + "_maddt.log"
logfile = os.path.join(cfg.get("logging","logdir"),LOG_FILENAME)
logging.basicConfig(format=LOG_FORMAT,level=cfg.getint("logging","loglevel"),filename=logfile)
logging.captureWarnings(True)

try:
    from django.http import HttpResponse, HttpResponseRedirect 
    from django.shortcuts import render_to_response 
    from django.template import loader,Context,RequestContext 
    from django.core.context_processors import csrf
    from django.conf import settings
    from django.db import connections,transaction

    from models import Urlpath as Urlpath
    from copyjobs.models import CopyJob

except ImportError:
    logging.warn("Django not found, only reduced functionality available")

def check_voms_proxy():
    """
    Check if grid proxy is still valid
    """

    valid_proxy = False
    p1=subprocess.Popen(['voms-proxy-info'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2=subprocess.Popen(['grep', 'timeleft'], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        valid_time=p2.communicate()[0].splitlines()[0].split()[-1].split(":")
    except IndexError:
        logging.error('Can not issue proxy info command, recheck your voms proxy!')
        valid_time=[0]
        #sys.exit()

    valid_proxy = (True in [j > 0 for j in [int(i) for i in valid_time]])
    if valid_proxy:
        logging.debug("Voms-proxy checked, your grid proxy is still valid for %s hours and %s minutes"     % (valid_time[0],valid_time[1] ))
        return None

    else:
        logging.error("No valid voms-proxy found, program terminated!")
        sys.exit()

def write_access(path):
    """
    python os is not able to manage write access on dCache,
    so this is to be done manually
    """
    c_line = ['chmod', '-R', '--quiet' ,'775', path]
    grant_acces = subprocess.Popen(c_line)
    grant_acces.communicate()
    return None

def create_directories(files):
    """
    Create the necessary directories on Zeuthen dCache as the
    -cd flag of globus-url-copy does not work here
    """

    dirs_to_create = set([pth for pth in map(get_local_path,files) if not os.path.exists(pth)])
    #dirs_to_create = set([get_local_path(f) for f in files if not os.path.exists(get_local_path(f))])
    
    map(os.makedirs,dirs_to_create)
    map(write_access,dirs_to_create)
    if dirs_to_create:
        logging.info("Created directories %s" %(dirs_to_create.__repr__()))    


def compare_checksums(localcsum,remotecsum):
    """
    Compare two checksums (remote and local) for the task
    Dummy function, but more clever implementation should
    go here
    """
    if localcsum == remotecsum:
        return True
    else:
        return False



def get_afs_token():
    """
    Keep the job alive and get a new afs token,
    so that it can still write data to disk
    """
    p = subprocess.Popen(['kinit', '-R'])
    p.communicate()
    return


def get_files(cfg):
    """
    Query the i3filter db to get a bunch of files
    """

    def madison_file_getter(cfg):
        """
        Provided by Dipo
        """    
        import sys, os
        import datetime
        import cPickle
        import operator
        
        
        def SortnGroup(list_):
            #list_.sort(key=lambda x: x[3])
           
            #get unique entries using dict
            dList = {}
            for l in list_: dList[l[0]] = l[1:]
            sList = dList.items()
            #sort by queue_id
            #sList = sorted(dList.iteritems(), key=operator.itemgetter(1))
            sList = sorted(sList,key=lambda i: i[1][1])
            # then sort by run_id (may not be needed)
            sList = sorted(sList,key=lambda i: i[1][3])
            
            return sList
        
        cursor = connections["default"].cursor()    
        
        #sql = """select u.name, u.path, u.queue_id,u.urlpath_id, r.run_id,u.md5sum from i3filter.urlpath u
        #                           join i3filter.run r on r.queue_id=u.queue_id
        #                           where r.dataset_id=1861 and u.dataset_id=1861
        #                           and u.transferstate="WAITING" """
        #                           #order by r.run_id""")

        # new query, phone call on 13.6.14 with Dipo, checking for validated runs due to a change
        # with the .gaps.txt files, which are now tared.
        #SELECT u.name,u.queue_id,u.urlpath_id,u.transfertime,u.md5sum  FROM i3filter.urlpath u join i3filter.run r on r.queue_id=u.queue_id join i3filter.grl_snapshot_info g on r.run_id=g.run_id where u.dataset_id=1874 and r.dataset_id=1874 and u.transferstate="WAITING" and g.validated limit 1000
        sql = """SELECT u.name,u.path,u.queue_id,u.urlpath_id,u.transfertime,u.md5sum  FROM i3filter.urlpath u join i3filter.run r on r.queue_id=u.queue_id join i3filter.grl_snapshot_info g on r.run_id=g.run_id where u.dataset_id=%s and r.dataset_id=%s and u.transferstate="WAITING" and g.validated limit %s""" %(cfg.get("database_query","dataset_id"),cfg.get("database_query","dataset_id"),cfg.get("database_query","limit"))

        #sql = """select u.name, u.path, u.queue_id,u.urlpath_id, u.transfertime,u.md5sum from i3filter.urlpath u
        #                           where u.dataset_id=%s
        #                           and u.transferstate="WAITING" limit %s""" %(cfg.get("database_query","dataset_id"),cfg.get("database_query","limit"))
        #                           #order by r.run_id""")
        

        # 1870 for urlpath table  1861 for urlpath_test
        cursor.execute(sql)        
        dbInfo = cursor.fetchall()
        burnSampleL2 = [b for b in dbInfo if not b[4]%10 and b[0].find("PFFilt")<0]
        burnSamplePFFilt = [b for b in dbInfo if not b[4]%10 and b[0].find("PFFilt")>=0]
        OtherL2 = [b for b in dbInfo if b[4]%10 and b[0].find("PFFilt")<0 and b[0].find("GCD")<0]
        OtherPFFilt = [b for b in dbInfo if b[4]%10 and b[0].find("PFFilt")>=0]
        
        #print len(dbInfo)
        #print len(burnSamplePFFilt)
        #print len(burnSampleL2)
        #print len(OtherPFFilt)
        #print len(OtherL2) 
        Files2Copy = []
        # you can change the copying priority by changing the order that each group is added to Files2Copy
        # the group names are quite explicit
        if len(burnSampleL2): Files2Copy.extend(SortnGroup(burnSampleL2))
        if len(OtherL2): Files2Copy.extend(SortnGroup(OtherL2))
        if len(burnSamplePFFilt): Files2Copy.extend(SortnGroup(burnSamplePFFilt))
        if len(OtherPFFilt): Files2Copy.extend(SortnGroup(OtherPFFilt))
        
        logging.info("Retrieved %i files to copy from database" %len(Files2Copy))
        #for f in Files2Copy: print f
        return Files2Copy

    # get the models with help of the raw query
    # get them by id to be as fast as possible
    copy_request = madison_file_getter(cfg)
    #print len(copy_request)
    file_ids = [f[1][2] for f in copy_request]
    #print file_ids,"file ids"
    files_to_copy = Urlpath.objects.filter(pk__in=file_ids) #.filter(size__gt=10000000)
    average_file_size = 0
    if files_to_copy:
        average_file_size = fsum([f.size for f in files_to_copy])/(1000000*len(files_to_copy)) #MB
    
    logging.info("Will copy %i files with an average size of %4.2f MB" %(len(files_to_copy),average_file_size))
    return files_to_copy


def delete_obsolete_files(limit=None):
    """
    Check the DB for "DELETED" flags and delete the according files
    """

   
    deleted = Urlpath.objects.filter(transferstate__exact="DELETED")
    if limit is not None:

        assert isinstance(limit,int),"limit must be an integer!"
        deleted = deleted[:limit]

    logging.info("Got %i files with 'DELETED' flag" %len(deleted))

    confirmed_delete = 0
    if len(deleted):
        # individual delete to not 
        # 1) block the db
        # 2) keep 1:1 track to everything that should be deleted in the db
        for d in deleted:
            try:
                remove([d])
                d.transferstate = "DELETECONFIRMED"
                d.save(update_fields=["transferstate"])
                confirmed_delete += 1
            except Exception as e:
                logging.warn("Problems during deletion or update process for deleteconfirmed flag for file %s, exception %s" %(d.name.__repr__(), e.__repr__()))

        logging.info("Confirmed deltion of %i files" %confirmed_delete)

    return None




def write_filelist(files_to_copy,cfg):
    """
    Write an asci-filelist for the use with globus-url-copy
    """

    remote_host = cfg.get("madison_gsiftp","remote_gsiftp_host")
    local_host  = cfg.get('zeuthen_gsiftp','local_gsiftp_host')
    sources = [join(f.path,f.name).replace("file:",remote_host) for f in files_to_copy]
    
    destinations = [local_host + get_local_filename(f) for f in files_to_copy]

    tmpdir  = cfg.get('tmpdir','tmpdir')
    tmpfile = os.tempnam(tmpdir,"copy")

    with open(tmpfile,"w") as f:
        for source, dest in zip(sources,destinations):
            f.write(source + " " + dest + "\n")
    
    f.close()
    return tmpfile

def get_local_path(dbfile):
    """
    Converte a path in the datawarehouse to a path at DESY
    """
    year = get_year(dbfile)
    #path_prefix = dbfile.path.replace("file:","/lustre/fs6/group/i3/stoessl/urlpath_test")
    path_prefix = dbfile.path.replace("file:","/acs/icecube/icecube" + str(year)[2:])
    return path_prefix

def get_local_filename(dbfile):
    """
    Returns the DESY correspondend full path to a file
    """

    path_prefix = get_local_path(dbfile)
    return join(path_prefix,dbfile.name)

def get_year(dbfile):
    
    #FIXME: move the pattern to the configfile
    year = re.compile(r'.IceCube/(?P<year>\d+)/filtered.')
    year = year.search(dbfile.path)
    return year.groupdict()["year"]

def sanitize_local_files(files):
    """
    check if files exists and have a size larger than 0
    """
    
    def alive(f):
        name = get_local_filename(f)
        if os.path.exists(name):
            return os.path.getsize(name)
        else:
            return 0
   
    corruptfiles   = filter(lambda x: not alive(x), files)
    files          = filter(alive,files)
    #files          = list(files) # we need the .remove
    #map(files.remove,corruptfiles)
    return corruptfiles,files

def remove(files):
    """
    Delete a given set of files
    """

    filenames = map(get_local_filename,files)
    filenames = filter(os.path.exists,filenames)
    removed = []
    logging.debug("Will remove %i files" %len(filenames))
    if not filenames:
        return removed
    try:
        removed   = map(os.remove,filenames)
    except OSError:
        logging.warning("Can not remove files %s !" %(filenames.__repr__()))
    logging.info("Removed %i files" %len(removed))
    return removed

#@transaction.commit_manually
def local_csum_check(files,cfg,set_ignored=False):
    """
    Invoke DESY cluster to calculate checksums
    @param set_ignored: set IGNORED in i3filter db if file is corrupt
    """

    # sanitize files
    ghostfiles, existent_files = sanitize_local_files(files)
    # doing it here will prevent a calculation of a checksum
    # for a zero sized file and ensures that we are not
    # removing something which we have set the transferred 
    # flag already

    if not existent_files:
        logging.info("None of the requested files was found with a size larger than 0 on the filesystem!")
        return ghostfiles,existent_files #function should always return 2tuple

    elif ghostfiles:
        # removing the ghostfiles from the filelist
        logging.info("Deleting %i files with zero size, example file %s" %(len(ghostfiles),map(get_local_filename,ghostfiles)[0].__repr__()))
        remove(ghostfiles)
        files = existent_files    
    else:
        logging.info("No non-existent or zero-sized files found!")

    whoami = subprocess.Popen(['whoami'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=False).communicate()[0]
    logging.debug('Will submit as user %s' %whoami)

    qstat   = ['qstat','-u',whoami]
    wc      = ['wc','-l']

    p_qstat = subprocess.Popen(qstat,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p_wc    = subprocess.Popen(wc,stdout=subprocess.PIPE,stdin=p_qstat.stdout,stderr=subprocess.PIPE)
    p_qstat.communicate()

    max_farmjobs       = cfg.getint("job_management","max_jobs_on_local_cluster")
    user_jobs_on_farm  = p_wc.communicate()[0]
    logging.debug('Currently %s jobs on local cluster' %user_jobs_on_farm)

    # ensure that there are no more
    # than x jobs on the cluster
    while user_jobs_on_farm >= max_farmjobs:
        p_qstat = subprocess.Popen(qstat,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p_wc    = subprocess.Popen(wc,stdout=subprocess.PIPE,stdin=p_qstat.stdout,stderr=subprocess.PIPE)
        p_qstat.communicate()
        user_jobs_on_farm = p_wc.communicate()[0]
        logging.debug('Currently %s jobs on local cluster' %user_jobs_on_farm)
        user_jobs_on_farm = int(user_jobs_on_farm)
        time.sleep(10)

    csum_script    = cfg.get("job_management","local_csum_script")  
    checks_per_job = cfg.getint("job_management","max_csum_per_cluster_job") 

    tmpdir = cfg.get("tmpdir","tmpdir")
    active_jobs   = []
    finished_jobs = []
    md5sum_files  = []
    slice_files   = []
    slices = (len(files)/checks_per_job) +1
    for thisslice in list_slicer(files,slices):
        slice_files.append(thisslice)
        md5sumfile = os.tempnam(tmpdir,'check')
        md5sum_files.append(md5sumfile)
        submit_cmd = ['qsub',csum_script,md5sumfile] + [get_local_filename(f) for f in thisslice]
        # job submission
        jobid = subprocess.Popen(submit_cmd,stdout=subprocess.PIPE).communicate()[0]
        jobid = jobid.split()[2]
        active_jobs.append(jobid)

    job_on_farm = True
    while active_jobs:
        for jobid in active_jobs:
            #print active_jobs,jobid,finished_jobs
            qstat_cmd  = ['qstat','-j',jobid]
            job_on_farm = subprocess.Popen(qstat_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE).communicate()[0]
            if not job_on_farm:
                finished_jobs.append(jobid)
           
        for j in finished_jobs:
            try:        
                active_jobs.remove(j)
            except:
                pass 

        time.sleep(20) # do not overheat the master farm node with to many queries

    corrupt_files = []
    sane_files    = []
    errors = 0
    for md5sumfile,files_slice in zip(md5sum_files,slice_files):

        local_csum_file_pairs  = parse_md5sumfile(md5sumfile)
        remote_csum_file_pairs = [(get_local_filename(f),f.md5sum) for f in files_slice]
   
        for f in files_slice:
            try:
                compare_checksums(local_csum_file_pairs[get_local_filename(f)],format_csum(f.md5sum))
            except:
                print f.name
                print get_local_filename(f)
                print local_csum_file_pairs
                raise 
            if compare_checksums(local_csum_file_pairs[get_local_filename(f)],format_csum(f.md5sum)) :
                # a junction, because for GCD files there are many entries and
                # they neded to be updatedad at once

                # DEBUG
                #print f.name,f.transferstate,f.pk
                #x = Urlpath.objects.filter(pk__in=[f.pk])[0]
                #print x.name,x.transferstate,x.pk,"debug for database_error"
                if "GCD" in f.name:
                    representatives = Urlpath.objects.filter(md5sum=f.md5sum).exclude(transferstate__exact="TRANSFERRED")
                    logging.debug("Found %i representatives for file %s" %(len(representatives),f.name))
                    gcd_errors = 0
                    for r in representatives:
                        #print r.pk, r.md5sum,r.name,r.transferstate
                        r.transferstate = "TRANSFERRED"
                        try:
                            r.save(update_fields=["transferstate"])
                        except Exception as e:
                            logging.debug("Got exception (gcd) %s while updating file %s with id %i" %(e.__repr__(),r.name,r.pk))
                            gcd_errors += 1

                    if gcd_errors:
                        logging.debug("%i gcd errors occured during db-update" %gcd_errors)
                    logging.debug("Saving md5sum for file %s for %i representatives" %(f.name,len(representatives)))
                    sane_files.append(f)
                else:

                    #print "transferred succesfully",f.name
                    f.transferstate = "TRANSFERRED"
                    # FIXME: think about using the
                    # pre-emit-save-signal
                    # to invoke Dipo's SQLServer2
                    try:
                        f.save(update_fields=["transferstate"])       
                    except Exception as e:
                        logging.debug("Got exception %s while updating file %s with id %i" %(e.__repr__(),f.name,f.pk))
                        errors += 1
                    
                    sane_files.append(f)
            # else case for corrupt files            
            else:
                #print "file corrupt",f.name,f.md5sum,local_csum_file_pairs[get_local_filename(f)]
                if set_ignored:
                    logging.warn("Setting 'IGNORED' flag on flie %s %s" %(f.path,f.name)  )
                    if "GCD" in f.name:
                        representatives = Urlpath.objects.filter(md5sum=f.md5sum).exclude(transferstate__exact="TRANSFERRED")
                        logging.debug("Found %i representatives for file %s for DELETED flag" %(len(representatives),f.name))
                        gcd_errors = 0
                        for r in representatives:
                            #print r.pk, r.md5sum,r.name,r.transferstate
                            r.transferstate = "IGNORED"
                            try:
                                r.save(update_fields=["transferstate"])
                            except Exception as e:
                                logging.debug("Got exception (gcd) %s while updating file %s with id %i" %(e.__repr__(),r.name,r.pk))
                                gcd_errors += 1

                        if gcd_errors:
                            logging.debug("%i gcd errors occured during db-update" %gcd_errors)
                    else:
                        f.transferstate = "IGNORED"
                        f.save(update_fields=["transferstate"])

                corrupt_files.append(f)
    # commit all as bunch
    # be carful not to lock the db
    #transaction.commit()
    logging.info("%i files checked, updated the db for %i files and %i files corrupt" %(len(files),len(sane_files),len(corrupt_files)))

    if errors:
        logging.warn("%i errors occured during db-update" %errors)

    #DEBUG
    #for f in sane_files:
        #print "------------"
        #print f.pk,f.urlpath_id,f.path,f.name,f.md5sum,f.transferstate
    # clear the tempfile
    for f in md5sum_files:
        os.remove(f)

    # adding the ghostfiles to request a copy of them
    corrupt_files += ghostfiles

    return corrupt_files,sane_files
    



def format_csum(checksum):
    """
    Convert the checksum to the desired format
    """
    buffer = ''
    formatted_checksum = ''
    for letter in checksum:
        buffer+= letter
        if len(buffer) == 2:
            formatted_checksum += buffer + ':'
            buffer = ''

    formatted_checksum = formatted_checksum.rstrip(':')
    if not ":" in checksum:
        return formatted_checksum
    else:
        return checksum


def parse_md5sumfile(md5sumfile):
    """
    Parse the md5sumfile calculated on the cluster
    """

    csum_file_pairs = dict()
    with open(md5sumfile) as tmpcontent:
        for line in tmpcontent.readlines():
            line = line.split()
            try:
                #print format_csum(line[0])
                #print line[0]
                csum_file_pairs[line[1]] = format_csum(line[0])
            except IndexError:
                logging.debug("csum file pair corrupt %s" %line.__repr__())
                csum_file_pairs[line[0]] = "FAILED"

    return csum_file_pairs

def copy(files,cfg):
    """
    The actual routine for copying. Accepts a list
    of files from the urlpath-table.
    Checks if the copy was good by comparing
    checksums
    """

    ## DEBUG
    #print "copy files"
    #for f in files:
    #    print f.pk,f.urlpath_id,f.name,f.transferstate
    #print "----------------------------------------------"

    # check if grid-certificate is still valid
    check_voms_proxy()

    thisjobstart     = datetime.datetime.now()
    tmpdir = cfg.get("tmpdir","tmpdir")
    logdir = cfg.get("logging","logdir")
    #globus-url-options        
    parallel      = cfg.get('globus_url_options','parallel')
    cc            = cfg.get('globus_url_options','cc')
    tcp_bs        = cfg.get('globus_url_options','tcp_bs')
    bs            = cfg.get('globus_url_options','bs')
    rst_retries   = cfg.get('globus_url_options','rst_retries')
    rst_interval  = cfg.get('globus_url_options','rst_interval')

    copy_retries  = cfg.getint("advanced_options","copy_retries")
   
    for trial in xrange(copy_retries + 1):
        logging.debug("Starting copy cycle %i of %i" %(trial,copy_retries)) 
        corrupt_files,goodfiles = local_csum_check(files,cfg)
        logging.debug("Got %i files to copy" %len(corrupt_files))
        logging.debug("%i files where found copied and sane already" %len(goodfiles))
        if corrupt_files:

            # dcache is not able to overwrite files and create directories recursively, do this manually
            remove(corrupt_files)
            create_directories(corrupt_files)

            # copy new files
            filelist = write_filelist(corrupt_files,cfg)
            totalsize = [float(f.size) for f in corrupt_files]
            
            # avoid buffering of too much output as it might cause problems with multiprocessing.Pool()
            sys.stdout.flush()

            # FIXME be careful with the -dbg option, as much output
            # might cause problems with multiprocessing/subprocess forked jobs
            globus_cmd = ['globus-url-copy', '-r' , '-nodcau', '-fast', '-p', parallel, '-tcp-bs',tcp_bs, '-bs', bs, '-rst', '-cc', cc,'-vb','-c', '-rst-retries', rst_retries, '-rst-interval', rst_interval,'-cd', '-f',filelist]
            globus_log = os.tempnam(logdir,'glog')
            globus_job = subprocess.Popen(globus_cmd,stdout=open(globus_log,"w"),stderr=subprocess.PIPE)
            globus_job_pid = globus_job.pid
            logging.info("Putting together globus string %s" %("".join(globus_cmd))) 
            logging.info("Submitting globus job %i with filelist %s writing to logfile %s" %(globus_job_pid,filelist,globus_log))
            std_error  =  globus_job.communicate()[1]
            if std_error:
                logging.warn("Globus job failed with the following error %s" %std_error.__repr__())

            # remove the tmpfile
            os.remove(filelist)
            # avoid buffering of too much output as it might cause problems with multiprocessing.Pool()
            sys.stdout.flush()

            logging.debug("Copy finished!")

            # monitoring tasks
        thisjobs_consumed_copytime = (datetime.datetime.now() - thisjobstart).total_seconds()
        corrupt_files,goodfiles = local_csum_check(corrupt_files,cfg,set_ignored=False)#(trial == copy_retries))

        thisjobs_consumed_time = datetime.datetime.now() - thisjobstart
        thisjobs_consumed_time = thisjobs_consumed_time.total_seconds()
        datavolume = n.array([float(f.size) for f in goodfiles]).sum()

        jobinfo = dict()
        jobinfo["corrupt_files"]        = len(corrupt_files)
        jobinfo["copied_files"]         = len(goodfiles)
        jobinfo["elapsed_copy_time"]    = thisjobs_consumed_copytime
        jobinfo["elapsed_time"]         = thisjobs_consumed_time
        jobinfo["datavolume"]           = datavolume 
        jobinfo["transfertime"]         = datetime.datetime.now()

        copyjobinfo  = CopyJob(**jobinfo)
        copyjobinfo.save(using="copyjobs")
    
    return jobinfo

def list_slicer(list_to_slice,slices):
    """
    helper function to slice a list
    """
    
    #FIXME: there must be something in the std lib..
    # implementing this because I am flying anyway
    # right now and have nothing to do..


    if slices == 0:
        slices = 1 # prevent ZeroDivisionError
    maxslice = len(list_to_slice)/slices
    if (maxslice*slices) < len(list_to_slice) :
        maxslice = maxslice + 1
    for index in range(0,slices):
        lower_bound = index*maxslice
        upper_bound = lower_bound + maxslice
        thisslice = list_to_slice[lower_bound:upper_bound]
        yield thisslice



