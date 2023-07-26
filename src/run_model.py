# Run the model
import os
import warnings
import shutil

def line_nophysic_check(line):
    """
    Check if physic is deactivated
    Return False if no impact
    Return True
    """
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

def main(agcm_file_path, run_file, physic):
    """Copy the corresponding AGCM_{phys}.rc file to AGCM.rc,
    check if it has corresponding physic.
    Then Run gcm_run.j from the file using either AGCM_r
    The old agcm file is overwritten
    Args:
        file_path (str): path of the agcm file with or without physic
        physic (bool): boolean indicating if physic must be present or not
    """
    f = open('templates/AGCM_template.rc')
    text = f.read()
    if physic:
        text=text.format(run_physic="#RUN_PHYSICS: .false.")
    else:
        text=text.format(run_physic="RUN_PHYSICS: .false.")
    f.close() 
    
    has_physic = check(agcm_file_path)
    if has_physic != physic:
        if physic:
            warnings.warn("Run file doesn't have physic when it should")  
        else:
            warnings.warn("Run file have physic activated when it shouldn't")  
        assert(has_physic==physic) 
    # Save Template
    print(f"Saving {agcm_file_path} with physic {physic}")
    outfile = open(agcm_file_path, "w")
    outfile.write(text)
    outfile.close()   
    if physic:
        print(f"running with physic: .{run_file}")
    else:
        print(f"running without physic: .{run_file}")
    os.system(f"{run_file}")
    return 
