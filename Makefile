all: help

help:
	@echo "make dir   # will create the destination directory for rules"
	@echo "make build # will build the container image"
	@echo "make run   # will run the container which create pktables.rules file with updated rules in rules directory"
	@echo "make rules # will do all of the above"

dir:
	@if [ ! -d "rules" ]; then echo "creating rules directory "; mkdir rules ; fi
	
build:
	docker build -t pktables .

run:
	docker run --env-file=env -v `pwd`/rules:/data pktables

rules: dir build run
