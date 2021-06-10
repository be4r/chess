Some docs
===========
Шахматы. Это шахматы. Проект состоит из 2 модулей:

.. toctree::
   backend-docs
   frontend-docs

Фронтенд - часть, с которой взаимодействует пользователь. Реализует графику и немного звук.

Бэкенд - "мозг" всей операции, реализует логику самой игры.

Запускать это все дело можно модулем:

.. code-block:: python

	python3 -m chess

напрямую:

.. code-block:: python

	python3 ./chess/main.py

или даже из другого файла:

.. code-block:: python
	:emphasize-lines: 0

	python3 -c '__import__("chess.main").main.Game().start()'





А тут лицензия:

.. toctree::
   license


