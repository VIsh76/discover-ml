import os
import datetime

# SHOULD MODIFY HISTORY.rc no to save anything
def main(caprc_path, beg_date_time, delta_time, time_format, heartbeat_dt=450, job_sgmt='00000001 000000'):
    """Set up the experiment folder cap.rc to make it start and run for the corresponding time

    Args:
        caprc_path (str): path of the cap.rc file in the experiment folder
        beg_date_str (str): datetime in time_format
        delta_time (time.timedelta): length of the run
        time_format (str): format of the time of caprc
        heartbeat_dt (int, optional): heartbeat. Defaults to 450.
        job_sgmt (str, optional): job_sgmt. Defaults to '00000001 000000'.

    Returns:
        date.time: end date (new start date)
    """
    end_date_time = beg_date_time + delta_time
    beg_date_str  = beg_date_time.strftime(time_format)
    end_date_str  = end_date_time.strftime(time_format)
    # Write Template
    f = open('templates/CAP_template.rc')
    text = f.read()
    text=text.format(HEARTBEAT_DT=heartbeat_dt, 
                     BEG_DATE=beg_date_str, 
                     JOB_SGMT=job_sgmt, 
                     END_DATE=end_date_str)
    f.close()
    # Save Template
    print(f"Saving {caprc_path} with end date {end_date_str}")
    outfile = open(caprc_path, "w")
    outfile.write(text)
    outfile.close()
    return end_date_time

if __name__=='__main__':
    l = main('cap_test.rc', 
            beg_date_time=datetime.datetime.strptime('20000401 210000', "%Y%m%d %H%M%S"), 
            delta_time=datetime.timedelta(seconds=450),
            time_format= "%Y%m%d %H%M%S")
