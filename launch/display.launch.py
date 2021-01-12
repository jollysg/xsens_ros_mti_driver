import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    ld = LaunchDescription()

    # Set env var to print messages to stdout immediately
    arg = SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1')
    ld.add_action(arg)
    
    driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            launch_file_path=PathJoinSubstitution([
                FindPackageShare('xsens_mti_driver'), 'launch', 'xsens_mti_node.launch.py'
                ]),
            )
        )
    ld.add_action(driver_launch)

    # Robot State Publisher node
    urdf_file_path = os.path.join(get_package_share_directory('xsens_mti_driver'), 'urdf', 'MTI_10.urdf')
    state_publisher_node = Node(
        package='robot_state_publisher',
        node_executable='robot_state_publisher',
        node_name='xsens_state_publisher',
        output='screen',
        arguments=[urdf_file_path],
    )
    ld.add_action(state_publisher_node)

    # Rviz2 node
    # rviz_config_path = os.path.join(get_package_share_directory('xsens_mti_driver'), 'rviz', 'display.rviz')
    # rviz2_node = Node(
    #     package='rviz2',
    #     node_executable='rviz2',
    #     node_name='xsens_rviz2',
    #     output='screen',
    #     arguments=[["-d"],[rviz_config_path]],
    # )
    # ld.add_action(rviz2_node)

    return ld