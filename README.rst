WebService Serial
=================

WebService Serial disposes the `WebService`_ communication via TCP
Serial communication.

With it, is possible:

-  Use `DisplayView`_, an Android application that provides pedalboard
   data for live presentations. Your focus is a speed management in live
   performances.


**Documentation:**
   https://github.com/PedalPi/WebServiceSerial

**Code:**
   https://github.com/PedalPi/WebServiceSerial

**Python Package Index:**
   https://pypi.org/project/PedalPi-WebServiceSerial

**License:**
   `Apache License 2.0`_

.. _Apache License 2.0: https://github.com/PedalPi/WebServiceSerial/blob/master/LICENSE

~How to use~ FIXME
------------------

Like described in `Application documentation`_, create a ``start.py``
and register AndroidController component.

.. code:: python

    import sys
    import tornado

    # DEPRECATED
    sys.path.append('application')
    sys.path.append('android_controller')

    from application.Application import Application
    from android_controller.android_controller import AndroidController

    address = 'localhost'
    port = 3000

    application = Application(path_data="data/", address=address, test=True)
    application.register(AndroidController(application, "adb"))

    application.start()

    tornado.ioloop.IOLoop.current().start()

Dependencies
~~~~~~~~~~~~

**WebService Serial** requires ``Tornado >= 4.2`` for TCP connection.

For communication with Android (over USB), also needs ``adb``.

If you uses in a ARM architecture, maybe will be necessary compile
**adb**. In these cases, the project https://github.com/PedalPi/adb-arm
can help you. **adb-arm** PedalPi *fork* already contains some binaries
for RaspberryPi.

Protocol
--------

The communication are described here. For the possible command lists,
see the `WebService documentation`_.

Request
~~~~~~~

::

    <METHOD> <URL>\n
    <DATA>\n
    EOF\n

-  ``<METHOD>``: ``GET``, ``POST``, ``PUT``, ``DELETE``, ``SYSTEM``
-  ``<DATA>``: Json data. If none, send ``'{}'``
-  ``<URL>``: http://pedalpi.github.io/WebService/
-  ``EOF``: The string “EOF”.

Example:

::

    PUT /current/bank/1/pedalboard/3
    {}
    EOF

Response
~~~~~~~~

::

    RESPONSE <DATA>

-  ``RESPONSE``: String ``RESPONSES``;
-  ``<DATA>``: Json data. If none, send ``'{}'``

Notification
~~~~~~~~~~~~

This corresponds the websocket data notifications

::

    EVENT <DATA>

-  ``EVENT``: String ``EVENT``
-  ``<DATA>``: Json data. If none, send ``'{}'``

Initialization
~~~~~~~~~~~~~~

After the connection has been realized,

1. Application send

::

    SYSTEM /
    {"message": "connected"}
    EOF

After initialization
~~~~~~~~~~~~~~~~~~~~

The connected device can be request thinks, like:

-  The current pedalboard number

::

    GET /v1/current
    {}
    EOF

-  Response

::

    RESPONSE { "bank": 1, "pedalboard": 0 }

-  The pedalboard data

::

    GET /v1/bank/1/pedalboard/0
    {}
    EOF

-  Response

::

    RESPONSE { "name": "My pedalboard", "effects": [], "connections": [], "data": {} }

.. _WebService: https://github.com/PedalPi/WebService
.. _DisplayView: https://github.com/PedalPi/DisplayView
.. _Application documentation: http://pedalpi-application.readthedocs.io/en/latest/
.. _WebService documentation: http://pedalpi.github.io/WebService/

Scripts
=======

Install locally to develop
python setup.py develop
