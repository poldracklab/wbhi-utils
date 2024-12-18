import re

# Parse a dicom header and return the pi-id and sub-id
def parse_pi(dcm_hdr: dict, site: str) -> str:
    """Parse a dicom header and return the PI-ID"""
    if site == 'ucsb':
        return re.split('[^0-9a-zA-Z]', dcm_hdr["PatientName"], maxsplit=1)[0]
    elif site == 'uci':
        return re.split('__', dcm_hdr["PatientName"], maxsplit=1)[0]
    elif site == 'ucb':
        return re.split(' ', dcm_hdr["StudyDescription"], maxsplit=1)[0]
    elif site == 'ucsd':
        return dcm_hdr["ReferringPhysicianName"]
    elif site == 'ucsf':
        return re.split('[^0-9a-zA-Z]', dcm_hdr["StudyDescription"], maxsplit=1)[1]
    else:
        return re.split('[^0-9a-zA-Z]', dcm_hdr["PatientName"], maxsplit=1)[0]
    
    return pi_id, sub_id

def parse_sub(dcm_hdr: dict, site: str) -> str:
    """Parse a dicom header and return the Sub-ID"""
    if site == 'ucsb':
        return re.split('[^0-9a-zA-Z]', dcm_hdr["PatientName"], maxsplit=1)[1]
    elif site == 'uci':
        return re.split('__', dcm_hdr["PatientID"], maxsplit=1)[0]
    elif site == 'ucb':
        return dcm_hdr["PatientName"]
    elif site == 'ucsd':
        return dcm_hdr["PatientID"]
    elif site == 'ucsf':
        return dcm_hdr["PatientID"]
    else:
        return re.split('[^0-9a-zA-Z]', dcm_hdr["PatientName"], maxsplit=1)[1]
