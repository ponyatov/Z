# \ <section:var>
MODULE       = $(notdir $(CURDIR))
OS           = $(shell uname -s)
# / <section:var>
# \ <section:dir>
CWD          = $(CURDIR)
TMP          = $(CWD)/tmp
# / <section:dir>
# \ <section:tool>
WGET         = wget -c
PY           = $(shell which python3)
PIP          = $(shell which pip3)
# / <section:tool>
# \ <section:src>
S += $(MODULE).py
# / <section:src>
# \ <section:all>
.PHONY: all
all: $(PY) $(S)
	$^
# / <section:all>
# \ <section:install>
.PHONY: install
install: $(OS)_install
	$(MAKE) update
.PHONY: update
update: $(OS)_update
.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# / <section:install>

