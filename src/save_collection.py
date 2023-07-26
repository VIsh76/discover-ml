# Cleanest way :
# 1) Read collections in HISTORY.rc
# 2) Read Date in CAP.rc
# 3) Find corresponding output file name
# 4) Copy that file somewhere it isnt overwritten
import warnings
import datetime
import os


def main(input_file, output_file):
    """Copy the variables from input_path to output_path, 
    input path and out path must be formatted with the corresponding
    variable. The file must correspond to HISTORY.rc
    The output directory is created if it doesnt exists

    Args:
        input_path (str): file where HISTORY.rc save variables
        output_path (str): file directory 
        list_of_vars (list of str): variables from HISTORY.rc files.
    """
    output_folder = os.path.dirname(output_file)
    if not os.path.exists(output_folder):
        print(f"Making {output_folder}")
        os.makedirs(output_folder, exist_ok=True)
    if os.path.exists(input_file):            
        print(f"Moving file from {input_file} to {output_file}")
        os.rename(input_file, output_file)
        print("- successful - ")
    else:
        warnings.warn(f"File {input_file} not found - skip can't copy to {output_file}")
