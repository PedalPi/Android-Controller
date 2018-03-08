WebService Serial
=================

.. image:: https://travis-ci.org/PedalPi/WebServiceSerial.svg?branch=master
    :target: https://travis-ci.org/PedalPi/WebServiceSerial
    :alt: Build Status

.. image:: https://codecov.io/gh/PedalPi/WebServiceSerial/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PedalPi/WebServiceSerial
    :alt: Code coverage


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

Also is necessary install the `Android Debug Bridge (adb)`_
for communication between the Pedal Pi and a Android device. In a Linux like, execute

.. code-block:: bash

    sudo apt-get install android-tools-adb

.. _Android Debug Bridge (adb): https://developer.android.com/studio/command-line/adb.html

In embedded systems, the WebService Serial will try to download an adb pre-build
if the adb is not installed on the device.

Also, is possible compile the adb. See https://github.com/PedalPi/adb-arm

How to use
----------

Like described in `Application documentation`_, create a ``start.py``
and register  WebService Serial component. Is necessary that **WebService Serial**
be registered after the **WebService** (WebService is dependency of WebService Serial
and it will be installed when WebService Serial is installed).

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


WebService Serial now has been configured to connect with a Android device that are
installed a app compatible with it. If haven't installed a app in your device, is recommended
the `Pedal Pi - Display View`_. With Display View, is possible manages the current pedalboard
quickly by a Android device connected with Pedal Pi by the USB. Read your recommendations for
details how to configure the device to enable the communication between the devices
over USB.

.. _Pedal Pi - Display View: https://play.google.com/store/apps/details?id=io.github.com.pedalpi.displayview

Protocol
--------

`WebService Serial` provides a way to communicate with ``WebService`` through a serial connection.

`WebService Serial` provides a TCP client. For communication with a device, is necessary that
the device implements a socket TCP server listening the port ``8888``.

The communication are based in messages from device to the Pedal Pi (``Request`` messages)
and messages from Pedal Pi to the device (``Response`` and ``Event`` messages)

``Request`` Message
~~~~~~~~~~~~~~~~~~~

With ``Request`` Message, a device can request data. The message format has the following format::

    <IDENTIFIER> <METHOD> <URL>\n<DATA>\nEOF\n

::

    <IDENTIFIER> <METHOD> <URL>
    <DATA>
    EOF
    [empty line here]

The communication are described here. For the possible command lists,
see the `WebService documentation`_.

-  ``<IDENTIFIER>``: ``int`` Unique id that defines the request. This value will be used in a response message, identifying the original request message;
-  ``<METHOD>``: ``string`` Possible values are:

  + ``GET``, ``POST``, ``PUT``, ``DELETE`` Based in the `WebService documentation`_;
  + ``SYSTEM`` Informs custom system messages. Actually this isn't used;

-  ``<DATA>``: Json data. If none, send an empty string;
-  ``<URL>``: Resource identifier. Is necessary to informs the API version too (``/v1/<resouce>``). For the full list of resource, see http://pedalpi.github.io/WebService/
-  ``EOF``: The string “EOF”.

Example `Set the current pedalboard`_: ::

    1 PUT /v1/current/bank/1/pedalboard/3

    EOF

.. _Set the current pedalboard: http://pedalpi.github.io/WebService/#current-management-manages-the-current-pedalboard-put

``Response`` Message
~~~~~~~~~~~~~~~~~~~~

``Response`` messages contains a response of a request. For identify the
respective request, see the identifier. The message format has the following format::

    <IDENTIFIER> RESPONSE <DATA>\n

-  ``<IDENTIFIER>``: ``int`` A response returns the same Unique id that the respective request informs;
-  ``RESPONSE``: ``string`` The string “RESPONSE”;
-  ``<DATA>``: ``string`` Json encoded data. If none, it will be an empty string;

``Event`` Message
~~~~~~~~~~~~~~~~~

Changes that modify the Pedal Pi event can be applied by others Components. An example is
`Raspberry P0`_, that contains two buttons that when pressed changes the current pedalboard.
To maintain the application integrity, WebService Serial will send ``Event`` messages informing
the changes.

This corresponds the WebService `websocket data notifications`_.

.. _Raspberry P0: https://github.com/PedalPi/Raspberry-P0
.. _websocket data notifications: http://pedalpi.github.io/WebService/#websocket

A ``Event`` message format is::

    <IDENTIFIER> EVENT <DATA>\n

- ``EVENT``: ``string`` The string “EVENT”;
- ``<DATA>``: ``string`` Json encoded data. If none, it will be an empty string;

.. _WebService: https://github.com/PedalPi/WebService
.. _DisplayView: https://github.com/PedalPi/DisplayView
.. _Application documentation: http://pedalpi-application.readthedocs.io/en/latest/
.. _WebService documentation: http://pedalpi.github.io/WebService/

Development
===========

Install locally to develop::

    python setup.py develop

See makefile options::

    make help
