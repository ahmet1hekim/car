from launch import LaunchDescription

from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import DeclareLaunchArgument,SetEnvironmentVariable,IncludeLaunchDescription
from launch.substitutions import Command,LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from pathlib import Path
def generate_launch_description():
    
    car_description_dir =get_package_share_directory("car_description")
    
    model_arg = DeclareLaunchArgument(name="model",default_value=os.path.join(car_description_dir,"urdf","test.car.urdf.xacro"),description="Absolute path ")
    
    robot_description = ParameterValue(Command(["xacro ",LaunchConfiguration("model")]),value_type=str)
    
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description":robot_description}]
        )
    
    gazebo_resource_path=SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[str(Path(car_description_dir).parent.resolve())]

    )
    gazebo = IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(
        get_package_share_directory("ros_gz_sim"),"launch"),"/gz_sim.launch.py"]),launch_arguments=[("gz_args",[" -v 4"," -r"," empty.sdf"])
        ]
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output= "screen",
        arguments=["-topic","robot_description",
        "-name","car"
        ]
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher_node,
        gazebo_resource_path,
        gazebo,
        gz_spawn_entity


    ])