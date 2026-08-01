.PHONY: dev test verify

dev:
	docker compose up --build

test:
	cd backend && pytest -q

verify:
	node --check frontend/assets/app.js
