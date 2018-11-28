# IoT setup

## Quick-Ref

Start:

    docker-compose up -d

View logs:

    docker-compose logs -f --tail=10

Restart:

    docker-compose restart

Example `docker-compose.override.yml`:

    version: '2'
    services:
      opensensemap:
        command: ["58d42511c877fb0011ad4597"]
      homekit2mqtt:
        command: ["-b", "Bridge Name", "-a", "username", "-c", "000-00-000"]
      mirobo:
        environment:
          - MIROBO_TOKEN=...
          - MIROBO_IP=...
