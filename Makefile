.PHONY: build run clean

run:
	docker run -t -i sublinear
build:
	docker build -t sublinear .
clean:
	echo "TO DO- Cleanup"