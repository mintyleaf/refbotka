GIT_BOTKA = git+https://github.com/mintyleaf/botka@python-version-splits
IMAGE = registry.a1b7a.cc/refbotka
HOST = 7acca

.PHONY: dev prod docker docker-dev push

# Switch to local botka for development
dev:
	uv add --editable ../botka

# Restore git botka before committing / deploying
prod:
	uv add "botka @ $(GIT_BOTKA)"

# Build production image (fetches botka from git)
docker:
	docker build --platform linux/amd64 -t $(IMAGE) .

# Build dev image (uses local ../botka)
docker-dev: dev
	docker build --platform linux/amd64 -f Dockerfile.dev --build-context botka=../botka -t $(IMAGE) .

# Deploy to server
push:
	docker push $(IMAGE)
	ssh $(HOST) "cd ~/7ac/refinance && docker compose pull && docker compose up -d"
