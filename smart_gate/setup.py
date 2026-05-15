from setuptools import find_packages, setup

package_name = 'smart_gate'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rpi',
    maintainer_email='rpi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ultrasonic_node = smart_gate.ultrasonic_node:main',
            'dht_node = smart_gate.dht_node:main',   # 추가 필요시
            'cds_node = smart_gate.cds_node:main',   # 추가 필요시
            'controller_node = smart_gate.controller_node:main',
            'stepper_node = smart_gate.stepper_node:main',
            'led_node = smart_gate.led_node:main',   # 추가 필요시
        ],
    },
)
