all: test

Dockerfile.ok Dockerfile.warn_root Dockerfile.bad_array:
	@echo "\033[1;34mlinting $@\033[0m"
	@-python lint.py < fixtures/$@
	@echo "\033[1;32mOK\033[0m" # heh... ignoring $$?

test: Dockerfile.ok Dockerfile.warn_root Dockerfile.bad_array
	@echo "\033[1;32mdone\033[0m"

.PHONY: Dockerfile.* test all
