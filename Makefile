all: dm

dm: dm.c

install:
	ln -sf ~/pub/KeyRemap4MacBook-private.xml ~/Library/Application\ Support/KeyRemap4MacBook/private.xml

clean:
	rm -f *~
