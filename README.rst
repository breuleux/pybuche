
Buche
=====

Helper package to pretty-print and interact with Python objects using the Buche_ logger.

The package includes a repl and a debugger.

Requires Python >= 3.6


Usage
-----

You must install Buche_ first, either from the release_ or through npm (``npm install -g buche``). This package helps interact with Buche, but it is not the application itself. Once you have written your script, use it as follows:

.. code:: bash

    python -m buche yourscript.py

Alternatively, using ``buche`` directly:

.. code:: bash

    buche python -u yourscript.py

.. _Buche: https://github.com/breuleux/buche
.. _release: https://github.com/breuleux/buche/releases



Display
-------

Here's an example of what you can do with Buche. You can run this code using `buche python3 examples/demo.py`.

.. code:: python

    from buche import buche, H

    # You don't have to set a template, but if you do, it must be the
    # very first command you emit, before any printing.
    # You can also give `src=<path-to-file>` instead of `content=...`
    buche.command_template(content=H.div['my-template'](address="/"))

    # Use this command to add styles, stylesheets, scripts, etc.
    buche.command_resource(content=H.style(
        """
        .my-template {
            background-color: #eee;
            padding: 5px;
            display: flex;
            flex-direction: column;
            align-items: start;
        }
        """
    ))

    # Display simple HTML
    buche.html.h3('Welcome!')

    # Display objects
    buche(1234)
    buche([x * x for x in range(100)])
    buche.dict(avocado="green", banana="yellow", cherry="red")

    # Open automatically creates an address for an element
    div1 = buche.open.div(style="border: 3px solid red")

    # You can also set an address explicitly
    buche.html.div(address='/two', style="border: 3px solid blue")

    # Get a printer for the given address
    div2 = buche['/two']

    # These objects will go in the divs
    div1('One')
    div2('Two')
    div1('One again')

    # Handy tabs component
    grocery_list = buche.open.boxTabs()
    fruit = grocery_list.open.tabEntry(
        label='Fruits',
        active=True,
    )
    vegetable = grocery_list.open.tabEntry(
        label='Veggies',
    )

    fruit.html.div(H.s("Pineapple"))
    fruit.html.div("Raspberry")
    fruit.html.div("Grape")

    vegetable.html.div("Carrot")
    vegetable.html.div("Potato")
    vegetable.html.div("Yam")

    # Customize the representation of a class
    class Color:
        def __init__(self, r, g, b):
            self.r = r
            self.g = g
            self.b = b

        def __hrepr__(self, H, hrepr):
            sz = hrepr.config.swatch_size or 20
            return H.div(
                style=f'display:inline-block;width:{sz}px;height:{sz}px;margin:2px;'
                    f'background-color:rgb({self.r},{self.g},{self.b});'
            )

    # This will call __hrepr__
    buche(Color(255, 0, 0))

    # Configuration values can be anything and are propagated recursively
    buche(Color(0, 0, 255), swatch_size=50)

    # You can evaluate JavaScript on elements
    button = buche.open.button("Tickle me")
    button.command_eval(expression="this.onclick = () => alert('Hihihihi!')")


Repl
----

You can start an interactive evaluator very easily:

.. code:: python

    # repl.py
    from buche import repl
    repl.start()

Run ``buche python3 repl.py`` and you will get an empty window and an input box at the bottom. You can evaluate Python expressions in the input box and get very pretty output, and you can also click on the representations of the objects in order to put them in temporary variables.

Note: ``start`` is non-blocking. For a blocking version you can do this:

.. code:: python

    from buche import repl
    repl.start(synchronous=True)
    repl.query()  # Processes a single command, blocking


Debugger
--------

By setting the environment variable ``PYTHONBREAKPOINT`` to ``buche.breakpoint``, calls to the builtin ``breakpoint()`` will use Buche's repl for debugging. You can use it essentially the same way as ``pdb``, but you get pretty HTML printing.

.. code:: bash

    PYTHONBREAKPOINT=buche.breakpoint buche python3 mycode.py

This variable is automatically set when you run a script with ``python -m buche``.
