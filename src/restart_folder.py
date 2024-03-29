# Restart from clean folder ?
# Restart from previous moment ?
# (tar.z)
import shutil
import os



def main(folder_to_reset, folder_clean):
    """Reset folder_to_reset from parameter from folder_clean
    Erase _rst files, copy them from folder_clean to folder_to_reset
    and cap_restart, CAP.rc, HISTORY.rc

    Args:
        folder_to_reset (str): folder to reset
        folder_clean (str): intial folder untouched
    """
    # REMOVE ALL RST files first :
    print(f"LOADING FRON {folder_clean}")
    for rst in os.listdir(folder_to_reset):
        if rst[-4:] == '_rst':
            print(f"Remove {rst}")
            os.remove(f'{folder_to_reset}/{rst}')   
    for rst in os.listdir(folder_clean):
        if rst[-4:] == '_rst':
            print(f'Copy {rst}')
            shutil.copy(f'{folder_clean}/{rst}' , 
                        f'{folder_to_reset}/{rst}')
    for file in ['cap_restart']:
            print(f'Copy {file}')
            shutil.copy(f'{folder_clean}/{file}' , 
                        f'{folder_to_reset}/{file}')        
    return 
