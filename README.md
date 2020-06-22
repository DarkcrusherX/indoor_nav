# indoor_nav

Indoor navigation with drone using lidar.

## launch 

[lidar_mapping.launch](https://github.com/DarkcrusherX/indoor_nav/blob/master/launch/lidar_mapping.launch) : For launching px4 drone in gazebo with mavros.

### Mapping phase

[gmapping.launch](https://github.com/DarkcrusherX/indoor_nav/blob/master/launch/gmapping.launch) : To map the indoor and make a map out of it using laserscan data.Only needed in the mapping phase.
rosrun map_server map_saver -f mymap  to save the map.

sudo apt-get install ros-melodic-gmapping

### Navigation phase

[amcl.launcch](https://github.com/DarkcrusherX/indoor_nav/blob/master/launch/amcl.launch) : After loading the map with rosrun map_server map_server mymap.yaml , amcl.launch localizes drone.

sudo apt-get install ros-melodic-amcl

[planner.launch](https://github.com/DarkcrusherX/indoor_nav/blob/master/launch/amcl.launch) : After launching amcl and able to successfully load map and localise , launch move_base for trajectory planning.

sudo apt-get install ros-melodic-move-base

## Parameters

Both local and global parameters required for planner (move_base).

## src

[transmitter.py](https://github.com/DarkcrusherX/indoor_nav/blob/master/src/transmitter.py) : For controlling the drone while mapping.

pip install pygame

[px4_move.py](https://github.com/DarkcrusherX/indoor_nav/blob/master/src/px4_move.py) : For giving setpoint and to subscribe trajectory to publish to mavros.

[localposition.py](https://github.com/DarkcrusherX/indoor_nav/blob/master/src/localposition.py) : To pass odometry value while switching off gps.












