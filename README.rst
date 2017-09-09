GeoTagger
#########

Geotag your photos from GPS-less cameras with your phone's location
history data.


.. image:: https://github.com/jakubroztocil/geotagger/raw/master/geotagger.png
    :alt: GeoTagger
    :align: center


Is it for me?
=============

* Do you take photos with a camera without a GPS tracking feature?
* Do you have https://moves-app.com/ installed on your phone?
* Do you want to have your photos geotagged?

…if your answer is 3x yes, then this tool is for you.


How does it work?
=================

* You already walk around with your location-aware phone and Moves
  records your location.
* You snap photos with your GPS-less camera.
* GeoTagger uses the creation timestamps from photos
  to find your location at the time of taking them in your Moves log.
* GeoTagger is able to retrospectively add GEO tags to even old photos,
  as long as your location for the period is logged with Moves.


How is it implemented?
======================

When you ask GeoTagger to tag your photos, this process takes places:

1. Unique creation dates are extracted from the photo files.
2. Your Moves history for those days is fetched from the Moves API.
3. A `GPX <https://en.wikipedia.org/wiki/GPS_Exchange_Format>`_ file is
   generated from the data.
4. ``exiftool -geotag`` is used behind to scene to apply that location
   log to your photos.


Status
======

Beta quality.


Installation
============

1. `Install <http://www.sno.phy.queensu.ca/~phil/exiftool/install.html>`_
   ``exiftool``, for example, with: ``$ brew install exiftool``
2. Install ``geotagger`` from PyPi with: ``$ pip install geotagger``


Usage
=====

See ``$ geotagger --help`` and ``$ geotagger sub-command --help``.


Moves authentication
--------------------

1. Create a new app under your Moves account: https://dev.moves-app.com/apps/new
2. Specify ``http://127.0.0.1:7777/redirect`` as ``Redirect URI``.
3. Create ``~/.geotagger.json`` with credentials for your app:
   ``{"MOVES_ID": "<CLIENT_ID>", "MOVES_SECRET": "<CLIENT_SECRET>"}``
4. Run ``geotagger auth`` and follow the instruction to authenticate the app.


Geotagging
----------

Geotag all images in a folder:

.. code-block:: bash

    $ geotagger tag ./photos

You can also just generate a GPX log for the dates without applying it:

.. code-block:: bash

    $ geotagger gpx ./photos > log.gpx

The ``tag`` sub-command also optionally accepts a path to a GPX log file:

.. code-block:: bash

    $ geotagger tag ./photos log.gpx


TODO
====

* Improve UX: simplify installation and setup
* Make the external metadata updates play well with photos already imported to Lightroom
* Add Geosync support http://www.sno.phy.queensu.ca/~phil/exiftool/geotag.html#geosync
* Consider Electron-based GUI app
* Consider additional GPS log sources than Moves


Changelog
=========

0.0.3 (2017-09-09)
------------------

* Fixed ``missing configuration: MOVES__ID`` #1


Contact
=======

Jakub Roztocil

* https://github.com/jakubroztocil
* https://twitter.com/jakubroztocil
* https://roztocil.co


Contribute
==========

* https://github.com/jakubroztocil/geotagger


Licence
=======

MIT. See `LICENCE <./LICENCE>`_.
