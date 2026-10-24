import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('line_follower_bot')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    urdf_file = os.path.join(pkg_share, 'urdf', 'line_follower_bot.urdf')
    with open(urdf_file, 'r', encoding='utf-8') as f:
        robot_description = f.read()

    params_file = os.path.join(pkg_share, 'config', 'line_follower_params.yaml')
    default_world = os.path.join(pkg_share, 'worlds', 'hexagon_0_5.sdf')

    world = LaunchConfiguration('world')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    yaw = LaunchConfiguration('yaw')

    args = [
        DeclareLaunchArgument(
            'world',
            default_value=default_world,
            description='Absolute path to the world .sdf file',
        ),
        DeclareLaunchArgument('x', default_value='0.0', description='Spawn x [m]'),
        DeclareLaunchArgument('y', default_value='0.0', description='Spawn y [m]'),
        DeclareLaunchArgument('yaw', default_value='0.0', description='Spawn yaw [rad]'),
    ]

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': ['-r ', world],
            'on_exit_shutdown': 'true',
        }.items(),
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-name', 'line_follower_bot',
            '-topic', 'robot_description',
            '-x', x,
            '-y', y,
            '-z', '0.06',
            '-Y', yaw,
        ],
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
        ],
    )

    follower = Node(
        package='line_follower_bot',
        executable='line_follower_node',
        name='line_follower_node',
        output='screen',
        parameters=[params_file, {
            'use_sim_time': True,
            'open_end_recovery': ParameterValue(
                PythonExpression(["'s_loop_open' in '", world, "'"]),
                value_type=bool,
            ),
        }],
    )

    camera = Node(
        package='line_follower_bot',
        executable='camera_node',
        name='camera_node',
        output='screen',
        parameters=[{'use_sim_time': True}],
    )

    return LaunchDescription(
        args
        + [
            gz_sim,
            rsp,
            bridge,
            TimerAction(period=3.0, actions=[spawn]),
            camera,
            follower,
        ]
    )
