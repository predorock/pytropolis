
. scripts/clean.sh

export PYT_HOME_DIR=volumes/pytropolis/
mkdir -p $PYT_HOME_DIR
python app.py --debug $1