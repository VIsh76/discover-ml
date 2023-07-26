# discover-ml
Python layer of scripts for data generation and run of GEOS on discover.


############
# Commands :
############
##  BLOCK Structure :
- Restart from initial or restart folder
- Change runtime to T
- Run for T time with or without physic
- Can save the Restart file 
- Save/Move the HISTORY physic file (to the corresponding folder)

### Block 1 Setup :
- Restart from init time
- Run for T with physic on
- Save Restart files (RST_INIT)
- Save History Files (Input Data) 

### Block 2 Run No Phy :
- Restart from RST_INIT
- Run for heartbeat with physic off
- X
- Save History Files (Output Data) 

### Block 3 Run Phy :
- Restart from RST_INIT
- Run for heartbeat with physic on
- Save Restart files (RST_INIT)
- Save History Files (Output Data)
