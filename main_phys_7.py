# Only runs both the physic and the dynamic 
from src import restart_folder, run_model, save_collection, save_restart_state, restart_change_dates
import datetime
import warnings
import os

time_format= "%Y%m%d %H%M%S"

# Parameters are here (should be cleanner)
## folders:
_full_path = "/Users/vmarchai/Volumes/nobackup/experiments"
_full_path = "/discover/nobackup/vmarchai/experiments"
experiment_folder = f"{_full_path}/ML_0"
experiment_name ='ML_0'
initial_folder =  f"{_full_path}/reynolds_init"
restarts_folder = f"{_full_path}/restarts-ml"

## Files
#agcm_nophysic_path = f"{experiment_folder}/AGCM_nophysic.rc"
#agcm_physic_path = f"{experiment_folder}/AGCM_physic.rc"
agcm_file_path = f"{experiment_folder}/AGCM.rc"
run_file_path = f"{experiment_folder}/gcm_run.j"
cap_restart_path = f"{experiment_folder}/cap_restart"
cap_rc_path = f"{experiment_folder}/CAP.rc"


## Variables saving
list_of_vars = ['ml_input', 'ml_output']
## Heart_beat
heart_beat_dt = 450
max_runs = 195 # about two days with 15 min, 1 with 7
output_prefix = '../ML_DATA/latlon_7' # where the data is saved

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
    start_date_str = get_caprestart_date(cap_restart_path)
    print('Start_Date :', start_date_str)
    end_date = restart_change_dates.main(cap_rc_path, start_date_str, T, time_format)
    print(f'## Run model from {start_date_str} to {end_date}')
    res = run_model.main(agcm_file_path, run_file_path, physic=run_physic)   
    if save_restart_path:
        print('## Save Restart')
        save_restart_state.main(experiment_folder, save_restart_path)            

    n_failures = 0 # trackfailures on files localisation/copying
    if save_history_folder:
        for var in list_of_vars:
            print(f'## Save History {var}')
            input_file = format_history_path(experiment_folder, 'holding', end_date, var)
            output_file = format_history_path(experiment_folder, save_history_folder, end_date, var)
            n_failures += save_collection.main(input_file, output_file)
    return end_date, n_failures


def get_caprestart_date(cap_restart_file):
    """Convert the start date of the caprestart file into a datetime.datetime class

    Args:
        cap_restart_file (str): path to the cap_restart file

    Returns:
        datetime.datetime: date of the datetime
    """
    date_str = open(cap_restart_file, 'r').readlines()[0].strip('\n')
    date_beg = datetime.datetime.strptime(date_str, "%Y%m%d %H%M%S")
    return date_beg



if __name__ == '__main__':
    warnings.warn("HISTORY.rc file date must have '%Y%m%d %H%M%S' format")
    tot_failures = 0
    for n in range(max_runs):
        if n==0:
            reloader_folder = initial_folder # The first time we reload the intial folder (unless we want longer)
        else:
            reloader_folder = restarts_folder # Otherwise we reload from the restart folder with physics
        print("-------------------------- Run Physic -----------------------------")
        # Here we try 15 min and not 7.5 (heart_beat_dt * 2)
        delta_steps = heart_beat_dt
        end_date, n_failures = block(T=datetime.timedelta(seconds = delta_steps), 
              experiment_folder = experiment_folder, 
              reloader_folder = reloader_folder,
              run_physic = True,
              list_of_vars = list_of_vars,
              save_restart_path = restarts_folder,
              save_history_folder = f'{output_prefix}/Outputs_phys')
        tot_failures += n_failures
        print(f"================================== CURRENT RUN : {n}, {end_date}")

    print(f'Total of files not generated : {tot_failures}')
