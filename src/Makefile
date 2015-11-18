# Makefile
# ajdiaz, 2015-10-22 21:58


components: pyload xlib.zip
	@cp pyload xlib.zip python ../pyload/resources/

pyload:
	@./build

xlib.zip: pyload

clean:
	@./build clean
	@rm -f ../pyload/resources/pyload
	@rm -f ../pyload/resources/python
	@rm -f ../pyload/resources/xlib.zip

reset: clean
	@./build reset

install: components
	pip install -U ./src


# vim:ft=make
