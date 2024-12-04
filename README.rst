XScraper
=============

Introduction
------------
With this package you can collect user information, the followers, followings and tweets of a user, and collect tweets by a given hashtag or keyword on the platform X.

The package works with Selenium. You need a X profile, so you can login to the platform. Collection of large datasets might be a bit slow to prevent getting blocked.

Prerequisites
-------------
To install the package, execute the following command::

    $ pip install git+https://github.com/jpfefferlab/xscraper.git

If you want to execute the selenium functions, we recommend you to install any chrome browser on your system first. By this, the start_selenium-function will not use a test browser, but a normal chrome browser, which prevents many troubles when collecting data on X.

To use the XScraper in a project, put the following command in your python script::

    import xscraper

To see how to use the package, you can run the `example.py` script located in the root directory.

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.

Contributions
-------------
This package was developed by Angelina Voggenreiter (angelina.voggenreiter@tum.de) and Idil Sezgin (idil.sezgin@tum.de) as part of the research project 'Understanding, Detecting, and Mitigating Online Misogyny Against Politically Active Women' at the Technical University of Munich. This research project is funded by the Bavarian Research Institute for Digital Transformation (bidt), an institute of the Bavarian Academy of Sciences and Humanities. 