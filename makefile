BROWSER=firefox
BOLD=\033[1m
NORMAL=\033[0m

default: help

clean: clean-pyc clean-test clean-build clean-docs

clean-build:
	rm -rf .eggs
	rm -rf build
	rm -rf dist

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

clean-test:
	rm -rf .cache
	rm -f .coverage
	rm -rf htmlcov

clean-docs:
	rm -rf docs/build

docs: clean-docs
	cd docs && $(MAKE) html

docs-see: docs
	$(BROWSER) docs/build/html/index.html

install-develop-requirements:
	sudo apt-get install -y portaudio19-dev python-all-dev --no-install-recommends
	sudo apt-get install -y lilv-utils calf-plugins guitarix --no-install-recommends
	sudo apt-get install -y lv2-dev --no-install-recommends
	pip3 install -U setuptools
	pip3 install cffi
	sudo apt-get install -y android-tools-adb --no-install-recommends

install-docs-requirements:
	pip3 install sphinx
	pip install sphinx_rtd_theme

install-tests-requirements:
	pip3 install pytest pytest-cov
	# For midi tests - https://github.com/x42/midifilter.lv2
	cd /tmp && git clone git://github.com/x42/midifilter.lv2.git && \
	cd midifilter.lv2 && \
	make && \
	sudo make install PREFIX=/usr

run:
	@echo "Run option isn't created =)"

test: clean-test
	pytest --cov=webservice_serial

test-docs:
	python -m doctest *.rst -v
	python -m doctest docs/*/*.rst -v

test-details: test
	coverage3 html
	$(BROWSER) htmlcov/index.html

help: cabecalho
	@echo ""
	@echo "Commands"
	@echo "    $(BOLD)clean$(NORMAL)"
	@echo "          Clean files"
	@echo "    $(BOLD)docs$(NORMAL)"
	@echo "          Make the docs"
	@echo "    $(BOLD)docs-see$(NORMAL)"
	@echo "          Make the docs and open it in BROWSER"
	@echo "    $(BOLD)install-develop-requirements$(NORMAL)"
	@echo "          Install the develop requirements"
	@echo "    $(BOLD)install-docs-requirements$(NORMAL)"
	@echo "          Install the docs requirements"
	@echo "    $(BOLD)install-tests-requirements$(NORMAL)"
	@echo "          Install the tests requirements"
	@echo "    $(BOLD)test$(NORMAL)"
	@echo "          Execute the tests"
	@echo "    $(BOLD)test-details$(NORMAL)"
	@echo "          Execute the tests and shows the result in BROWSER"
	@echo "           - BROWSER=firefox"
	@echo "    $(BOLD)help$(NORMAL)"
	@echo "          Show the valid commands"

cabecalho:
	@echo "$(BOLD)==================="
	@echo "> WebService Serial"
	@echo "==================="
	@echo ""
	@echo "Github$(NORMAL): https://pypi.org/project/PedalPi-WebServiceSerial/"
