run:
	python3 main.py

define make_watch
$(eval
$1:
	( TARGET=$$(dir $$@)$$(patsubst $1,%,$$(notdir $$@)); \
	clear; $$(MAKE) $$$$TARGET; true; \
	while inotifywait -q -e modify -e attrib -e move -e move_self -e create -e delete -e delete_self Makefile $$$$(find . -name '*.py' -not -path './env*'); \
	do clear; $$(MAKE) $$$$TARGET; \
	done )
)
endef

$(call make_watch,watch_%)
$(call make_watch,%_watch)
$(call make_watch,%w)
$(call make_watch,%.pyw)

