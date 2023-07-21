# Run the model
import os
import warnings
import shutil

def line_nophysic_check(line):
    """Check if physic is deactivated"""
    if len(line) < 1:
        return False
    elif line[0]=='#':
        return False
    elif not('RUN_PHYSICS:.false.' in line):
        return False
    else:
        return True

def check(file):
    """Return True is physic is activated and False otherwise"""
    lines = open(file, 'r').readlines()
    # Strips the newline character
    for line in lines:
        if line_nophysic_check(line):
            return False
    return True

def main(agcm_file_path, physic):
    """Copy the corresponding AGCM_{phys}.rc file to AGCM.rc,
    check if it has corresponding physic.
    Then Run gcm_run.j from the file using either AGCM_r
    The old agcm file is overwritten
    Args:
        file_path (str): path of the agcm file with or without physic
        physic (bool): boolean indicating if physic must be present or not
    """
    has_physic = check(agcm_file_path)
    if has_physic != physic:
        if has_physic:
            warnings.warn("Run file doesn't have physic when it should")  
        else:
            warnings.warn("Run file have physic activated when it shouldn't")  
    assert(has_physic==physic) 

    # COPY THE AGCM file :
    agcm_orig_file = f"{os.path.dirname(agcm_file_path)}/AGCM.rc"
    shutil.copyfile(agcm_file_path, agcm_orig_file)

    if physic:
        print(f"running with physic: .{agcm_file_path}")
    else:
        print(f"running without physic: .{agcm_file_path}")
    os.system(f".{agcm_file_path}")
    return 
