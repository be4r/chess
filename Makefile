install: sphinx babel docker

run:
	docker run -e LANGUAGE="$(lang)" -it --rm --user=$(id -u $USER):$(id -g $USER) --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --device /dev/snd the_chess_game


COMPILED=chess/po/en/LC_MESSAGES/chess.mo chess/po/ru/LC_MESSAGES/chess.mo chess/uk_UA/en/LC_MESSAGES/chess.mo
SOURCES=$(COMPILED:.mo=.po)

deps:
	 apt update && env DEBIAN_FRONTEND="noninteractive" apt -y install git python3 python3-pip python3-sphinx python3-tk python3-babel python3-pil.imagetk docker.io python3-venv && pip3 install playsound

docker:
	xhost +
	docker build . -t the_chess_game

sphinx:
	sphinx-build source/ build/

babel: $(COMPILED)

$(COMPILED):$(SOURCES)
	pybabel compile -D chess -i chess/po/en/LC_MESSAGES/chess.po -o chess/po/en/LC_MESSAGES/chess.mo
	pybabel compile -D chess -i chess/po/ru/LC_MESSAGES/chess.po -o chess/po/ru/LC_MESSAGES/chess.mo
	pybabel compile -D chess -i chess/po/uk_UA/LC_MESSAGES/chess.po -o chess/po/uk_UA/LC_MESSAGES/chess.mo

$(SOURCES):chess/po/chess.pot
	pybabel update -D chess -o chess/po/en/LC_MESSAGES/chess.po -i chess/po/chess.pot -l en
	pybabel update -D chess -o chess/po/ru/LC_MESSAGES/chess.po -i chess/po/chess.pot -l ru
	pybabel update -D chess -o chess/po/uk_UA/LC_MESSAGES/chess.po -i chess/po/chess.pot -l uk

chess/po/chess.pot: chess/main.py
	pybabel extract -o chess/po/chess.pot chess/main.py
