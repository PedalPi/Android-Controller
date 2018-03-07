WebService Serial
=================

WebService Serial disposes the `WebService`_ communication via TCP
Serial communication.

With it, is possible:

- Use `DisplayView`_, an Android application for manages quickly the
  current pedalboard. Ideal for adjusting live performances and band
  rehearsal.

**Documentation:**
   https://github.com/PedalPi/WebServiceSerial

**Code:**
   https://github.com/PedalPi/WebServiceSerial

**Python Package Index:**
   https://pypi.org/project/PedalPi-WebServiceSerial

**License:**
   `Apache License 2.0`_

.. _Apache License 2.0: https://github.com/PedalPi/WebServiceSerial/blob/master/LICENSE

Installation
------------

Install with pip:

.. code-block:: bash

    pip install PedalPi-PluginsManager

Dependencies
~~~~~~~~~~~~

**WebService Serial** requires ``Tornado >= 4.2`` for TCP connection.

For communication with Android (over USB), also needs ``adb``.

If you uses in a ARM architecture, maybe will be necessary compile
**adb**. In these cases, the project https://github.com/PedalPi/adb-arm
can help you. **adb-arm** PedalPi *fork* already contains some binaries
for RaspberryPi.

How to use
----------

Like described in `Application documentation`_, create a ``start.py``
and register AndroidController component.

.. code:: python

    # Imports application
    from application.application import Application

    address = 'localhost'
    application = Application(path_data="data/", address=address)

    # Register WebService before WebServiceSerial
    from webservice.webservice import WebService
    application.register(WebService(application))

    # Register WebServiceSerial after WebService
    from webservice_serial.webservice_serial import WebServiceSerial
    from webservice_serial.target.android.android_display_view import AndroidDisplayView

    target = AndroidDisplayView()
    application.register(WebServiceSerial(application, target))

    # Start Application
    application.start()

    import tornado
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        application.stop()



Protocol
--------

The communication are described here. For the possible command lists,
see the `WebService documentation`_.

Request
~~~~~~~

::

    <IDENTIFIER> <METHOD> <URL>\n
    <DATA>\n
    EOF\n

-  ``<IDENTIFIER>``: ``int`` that informs the request
                     Responses will have the same identifier;
-  ``<METHOD>``: ``GET``, ``POST``, ``PUT``, ``DELETE``, ``SYSTEM``
-  ``<DATA>``: Json data. If none, send ``'{}'``
-  ``<URL>``: http://pedalpi.github.io/WebService/
-  ``EOF``: The string “EOF”.

Example:

::

    1 PUT /current/bank/1/pedalboard/3

    EOF

Response
~~~~~~~~

::

    <IDENTIFIER> RESPONSE <DATA>

-  ``<IDENTIFIER>``: ``int``. A response returns the same ``int`` that the request
                              informs;
-  ``RESPONSE``: String ``RESPONSES``;
-  ``<DATA>``: Json data. If none, send ``''``

Notification
~~~~~~~~~~~~

This corresponds the websocket data notifications

::

    <IDENTIFIER> EVENT <DATA>

-  ``EVENT``: String ``EVENT``
-  ``<DATA>``: Json data. If none, send ``''``

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
