#.PHONY: build run clean

#run:
#	docker run -t -i sublinear
#build:
#	docker build -t sublinear .
#clean:
#	echo "TO DO- Cleanup"
#init:
#	pip install -r requirements.txt
#test:
#	py.test tests
all:
	g++ -c -fPIC utility/hash.cpp -o build/hash.o
	g++ -shared -Wl,-install_name,libhash.so -o build/libhash.so  build/hash.o
