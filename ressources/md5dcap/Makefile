.PHONY:all 

# make sure that libdcap is in your LD_LIBRARY_PATH
DCAP_PATH=/opt/products
CFLAGS=-I${DCAP_PATH}/include -D_GNU_SOURCE -g
LDFLAGS=-L${DCAP_PATH}/lib64 -lssl -ldcap 

all: md5dcap

clean:
	-rm md5dcap

md5dcap: md5dcap.c
	gcc ${CFLAGS} ${LDFLAGS} -o md5dcap md5dcap.c
	chmod +x md5dcap
