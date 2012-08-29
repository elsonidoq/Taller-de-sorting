try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import os.path
src_folder= os.path.join(
    os.path.split(os.path.abspath(__file__))[0], 'src')
setup(
    name='taller_sorting',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "cherrypy",
        "mako"
    ],
    package_dir= {'' : 'src' },
    packages=find_packages(where=src_folder, exclude=['test', 'test.*']),
    package_data={'taller_sorting':['webi/*.ini', 'webi/templates/*', 
                                    'webi/static/css/images/*', 'webi/static/css/*.css', 
                                    'webi/static/images/*', 'webi/static/js/*']},
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    taller-sorting-config = taller_sorting.webi.build_ini:main
    taller-sorting-webi = taller_sorting.webi.controllers:main
    taller-sorting-build-alumni-distr = taller_sorting.build_alumni_distr:main
    """,
)

