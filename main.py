from src import restart_folder, run_model, save_collection, save_restart_state, restart_change_dates
import datetime
import warnings
import os

# Parameters are here (should be cleanner)
## folders:

_full_path = "/Users/vmarchai/Volumes/nobackup/experiments"
_full_path = "/discover/nobackup/vmarchai/experiments"
experiment_name ='test-c48'
experiment_folder = f"{_full_path}/{experiment_name}"
initial_folder =  f"{_full_path}/init-c48"
restarts_folder = f"{_full_path}/restarts-ml"

## Files
#agcm_nophysic_path = f"{experiment_folder}/AGCM_nophysic.rc"
#agcm_physic_path = f"{experiment_folder}/AGCM_physic.rc"
agcm_file_path = f"{experiment_folder}/AGCM.rc"
run_file_path = f"{experiment_folder}/gcm_run.j"
cap_restart_path = f"{experiment_folder}/cap_restart"
cap_rc_path = f"{experiment_folder}/cap.rc"

## Variables saving
list_of_vars = ['ml_input', 'ml_output']
## Heart_beat
heart_beat_dt = 450
time_format= "%Y%m%d %H%M%S"
## Pre launch T:
T = datetime.timedelta(seconds=heart_beat_dt)

def get_beg_date(cap_restart_file):
    date_str = open(cap_restart_file, 'r').readlines()[0].strip('\n')
    date_beg = datetime.datetime.strptime(date_str, "%Y%m%d %H%M%S")
    return date_beg

def format_history_path(intial_folder, save_folder, end_date, var):
    return f"{intial_folder}/{save_folder}/{var}/{end_date.strftime('%Y%m')}/{experiment_name}.{var}.{end_date.strftime('%Y%m%d_%H%Mz')}.nc4"
    
def block(T, 
          experiment_folder, 
          reloader_folder, 
          run_physic,
          list_of_vars=[],
          save_restart_path=False,
          save_history_folder=False):
    print(f"# Running for {T}")
    print('## Restart')
    restart_folder.main(experiment_folder, reloader_folder)
    start_date_str = get_beg_date(cap_restart_path)
    print('Start_Date :', start_date_str)
    end_date = restart_change_dates.main(cap_rc_path, start_date_str, T, time_format)
    print('## Run model')
    # run_model.main(agcm_file_path, run_file_path, physic=run_physic)
    if save_restart_path:
        print('## Save Restart')
        save_restart_state.main(experiment_folder, save_restart_path)
    if save_history_folder:
        for var in list_of_vars:
            print(f'## Save History {var}')
            input_file = format_history_path(experiment_folder, 'holding', end_date, var)
            output_file = format_history_path(experiment_folder, save_history_folder, end_date, var)
            save_collection.main(input_file, output_file)
    return end_date


if __name__ == '__main__':
    warnings.warn("HISTORY.rc file date must have '%Y%m%d %H%M%S' format")
    print("Preparation")
    block(T, 
          experiment_folder=experiment_folder, 
          reloader_folder=initial_folder,
          run_physic=True,
          list_of_vars=list_of_vars,
          save_restart_path=restarts_folder,
          save_history_folder='ml-data_input')

    print("Run No Physic")
    block(T=datetime.timedelta(seconds=heart_beat_dt),
          experiment_folder=experiment_folder, 
          reloader_folder=initial_folder,
          run_physic=False,
          list_of_vars=list_of_vars,
          save_restart_path=False,
          save_history_folder='ml-data_nophys')

    print("Run Physic")
    block(T=datetime.timedelta(seconds=heart_beat_dt), 
          experiment_folder=experiment_folder, 
          reloader_folder=initial_folder,
          run_physic=False,
          list_of_vars=list_of_vars,
          save_restart_path=restarts_folder,
          save_history_folder='ml-data_phys')
