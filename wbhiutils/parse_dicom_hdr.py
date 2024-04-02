import re

# Parse a dicom header and return the pi-id and sub-id
def parse_pi_sub(dcm_hdr, site): 
    if site == 'ucsb':
        pi_id, sub_id = re.split('[^0-9a-zA-Z]', dcm_hdr["PatientName"])[:2]
    elif site == 'uci':
        pi_id = re.split('[^0-9a-zA-Z]', dcm_hdr["PatientName"])[0]
        sub_id = re.split('[^0-9a-zA-Z]', dcm_hdr["PatientID"])[0]
    elif site == 'ucb':
        pi_id = re.split(' ', dcm_hdr["StudyDescription"])[0]
        sub_id = dcm_hdr["PatientName"]
    else:
        pi_id, sub_id = re.split('[^0-9a-zA-Z]', dcm_hdr["PatientName"])[:2]
    
    return pi_id, sub_id
