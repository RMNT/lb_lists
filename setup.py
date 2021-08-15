import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='lb_lists',
    version='0.0.3',
    author='Raminta Urbonavičiūtė',
    author_email='urbonaviciuteraminta@gmail.com',
    description='For getting unions of various lists from Letterboxd',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RMNT/lb_lists',
    project_urls = {
        "Bug Tracker":"https://github.com/RMNT/lb_lists/issues"
    },
    license='MIT',
    packages=['lb_lists'],
    install_requires=['requests', 'bs4', 'os', 'time', 'random', 're', 'pyquery', 'numpy'],
)
