FROM alpine:3.8

ENV INFLUXDB_VERISON 1.7.2

RUN apk --no-cache add ca-certificates
RUN apk add --no-cache --virtual .build-deps dep go glide git musl-dev && \
    go get -d github.com/influxdata/influxdb && \
    ( \
        cd /root/go/src/github.com/influxdata/influxdb ; \
        git checkout v${INFLUXDB_VERISON} ; \
        dep ensure -vendor-only ; \
        go install ./cmd/... ; \
        cp docker/entrypoint.sh /entrypoint.sh ; \
        cp docker/init-influxdb.sh /init-influxdb.sh \
    ) && \
    cp /root/go/bin/* /usr/bin/ && \
    rm -rf /root/go && \
    rm -rf /root/.cache && \
    apk del .build-deps

RUN apk --no-cache add bash tzdata
ENTRYPOINT ["/entrypoint.sh"]
CMD ["influxd"]
