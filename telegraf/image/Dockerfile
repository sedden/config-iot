FROM alpine:3.8
RUN apk --no-cache add ca-certificates
COPY --from=telegraf:1.9 /usr/bin/telegraf /usr/bin/telegraf
ENTRYPOINT /usr/bin/telegraf