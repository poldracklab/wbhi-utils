import logging
import os
import time
import flywheel
import sys


def run_gear(gear, inputs, config, dest, tags=None):
    """Submits a job with specified gear and inputs.
    
    Args:
        gear (flywheel.Gear): A Flywheel Gear.
        inputs (dict): Input dictionary for the gear.
        config (dict): Configuration for the gear
        dest (flywheel.container): A Flywheel Container where the output will be stored.
        tags (list): List of tags if any
        
    Returns:
        str: The id of the submitted job.
        
    """
    try:
        # Run the gear on the inputs provided, stored output in dest constainer and returns job ID
        gear_job_id = gear.run(inputs=inputs, config=config, destination=dest, tags=tags)
        log.debug('Submitted job %s', gear_job_id)
        return gear_job_id
    except flywheel.rest.ApiException:
        log.exception('An exception was raised when attempting to submit a job for %s', file_obj.name)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('root')

fw = flywheel.Client(os.environ['FW_API_KEY'])
redcap_api_key = os.environ.get('REDCAP_API_KEY')
redcap_gear = fw.lookup('gears/wbhi-redcap')
deid_gear = fw.lookup('gears/deid-export')

ignore_until_n_days_old = 1
site_list = ['ucsb']
destination_project_path = 'wbhi/wbhi'

for site in site_list:
    source_project_path = site + '/Inbound Data'
    #source_project_path = 'joe_test/ucsb_copy3'
    source_project = fw.lookup(source_project_path)
    deid_template = source_project.get_file('deid_profile.yaml')
    deid_inputs = {'deid_profile': deid_template}
    
    redcap_config = {
        'redcap_api_key': redcap_api_key,
        'ignore_until_n_days_old': ignore_until_n_days_old
    }
    redcap_job_id = run_gear(redcap_gear, None, redcap_config, source_project)
    while fw.get_job(redcap_job_id).state.name in ('PENDING', 'RUNNING'): 
        print(fw.get_job(redcap_job_id).state.name)
        time.sleep(5)
    if fw.get_job(redcap_job_id).state.name != 'COMPLETE':
        print('wbhi-redcap gear failed')
        continue
        
    to_deid_list =  [s for s in source_project.sessions() if 'wbhi' in s.tags and 'deid-wbhi' not in s.tags]
    deid_jobs = []
    
    for session in to_deid_list:
        deid_config = {
            'project_path': destination_project_path,
            'overwrite_files': True,
        }
        deid_job_id = run_gear(deid_gear, deid_inputs, deid_config, session)
        deid_jobs.append((deid_job_id, session))
    
    for job_id, session in deid_jobs:
        while fw.get_job(redcap_job_id).state.name in ('PENDING', 'RUNNING'):
            time.sleep(5)
        if fw.get_job(redcap_job_id).state.name != 'COMPLETE':
            print('wbhi-redcap gear failed')
            continue
        else:
            session.add_tag('deid-wbhi')
            
    
    