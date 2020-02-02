build:
	@docker build --rm -t ncov2019scrapy:dev --build-arg PIP_MIRROR_URL=${MIRROR_URL} . 