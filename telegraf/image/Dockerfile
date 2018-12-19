FROM alpine:3.8

ENV TELEGRAF_VERSION 1.8.3

RUN apk --no-cache add ca-certificates

RUN apk add --no-cache --virtual .build-deps dep git glide go make musl-dev && \
    go get -d github.com/influxdata/telegraf && \
    ( \
        cd /root/go/src/github.com/influxdata/telegraf ; \
        git checkout ${TELEGRAF_VERSION} ; \
        make PREFIX=/usr COMMIT= BRANCH= VERSION=${TELEGRAF_VERSION} ; \
        install -Dm755 telegraf /usr/bin/telegraf \
    ) && \
    rm -rf /root/go && \
    apk del .build-deps

ENTRYPOINT ["/usr/bin/telegraf"]