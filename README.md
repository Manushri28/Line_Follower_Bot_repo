circle_0_5.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
grep -A4 'name="camera_joint"' $I/urdf/robot.urdf | grep "<origin"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/circle_0_5.sdf x:=0.0 y:=0.0 z:=0.05 yaw:=0.0



circle_1_0.sdf - 

export PYTHONNOUSERSITE=1
grep -n -E '<model name|<pose>|<radius>' $PKG/worlds/circle_1_0.sdf | tail -6
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/circle_1_0.sdf x:=0.0 y:=0.0 z:=0.05 yaw:=0.0



circle_2_5.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/hexagon.sdf x:=1.0 y:=0.0 z:=0.05 yaw:=0.0



hexagon.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/hexagon.sdf x:=1.0 y:=0.0 z:=0.05 yaw:=0.0



hexagon_0_5.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/hexagon_0_5.sdf x:=0.25 y:=0.0 z:=0.05 yaw:=0.0



hexagon_1_0.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/hexagon_1_0.sdf x:=0.5 y:=0.0 z:=0.05 yaw:=0.0



line.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/line.sdf x:=0.3 y:=0.0 z:=0.05 yaw:=0.0



loop0.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/loop0.sdf x:=1.0 y:=0.0 z:=0.05 yaw:=0.0



loop1.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/loop1.sdf x:=2.0 y:=0.0 z:=0.05 yaw:=0.0



s_loop_open.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/s_loop_open.sdf x:=9.5 y:=10.0 z:=0.05 yaw:=3.1416



square_2_5.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/square_2_5.sdf x:=1.25 y:=0.0 z:=0.05 yaw:=0.0



square.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/square.sdf x:=0.5 y:=0.0 z:=0.05 yaw:=0.0



triangle.sdf - 

export PYTHONNOUSERSITE=1
pkill -f "gz sim"; sleep 3
source /opt/ros/jazzy/setup.bash; source $WS/install/setup.bash
I=$WS/install/line_follower_bot/share/line_follower_bot
echo "launch loads: $(grep -o "line_follower_bot.urdf\|robot.urdf" $I/launch/sim.launch.py | head -1)"
ros2 launch line_follower_bot sim.launch.py world:=$PKG/worlds/triangle.sdf x:=1.5 y:=0.0 z:=0.05 yaw:=0.0