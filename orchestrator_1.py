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
site_list = ['ucsb', 'uci']
wbhi_project_path = 'wbhi/wbhi'
wbhi_project = fw.lookup(wbhi_project_path)
deid_config = {
    'project_path': wbhi_project_path,
    'overwrite_files': True,
}

# Run redcap gear in each site's project
redcap_job_list = []
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
    redcap_job_list.append((site, redcap_job_id))

# Run deid gear after completion of redcap gear for each site
deid_jobs_all = []
for site, redcap_job_id in redcap_job_list:
    start = time.time()
    while fw.get_job(redcap_job_id).state.name in ('PENDING', 'RUNNING'): 
        time.sleep(5)
    end = time.time()
    print(end - start)
    if fw.get_job(redcap_job_id).state.name != 'COMPLETE':
        print(f'wbhi-redcap gear failed for {site}')
        continue
        
    to_deid_list =  [s for s in source_project.sessions() if 'wbhi' in s.tags and 'deid-wbhi' not in s.tags]
    deid_jobs = []
    
    for session in to_deid_list:
        deid_job_id = run_gear(deid_gear, deid_inputs, deid_config, session)
        deid_jobs.append((deid_job_id, session))
    deid_jobs_all.append((site, deid_jobs))

# Wait for completeion of deid jobs and tag 'deid-wbhi'  
for site, deid_jobs in deid_jobs_all:
    for job_id, session in deid_jobs:
        start = time.time()
        while fw.get_job(redcap_job_id).state.name in ('PENDING', 'RUNNING'):
            time.sleep(5)
        end = time.time()
        print(end - start)
        if fw.get_job(redcap_job_id).state.name != 'COMPLETE':
            print(f'deid gear failed for {job_id}')
            continue
        else:
            session.add_tag('deid-wbhi')

# Wait for completion of all jobs in wbhi project
start = time.time()
while True:
    time.sleep(30)
    jobs = fw.get_current_user_jobs()['jobs']
    wbhi_jobs = [j for j in jobs if 'wbhi' in j.related_container_ids]
    current_wbhi_jobs = [j.state for j in wbhi_jobs if j.state not in ('complete', 'failed')]
    print(current_wbhi_jobs)
    if not current_wbhi_jobs:
        break
end = time.time()
print(end - start)

# Run bids-pre-curate gear
wbhi_subs = wbhi_project.subjects()
wbhi_subs_no_precurate = [s for s in wbhi_subs if 'pre-curate' not in s.tags]



    
    