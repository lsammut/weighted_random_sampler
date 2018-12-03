=======================
Weighted Random Sampler
=======================


Generate weights for Vose Alias sampling.


Application
--------

Applied to fair sampling for single or multiple Advent Calendars.
Outputs list of names selected randomly but fairly given calendar preferences and availabilities.


Usage
-------

* Clone repository
* Edit availability and preference data
* start pipenv: ``pipenv shell``
* Run ``python weighted_sampler.py`` from ``weighted_random_sampler`` directory to output list of names selected
randomly but fairly.



Credits
-------

This package relies on the Vose Alias sampling method package_ as implemented by `asmith26/Vose-Alias-Method`_

.. _asmith26/Vose-Alias-Method: https://github.com/asmith26/Vose-Alias-Method
.. _package: https://pypi.org/project/Vose-Alias-Method/

and was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



