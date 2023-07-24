# Cleanest way :
# 1) Read collections in HISTORY.rc
# 2) Read Date in CAP.rc
# 3) Find corresponding output file name
# 4) Copy that file somewhere it isnt overwritten
import warnings
import datetime
import os



def main(list_of_vars, input_path, output_path):
    """Copy the variables from input_path to output_path, 
    input path and out path must be formatted with the corresponding
    variable. The file must correspond to HISTORY.rc
    The output directory is created if it doesnt exists

    Args:
        input_path (str): file where HISTORY.rc save variables
        output_path (str): file directory 
        list_of_vars (list of str): variables from HISTORY.rc files.
    """
    for var in list_of_vars:
        input_file = input_path.format(var=var)
        output_file = output_path.format(var=var)
        output_folder = os.path.dirname(output_file)
        if not os.path.exists(output_folder):
            print(f"Making {output_folder}")
            os.makedirs(output_folder, exist_ok=True)
        if os.path.exists(input_file):            
            print(f"Moving file from {input_file} to {output_file}")
            os.rename(input_file, output_file)
            print("- successful - ")
        else:
            warnings.warn(f"File {input_file} not found - skip {var}")
