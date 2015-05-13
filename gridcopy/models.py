# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Alias(models.Model):
    alias_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey('Dataset', null=True, blank=True)
    name = models.CharField(max_length=30L, unique=True, blank=True)
    class Meta:
        managed = False
        db_table = 'alias'

class ArchivedJob(models.Model):
    job_id = models.IntegerField(primary_key=True)
    queue_id = models.IntegerField()
    status = models.CharField(max_length=19L, blank=True)
    prev_state = models.CharField(max_length=19L, blank=True)
    dataset = models.ForeignKey('Dataset')
    grid = models.ForeignKey('Grid', null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    errormessage = models.TextField(blank=True)
    host = models.CharField(max_length=200L, blank=True)
    submitdir = models.CharField(max_length=200L, blank=True)
    grid_queue_id = models.CharField(max_length=80L, blank=True)
    failures = models.IntegerField(null=True, blank=True)
    evictions = models.IntegerField(null=True, blank=True)
    time_real = models.FloatField(null=True, blank=True)
    time_user = models.FloatField(null=True, blank=True)
    time_sys = models.FloatField(null=True, blank=True)
    mem_heap = models.FloatField(null=True, blank=True)
    mem_heap_peak = models.FloatField(null=True, blank=True)
    mem_stack_peak = models.FloatField(null=True, blank=True)
    status_changed = models.DateTimeField(null=True, blank=True)
    nevents = models.IntegerField(null=True, blank=True)
    gevents = models.IntegerField(null=True, blank=True)
    keepalive = models.DateTimeField(null=True, blank=True)
    passkey = models.CharField(max_length=10L, blank=True)
    tray = models.IntegerField(null=True, blank=True)
    iter = models.IntegerField(null=True, blank=True)
    run = models.IntegerField(null=True, blank=True)
    old = models.TextField(blank=True) # This field type is a guess.
    host_id = models.CharField(max_length=20L, blank=True)
    class Meta:
        managed = False
        db_table = 'archived_job'

class ArchivedJobStatistics(models.Model):
    job_statistics_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey('Dataset')
    queue_id = models.IntegerField()
    name = models.CharField(max_length=30L)
    value = models.FloatField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'archived_job_statistics'

class ArrayElement(models.Model):
    array_element_id = models.IntegerField(primary_key=True)
    parameter = models.ForeignKey('Parameter')
    name = models.CharField(max_length=30L, blank=True)
    value = models.CharField(max_length=255L)
    unit = models.CharField(max_length=30L, blank=True)
    class Meta:
        managed = False
        db_table = 'array_element'

class BatchOption(models.Model):
    batch_option_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30L)
    type = models.CharField(max_length=30L, blank=True)
    value = models.CharField(max_length=255L)
    dataset = models.ForeignKey('Dataset')
    class Meta:
        managed = False
        db_table = 'batch_option'

class CarrayElement(models.Model):
    carray_element_id = models.IntegerField(primary_key=True)
    cparameter = models.ForeignKey('Cparameter')
    name = models.CharField(max_length=30L, blank=True)
    value = models.CharField(max_length=255L)
    unit = models.CharField(max_length=30L, blank=True)
    class Meta:
        managed = False
        db_table = 'carray_element'

class ConfigFiles(models.Model):
    dataset = models.ForeignKey('Dataset', primary_key=True)
    xml = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'config_files'

class Connection(models.Model):
    connection_id = models.IntegerField(primary_key=True)
    source = models.CharField(max_length=30L)
    outbox = models.CharField(max_length=30L)
    destination = models.CharField(max_length=30L)
    inbox = models.CharField(max_length=30L)
    dataset = models.ForeignKey('Dataset')
    tray_index = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'connection'

class Cparameter(models.Model):
    cparameter_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30L)
    type = models.CharField(max_length=10L)
    value = models.CharField(max_length=255L)
    unit = models.CharField(max_length=30L, blank=True)
    dataset = models.ForeignKey('Dataset')
    module_pivot = models.ForeignKey('ModulePivot')
    tray_index = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'cparameter'

class Dataset(models.Model):
    dataset_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=40L)
    description = models.CharField(max_length=255L, blank=True)
    description_template = models.CharField(max_length=255L, blank=True)
    simcat = models.ForeignKey('Simcat', null=True, blank=True)
    institution = models.CharField(max_length=50L, blank=True)
    hostname = models.CharField(max_length=200L, blank=True)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField(null=True, blank=True)
    temporary_storage = models.CharField(max_length=255L, blank=True)
    global_storage = models.CharField(max_length=255L, blank=True)
    time_real = models.FloatField(null=True, blank=True)
    time_user = models.FloatField(null=True, blank=True)
    time_sys = models.FloatField(null=True, blank=True)
    mem_heap = models.FloatField(null=True, blank=True)
    mem_heap_peak = models.FloatField(null=True, blank=True)
    mem_stack_peak = models.FloatField(null=True, blank=True)
    jobs_submitted = models.IntegerField(null=True, blank=True)
    jobs_enqueued = models.IntegerField(null=True, blank=True)
    jobs_completed = models.IntegerField(null=True, blank=True)
    jobs_failed = models.IntegerField(null=True, blank=True)
    inputevents = models.IntegerField(null=True, blank=True)
    events = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=14L, blank=True)
    verified = models.CharField(max_length=5L, blank=True)
    tray_count = models.IntegerField()
    ticket_number = models.IntegerField()
    parent_id = models.IntegerField(null=True, blank=True)
    hist = models.IntegerField(null=True, blank=True)
    dataset_category = models.CharField(max_length=11L)
    debug = models.IntegerField(null=True, blank=True)
    geometry = models.CharField(max_length=15L, blank=True)
    normalization = models.FloatField(null=True, blank=True)
    inputdataset_id = models.IntegerField(null=True, blank=True)
    chksum_verify = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'dataset'

class DatasetNotes(models.Model):
    dataset_note_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    posted_by = models.CharField(max_length=255L)
    posted_on = models.DateTimeField()
    content = models.TextField()
    type = models.CharField(max_length=7L, blank=True)
    class Meta:
        managed = False
        db_table = 'dataset_notes'

class DatasetParam(models.Model):
    dataset_param_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=50L)
    value = models.CharField(max_length=50L)
    class Meta:
        managed = False
        db_table = 'dataset_param'

class DatasetStatistics(models.Model):
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=30L)
    value = models.FloatField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'dataset_statistics'

class DatasetStatisticsLog(models.Model):
    dataset_id = models.IntegerField()
    queue_id = models.IntegerField()
    grid_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255L)
    amount = models.DecimalField(max_digits=67, decimal_places=2)
    class Meta:
        managed = False
        db_table = 'dataset_statistics_log'

class DatasetStatisticsMv(models.Model):
    dataset = models.ForeignKey(Dataset)
    metaproject = models.ForeignKey('Metaproject')
    simcat = models.ForeignKey('Simcat')
    grid_id = models.IntegerField()
    name = models.CharField(max_length=30L)
    value = models.FloatField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'dataset_statistics_mv'

class Dictionary(models.Model):
    dictionary_id = models.IntegerField()
    keystring = models.CharField(max_length=20L)
    value = models.CharField(max_length=255L)
    dataset = models.ForeignKey(Dataset)
    class Meta:
        managed = False
        db_table = 'dictionary'

class Dif(models.Model):
    dataset = models.ForeignKey(Dataset)
    entry_title = models.CharField(max_length=30L, blank=True)
    parameters = models.CharField(max_length=85L, blank=True)
    summary = models.TextField(blank=True)
    source_name = models.CharField(max_length=56L)
    dif_creation_date = models.DateTimeField(null=True, blank=True)
    sensorname = models.CharField(max_length=8L, blank=True)
    class Meta:
        managed = False
        db_table = 'dif'

class Diskmgt(models.Model):
    name = models.TextField(blank=True)
    wg = models.TextField(blank=True)
    vol = models.TextField(blank=True)
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'diskmgt'

class Extern(models.Model):
    extern_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=30L)
    version = models.CharField(max_length=10L, blank=True)
    description = models.CharField(max_length=100L, blank=True)
    command = models.CharField(max_length=50L)
    arguments = models.CharField(max_length=255L, blank=True)
    infile = models.CharField(max_length=100L, blank=True)
    outfile = models.CharField(max_length=100L, blank=True)
    errfile = models.CharField(max_length=100L, blank=True)
    steering = models.TextField(blank=True)
    steering_name = models.CharField(max_length=100L, blank=True)
    class Meta:
        managed = False
        db_table = 'extern'

class File(models.Model):
    file_id = models.IntegerField(primary_key=True)
    job = models.ForeignKey('Job')
    dataset = models.ForeignKey(Dataset)
    path = models.CharField(max_length=255L, blank=True)
    subdir = models.CharField(max_length=100L, blank=True)
    filename = models.CharField(max_length=100L, blank=True)
    class Meta:
        managed = False
        db_table = 'file'

class Geometry(models.Model):
    geometry_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=4L)
    description = models.CharField(max_length=100L, blank=True)
    class Meta:
        managed = False
        db_table = 'geometry'

class Grid(models.Model):
    grid_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30L, unique=True, blank=True)
    institution = models.CharField(max_length=80L, blank=True)
    batchsys = models.CharField(max_length=30L, blank=True)
    url = models.CharField(max_length=80L, blank=True)
    submitnode = models.CharField(max_length=80L, blank=True)
    soaptray = models.CharField(max_length=12L, blank=True)
    soapmon = models.CharField(max_length=12L, blank=True)
    soapqueue = models.CharField(max_length=12L, blank=True)
    soapdh = models.CharField(max_length=12L, blank=True)
    soaphisto = models.CharField(max_length=12L, blank=True)
    logserver = models.CharField(max_length=12L, blank=True)
    version = models.CharField(max_length=30L, blank=True)
    soaptray_pid = models.IntegerField()
    soapmon_pid = models.IntegerField()
    soapqueue_pid = models.IntegerField()
    soapdh_pid = models.IntegerField()
    soaphisto_pid = models.IntegerField()
    logserver_pid = models.IntegerField(null=True, blank=True)
    lastupdate = models.DateTimeField(null=True, blank=True)
    visible = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'grid'

class GridStatistics(models.Model):
    grid_statistics_id = models.IntegerField(primary_key=True)
    grid = models.ForeignKey(Grid)
    dataset = models.ForeignKey(Dataset)
    failures = models.IntegerField(null=True, blank=True)
    evictions = models.IntegerField(null=True, blank=True)
    ok = models.IntegerField(null=True, blank=True)
    time_real = models.FloatField(null=True, blank=True)
    time_user = models.FloatField(null=True, blank=True)
    time_sys = models.FloatField(null=True, blank=True)
    mem_heap = models.FloatField(null=True, blank=True)
    mem_heap_peak = models.FloatField(null=True, blank=True)
    mem_stack_peak = models.FloatField(null=True, blank=True)
    nevents = models.IntegerField(null=True, blank=True)
    debug = models.IntegerField(null=True, blank=True)
    suspend = models.IntegerField(null=True, blank=True)
    task_def_id = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'grid_statistics'

class History(models.Model):
    history_id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=12L, blank=True)
    cmd = models.CharField(max_length=60L, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'history'

class Job(models.Model):
    job_id = models.IntegerField(primary_key=True)
    queue_id = models.IntegerField()
    status = models.CharField(max_length=19L, blank=True)
    prev_state = models.CharField(max_length=19L, blank=True)
    dataset = models.ForeignKey(Dataset)
    grid = models.ForeignKey(Grid, null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    errormessage = models.TextField(blank=True)
    host = models.CharField(max_length=200L, blank=True)
    submitdir = models.CharField(max_length=200L, blank=True)
    grid_queue_id = models.CharField(max_length=80L, blank=True)
    failures = models.IntegerField(null=True, blank=True)
    evictions = models.IntegerField(null=True, blank=True)
    time_real = models.FloatField(null=True, blank=True)
    time_user = models.FloatField(null=True, blank=True)
    time_sys = models.FloatField(null=True, blank=True)
    mem_heap = models.FloatField(null=True, blank=True)
    mem_heap_peak = models.FloatField(null=True, blank=True)
    mem_stack_peak = models.FloatField(null=True, blank=True)
    status_changed = models.DateTimeField(null=True, blank=True)
    nevents = models.IntegerField(null=True, blank=True)
    gevents = models.IntegerField(null=True, blank=True)
    keepalive = models.DateTimeField(null=True, blank=True)
    passkey = models.CharField(max_length=10L, blank=True)
    tray = models.IntegerField(null=True, blank=True)
    iter = models.IntegerField(null=True, blank=True)
    run = models.IntegerField(null=True, blank=True)
    old = models.TextField() # This field type is a guess.
    host_id = models.CharField(max_length=20L, blank=True)
    class Meta:
        managed = False
        db_table = 'job'

class JobDependency(models.Model):
    job_dependency_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, null=True, blank=True)
    input_dataset = models.ForeignKey(Dataset, null=True, db_column='input_dataset', blank=True)
    input_job = models.CharField(max_length=20L, blank=True)
    class Meta:
        managed = False
        db_table = 'job_dependency'

class JobStatistics(models.Model):
    job_statistics_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    queue_id = models.IntegerField()
    name = models.CharField(max_length=30L)
    value = models.FloatField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'job_statistics'

class Metaproject(models.Model):
    metaproject_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20L)
    major_version = models.CharField(max_length=3L, blank=True)
    minor_version = models.CharField(max_length=3L, blank=True)
    patch_version = models.CharField(max_length=5L, blank=True)
    branch_version = models.CharField(max_length=2L, blank=True)
    versiontxt = models.CharField(max_length=30L, blank=True)
    visible = models.IntegerField()
    notes = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'metaproject'

class MetaprojectPivot(models.Model):
    metaproject_pivot_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    metaproject = models.ForeignKey(Metaproject)
    load_index = models.IntegerField()
    tray_index = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'metaproject_pivot'

class MetaprojectTarball(models.Model):
    metaproject_tarball_id = models.IntegerField(primary_key=True)
    metaproject = models.ForeignKey(Metaproject)
    platform = models.CharField(max_length=20L, blank=True)
    gcc = models.CharField(max_length=20L, blank=True)
    relpath = models.CharField(max_length=100L, blank=True)
    class Meta:
        managed = False
        db_table = 'metaproject_tarball'

class Module(models.Model):
    module_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40L)
    class_field = models.CharField(max_length=60L, db_column='class') # Field renamed because it was a Python reserved word.
    module_type = models.CharField(max_length=11L)
    project = models.ForeignKey('Project')
    class Meta:
        managed = False
        db_table = 'module'

class ModuleDependency(models.Model):
    module_dependency_id = models.IntegerField(primary_key=True)
    module = models.ForeignKey(Module)
    project = models.ForeignKey('Project')
    class Meta:
        managed = False
        db_table = 'module_dependency'

class ModulePivot(models.Model):
    module_pivot_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60L)
    module = models.ForeignKey(Module)
    load_index = models.IntegerField()
    dataset = models.ForeignKey(Dataset)
    tray_index = models.IntegerField()
    iptype = models.CharField(max_length=4L, blank=True)
    class Meta:
        managed = False
        db_table = 'module_pivot'

class MpPivot(models.Model):
    mp_pivot_id = models.IntegerField(primary_key=True)
    metaproject = models.ForeignKey(Metaproject)
    project = models.ForeignKey('Project')
    project_name = models.CharField(max_length=100L, blank=True)
    class Meta:
        managed = False
        db_table = 'mp_pivot'

class NodeStatistics(models.Model):
    node_statistics_id = models.IntegerField()
    name = models.CharField(max_length=200L)
    completed = models.IntegerField(null=True, blank=True)
    failures = models.IntegerField(null=True, blank=True)
    evictions = models.IntegerField(null=True, blank=True)
    time_real = models.FloatField(null=True, blank=True)
    time_user = models.FloatField(null=True, blank=True)
    time_sys = models.FloatField(null=True, blank=True)
    mem_heap = models.FloatField(null=True, blank=True)
    mem_heap_peak = models.FloatField(null=True, blank=True)
    grid = models.ForeignKey(Grid, null=True, blank=True)
    platform = models.CharField(max_length=60L, blank=True)
    host_id = models.CharField(max_length=60L, blank=True)
    syscheck = models.CharField(max_length=6L, blank=True)
    lastupdate = models.DateTimeField(null=True, blank=True)
    domain = models.CharField(max_length=60L, blank=True)
    class Meta:
        managed = False
        db_table = 'node_statistics'

class Parameter(models.Model):
    parameter_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40L)
    type = models.CharField(max_length=10L)
    value = models.CharField(max_length=255L)
    unit = models.CharField(max_length=30L, blank=True)
    description = models.TextField(blank=True)
    module = models.ForeignKey(Module)
    class Meta:
        managed = False
        db_table = 'parameter'

class Plus(models.Model):
    dataset = models.ForeignKey(Dataset)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=12L, blank=True)
    i3db_key = models.IntegerField(null=True, blank=True)
    subcategory = models.CharField(max_length=40L, blank=True)
    steering_file = models.CharField(max_length=250L, blank=True)
    class Meta:
        managed = False
        db_table = 'plus'

class PreProcessingChecks(models.Model):
    run_id = models.IntegerField(primary_key=True)
    gcdcheck = models.IntegerField(null=True, db_column='GCDCheck', blank=True) # Field name made lowercase.
    baddomscheck = models.IntegerField(null=True, db_column='BadDOMsCheck', blank=True) # Field name made lowercase.
    nolid = models.IntegerField(null=True, db_column='NoLID', blank=True) # Field name made lowercase.
    runduration = models.IntegerField(null=True, db_column='RunDuration', blank=True) # Field name made lowercase.
    nottestrun = models.IntegerField(null=True, db_column='NotTestRun', blank=True) # Field name made lowercase.
    filescomplete = models.IntegerField(null=True, db_column='FilesComplete', blank=True) # Field name made lowercase.
    checksoverride = models.IntegerField(null=True, db_column='ChecksOverride', blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'pre_processing_checks'

class PreProcessingChecksParanoid(models.Model):
    run_id = models.IntegerField(primary_key=True)
    gcdcheck = models.IntegerField(null=True, db_column='GCDCheck', blank=True) # Field name made lowercase.
    baddomscheck = models.IntegerField(null=True, db_column='BadDOMsCheck', blank=True) # Field name made lowercase.
    nolid = models.IntegerField(null=True, db_column='NoLID', blank=True) # Field name made lowercase.
    runduration = models.IntegerField(null=True, db_column='RunDuration', blank=True) # Field name made lowercase.
    nottestrun = models.IntegerField(null=True, db_column='NotTestRun', blank=True) # Field name made lowercase.
    filescomplete = models.IntegerField(null=True, db_column='FilesComplete', blank=True) # Field name made lowercase.
    checksoverride = models.IntegerField(null=True, db_column='ChecksOverride', blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'pre_processing_checks_paranoid'

class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20L)
    major_version = models.CharField(max_length=3L, blank=True)
    minor_version = models.CharField(max_length=3L, blank=True)
    patch_version = models.CharField(max_length=3L, blank=True)
    versiontxt = models.CharField(max_length=20L, blank=True)
    type = models.CharField(max_length=6L, blank=True)
    class Meta:
        managed = False
        db_table = 'project'

class ProjectDepend(models.Model):
    project_depend_id = models.IntegerField(primary_key=True)
    project = models.ForeignKey(Project)
    metaproject = models.ForeignKey(Metaproject)
    dependency = models.ForeignKey(Project)
    class Meta:
        managed = False
        db_table = 'project_depend'

class ProjectPivot(models.Model):
    project_pivot_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    project = models.ForeignKey(Project)
    load_index = models.IntegerField()
    tray_index = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'project_pivot'

class Run(models.Model):
    run_entry_id = models.IntegerField(primary_key=True)
    run_id = models.IntegerField(null=True, blank=True)
    dataset = models.ForeignKey(Job, null=True, blank=True)
    queue = models.ForeignKey(Job, null=True, blank=True)
    sub_run = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'run'

class Simcat(models.Model):
    simcat_id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=30L, unique=True)
    class Meta:
        managed = False
        db_table = 'simcat'

class SteeringDependency(models.Model):
    steering_dependency_id = models.IntegerField(primary_key=True)
    filename = models.CharField(max_length=255L)
    dataset = models.ForeignKey(Dataset)
    cache = models.CharField(max_length=5L, blank=True)
    class Meta:
        db_table = 'steering_dependency'

class SteeringParameter(models.Model):
    steering_parameter_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40L)
    type = models.CharField(max_length=10L)
    value = models.CharField(max_length=255L)
    description = models.TextField(blank=True)
    dataset = models.ForeignKey(Dataset)
    class Meta:
        managed = False
        db_table = 'steering_parameter'

class StorageRequests(models.Model):
    request_id = models.IntegerField(primary_key=True)
    r_name = models.CharField(max_length=50L, blank=True)
    r_email = models.CharField(max_length=50L)
    wg_name = models.CharField(max_length=20L)
    wg_email = models.CharField(max_length=50L)
    r_vol = models.CharField(max_length=20L)
    r_size = models.IntegerField()
    r_date = models.DateField()
    r_duration = models.CharField(max_length=20L)
    a_name = models.CharField(max_length=50L, blank=True)
    a_email = models.CharField(max_length=50L, blank=True)
    a_vol = models.CharField(max_length=20L, blank=True)
    a_size = models.IntegerField(null=True, blank=True)
    a_date = models.DateField(null=True, blank=True)
    a_duration = models.CharField(max_length=20L, blank=True)
    a_status = models.CharField(max_length=8L, blank=True)
    data_season = models.CharField(max_length=20L, blank=True)
    wg_leader = models.CharField(max_length=50L, blank=True)
    class Meta:
        managed = False
        db_table = 'storage_requests'

class StorageStatus(models.Model):
    used = models.IntegerField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    request = models.ForeignKey(StorageRequests, null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'storage_status'

class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    task_def_tray = models.ForeignKey('TaskDefTray')
    job = models.ForeignKey(Job)
    host = models.CharField(max_length=255L, blank=True)
    status = models.CharField(max_length=13L, blank=True)
    last_status = models.CharField(max_length=13L, blank=True)
    status_changed = models.DateTimeField(null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    finish = models.DateTimeField(null=True, blank=True)
    grids = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'task'

class TaskDef(models.Model):
    task_def_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=255L)
    reqs = models.CharField(max_length=255L)
    parallel = models.IntegerField()
    photonics = models.IntegerField()
    opts = models.CharField(max_length=255L, blank=True)
    grids = models.CharField(max_length=255L, blank=True)
    class Meta:
        managed = False
        db_table = 'task_def'

class TaskDefRel(models.Model):
    parent_task_def = models.ForeignKey(TaskDef)
    child_task_def = models.ForeignKey(TaskDef)
    class Meta:
        managed = False
        db_table = 'task_def_rel'

class TaskDefTray(models.Model):
    task_def_tray_id = models.IntegerField(primary_key=True)
    task_def = models.ForeignKey(TaskDef)
    idx = models.IntegerField()
    iter = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'task_def_tray'

class TaskStatistics(models.Model):
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=255L)
    value = models.DecimalField(max_digits=66, decimal_places=2)
    class Meta:
        managed = False
        db_table = 'task_statistics'

class Tray(models.Model):
    tray_id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset)
    tray_index = models.IntegerField()
    iterations = models.IntegerField()
    inputevents = models.IntegerField()
    name = models.CharField(max_length=30L, blank=True)
    python = models.CharField(max_length=255L, blank=True)
    class Meta:
        managed = False
        db_table = 'tray'

class TrayFiles(models.Model):
    tray = models.ForeignKey(Tray)
    type = models.CharField(max_length=6L)
    name = models.CharField(max_length=255L)
    photonics = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'tray_files'

class Urlpath(models.Model):
    urlpath_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255L, blank=True)
    path = models.CharField(max_length=225L)
    type = models.CharField(max_length=9L)
    dataset = models.ForeignKey(Dataset)
    queue_id = models.IntegerField(null=True, blank=True)
    md5sum = models.CharField(max_length=255L, blank=True)
    size = models.IntegerField(null=True, blank=True)
    transfertime = models.FloatField(null=True, blank=True)
    transferstate = models.CharField(max_length=11L)
    verify = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'urlpath'

class UrlpathTest(models.Model):
    urlpath_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255L, blank=True)
    path = models.CharField(max_length=225L)
    type = models.CharField(max_length=9L)
    dataset_id = models.IntegerField()
    queue_id = models.IntegerField(null=True, blank=True)
    md5sum = models.CharField(max_length=255L, blank=True)
    size = models.IntegerField(null=True, blank=True)
    transfertime = models.FloatField(null=True, blank=True)
    transferstate = models.CharField(max_length=11L)
    class Meta:
        managed = False
        db_table = 'urlpath_test'

class Validatedata(models.Model):
    run_id = models.IntegerField(primary_key=True)
    dataset_id = models.IntegerField()
    processing_status = models.CharField(max_length=19L, blank=True)
    grl_status = models.CharField(max_length=6L, blank=True)
    status_conflict = models.IntegerField(null=True, blank=True)
    files_check = models.IntegerField(null=True, blank=True)
    validation_status = models.IntegerField(null=True, blank=True)
    i3live_status = models.CharField(max_length=8L, blank=True)
    class Meta:
        managed = False
        db_table = 'validateData'

class Verify(models.Model):
    urlpath_id = models.IntegerField(primary_key=True)
    verified = models.IntegerField(null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'verify'

