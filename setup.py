from setuptools import setup
setup(
    name = 'nutrition_helper',
    version = '0.0.1',
    packages = ['nutrition_helper'],
    entry_points = {
        'console_scripts': [
            'nutrition_helper= nutrition_helper.__main__:main'
        ]
    })

