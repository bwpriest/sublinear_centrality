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
	g++ -c -fPIC utility/mashash.cpp -o build/mashash.o
	g++ -shared -Wl,-install_name,libmashash.so -o build/libmashash.so  build/mashash.o
