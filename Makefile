
clean:
	rm -Rf *.egg-info/
	rm -Rf build/
	rm -Rf dbs eggs

lint:
	docker-compose run --rm app pre-commit run --all-files

run_spiders:
	curl http://127.0.0.1:6800/schedule.json -d project=zdmenu_spiders -d spider=menu_spider

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

deploy:
	docker compose run --rm app scrapyd-deploy local

bash:
	docker exec -it zdmenu_scraper_scrapyd_1 bash