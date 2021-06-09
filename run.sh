docker build . -t the_chess_game
docker run -it --rm --user=$(id -u $USER):$(id -g $USER) --env="DISPLAY" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --device /dev/snd the_chess_game
