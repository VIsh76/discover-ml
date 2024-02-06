# Restart from clean folder ?
# Restart from previous moment ?
# (tar.z)
import shutil
import datetime
import os


def main(folder_experiment, folder_to_save):
    """Save the current state of the folder experiment into folder to save
    That way we can reload it twice(one for physic, one without physic)

    Args:
        folder_experiment (str): folder of the experiment
        folder_to_save (str): where to save
    """
    # Save restart files to the folder:
     
    if not os.path.exists(folder_to_save):
        print(f"CREATING {folder_to_save}")
        os.makedirs(folder_to_save)
    for rst in os.listdir(folder_experiment):
        if rst[-4:] == '_rst' and rst[0] != '.':
            if os.path.exists(f'{folder_to_save}/{rst}'):
                print(f"Erase previous '{folder_to_save}/{rst}")
                os.remove(f"{folder_to_save}/{rst}")
            print(f'Copy {rst}')
            shutil.copy(f'{folder_experiment}/{rst}' , 
                        f'{folder_to_save}/{rst}')
    # Save History, Cap Restart, Cap rc
    for file in ['cap_restart']:
            print(f'Copy {file}')
            shutil.copy(f'{folder_experiment}/{file}' , 
                        f'{folder_to_save}/{file}')        
    return 
