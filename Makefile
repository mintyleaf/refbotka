GIT_BOTKA = git+https://github.com/mintyleaf/botka@python-version-splits

.PHONY: dev prod

# Switch to local botka for development
dev:
	uv add --editable ../botka

# Restore git botka before committing
prod:
	uv add "botka @ $(GIT_BOTKA)"
