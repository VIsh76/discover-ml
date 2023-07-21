from src import restart_folder, run_model, save_collection
import datetime
import warnings
import os

# Parameters are here (should be cleanner)
experiment_folder = "/discover/nobackup/vmarchai/experiments/test-c48"
initial_folder = "/discover/nobackup/vmarchai/experiments/test-c48"
experiment_name = 'test-c48'
agcm_nophysic_path = f"{experiment_folder}/AGCM_nophysic.rc"
agcm_physic_path = f"{experiment_folder}/AGCM_physic.rc"
list_of_vars = ['prog.eta']
heart_beat = 450
cap_restart_file = {experiment_folder}/'cap_restart'


def get_dates(cap_restart_file, heart_beat):
    date_str = open(cap_restart_file, 'r').readlines()[0].strip('\n')
    date_beg = datetime.datetime.strptime(date_str, "%Y%m%d %H%M%S")
    t = datetime.timedelta(seconds=heart_beat)
    date_end = date_beg + t
    return date_beg, date_end

if __name__ == '__main__':
    warnings.warn("Currently only support '%y4%m2%d2_%h2%n2z.nc4' format")        
    
    date_beg, date_end = get_dates(cap_restart_file, heart_beat)
    input_path = f"{experiment_folder}/holding/{{var}}/{date_beg.strftime('%Y%m')}/{experiment_name}.{{var}}.{date_end.strftime('%Y%m%d_%H%Mz')}.nc4"
    output_path_phy_yes = f"{experiment_folder}/ml_physics_yes/{{var}}/{date_beg.strftime('%Y%m')}/{experiment_name}.{{var}}.{date_end.strftime('%Y%m%d_%H%Mz')}.nc4"
    output_path_phy_no  = f"{experiment_folder}/ml_physics_no/{{var}}/{date_beg.strftime('%Y%m')}/{experiment_name}.{{var}}.{date_end.strftime('%Y%m%d_%H%Mz')}.nc4"

    print("# No Physic")
    print("## Restart")
    restart_folder.main(experiment_folder, initial_folder)
    print("## Run Model")
    run_model.main(agcm_nophysic_path, False)
    print('## Save files')
    save_collection.main(list_of_vars, input_path, output_path_phy_no)
        
    print("--------------------------")
    print("# No Physic")
    print("## Restart")
    restart_folder.main(experiment_folder, initial_folder)
    print("## Run Model")
    run_model.main(agcm_physic_path, True)
    print('## Save files')
    save_collection.main(list_of_vars, input_path, output_path_phy_yes)
