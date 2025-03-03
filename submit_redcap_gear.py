import logging
import os
import flywheel

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
        log.info('Submitted job %s', gear_job_id)
        return gear_job_id
    except flywheel.rest.ApiException:
        log.exception('An exception was raised when attempting to submit a job for %s', gear.label)

def main():
    client = flywheel.Client(os.environ['FW_API_KEY'])
    redcap_api_key = os.environ['REDCAP_API_KEY']

    redcap_gear = client.lookup('gears/wbhi-redcap')
    pre_deid_project = client.lookup('wbhi/pre-deid')
    redcap_config = {
        'redcap_api_key': redcap_api_key,
        'ignore_until_n_days_old': 1
    }

    run_gear(redcap_gear, None, redcap_config, pre_deid_project)


if __name__ == "__main__":
    main()