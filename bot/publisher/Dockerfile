FROM python:3.12-slim-bookworm

RUN apt-get update \
 && apt-get install -y --no-install-recommends git openssh-client \
 && rm -rf /var/lib/apt/lists/*

COPY publisher/publisher.py publisher/build_catalog.py /app/
COPY common /app/common
# ssh refuses to run for a uid with no passwd entry, so give uid 1000 a name.
RUN useradd -u 1000 -M -d /tmp -s /usr/sbin/nologin bot \
 && mkdir -p /state/thumbs /state/profile && chown -R 1000:1000 /state

USER 1000:1000
ENV HOME=/tmp \
    PYTHONPATH=/app/common \
    GIT_SSH_COMMAND="ssh -i /run/secrets/deploy_key -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/state/known_hosts"
RUN git config --global --add safe.directory /repo
ENTRYPOINT ["python3", "-u", "/app/publisher.py"]
