# Registry и образ
REGISTRY   := ghcr.io
USER       := goodwill-v
IMAGE_NAME := autodeploy_fastapi
IMAGE      := $(REGISTRY)/$(USER)/$(IMAGE_NAME)

# Версия: из git-тега или переменной VERSION, иначе 0.0.1
VERSION    ?= $(shell git describe --tags --always --dirty 2>/dev/null || echo "0.0.1")

# Убрать префикс v из версии (v1.0.0 -> 1.0.0)
VERSION    := $(patsubst v%,%,$(VERSION))

.PHONY: login build push build-push commit help

help:
	@echo "Использование:"
	@echo "  make login       - авторизация в $(REGISTRY) (передать токен: echo \$$GH_PAT | make login)"
	@echo "  make build       - сборка образа $(IMAGE):$(VERSION) и $(IMAGE):latest"
	@echo "  make push        - пуш образов с тегами $(VERSION) и latest"
	@echo "  make build-push  - сборка и пуш (login нужно выполнить отдельно)"
	@echo "  make commit      - git init, add ., commit, branch main, push (MSG=\"тест_Х\" или make commit MSG=\"ваше сообщение\")"
	@echo ""
	@echo "Переменные: VERSION=$(VERSION), IMAGE=$(IMAGE)"

login:
	@echo "Логин в $(REGISTRY)..."
	docker login $(REGISTRY) -u $(USER) --password-stdin

build:
	docker build -t $(IMAGE):$(VERSION) -t $(IMAGE):latest .

push: build
	docker push $(IMAGE):$(VERSION)
	docker push $(IMAGE):latest
	@echo "Опубликовано: $(IMAGE):$(VERSION) и $(IMAGE):latest"

build-push: login
	@$(MAKE) push

# Сообщение коммита по умолчанию (переопределить: make commit MSG="ваше сообщение")
MSG ?= тест_Х

commit:
	git init
	git add .
	git commit -m "commit: $(MSG)"
	git branch -M main
	git push -u origin main
