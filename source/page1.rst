Some docs
===========
This is chess. The module consists of two submodules:

.. toctree::
   backend-docs
   frontend-docs

Frontend is the part that interracts with user, manages graphics and sound.
Backend is the brain of this whole thing.

Can be run as a module

.. code-block:: python

	python3 -m chess

directly

.. code-block:: python

	python3 ./chess/main.py

or even from another file:

.. code-block:: python
	:emphasize-lines: 0

	python3 -c '__import__("chess.main").main.Game().start()'





Also license:

.. toctree::
   license


