=============
ckanext-opengovharvester
=============

.. A CKAN Harvester extension that downloads the associated resource files,
 uploads to destination CKAN instance via FileStore API and updates resource URLs of the harvested datasets.


------------
Requirements
------------

This extension requires an installation of CKAN. To install and set up CKAN, visit CKAN Documentation



------------
Installation
------------

To install ckanext-opengovharvester:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-opengovharvester Python package into your virtual environment::

     pip install ckanext-opengovharvester

3. Add ``opengovharvester`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

    # Configure user API key in the CKANHarvester `Configuration` JSON for uploading to destination CKAN instance

    {..., "ckan_api_key": ""}

------------------------
Development Installation
------------------------

To install ckanext-opengovharvester for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/codefortanzania/ckanext-opengovharvester.git
    cd ckanext-opengovharvester
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.opengovharvester --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-opengovharvester on PyPI
---------------------------------

ckanext-opengovharvester should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-opengovharvester. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-opengovharvester
----------------------------------------

ckanext-opengovharvester is availabe on PyPI as https://pypi.python.org/pypi/ckanext-opengovharvester.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
