import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'line_follower_bot'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (os.path.join('share', package_name, 'meshes'), glob(os.path.join('meshes', '*.stl'))),
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (
            os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.[pxy][yma]*')),
        ),
        (
            os.path.join('share', package_name, 'urdf'),
            glob(os.path.join('urdf', '*')),
        ),
        (
            os.path.join('share', package_name, 'worlds'),
            glob(os.path.join('worlds', '*')),
        ),
        (
            os.path.join('share', package_name, 'config'),
            glob(os.path.join('config', '*')),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='you@example.com',
    description='PID + OpenCV line follower for a differential drive robot in Gazebo Harmonic',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_node = line_follower_bot.camera_node:main',
            'line_follower_node = line_follower_bot.line_follower_node:main',
        ],
    },
)
