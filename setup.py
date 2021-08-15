import setuptools
    
setup(
    name='lb_lists',
    version='0.1.0',    
    description='a package for Letterboxd list comparison',
    url='https://github.com/RMNT/lb_lists',
    author='Raminta Urbonavičiūtė',
    author_email='urbonaviciuteraminta@gmail.com',
    license='MIT',
    packages=['lb_lists'],
    install_requires=['mpi4py>=2.0',
                      'numpy', 're', 'requests', 'bs4', 'os', 'random', 'time'                     
                      ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
