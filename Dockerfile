FROM python:3.12.1-alpine3.19

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/src

ARG USERNAME=default
ARG GROUPNAME=$USERNAME
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN addgroup -g ${USER_GID} ${GROUPNAME} \
    && adduser -D ${USERNAME} -G ${GROUPNAME} -u ${USER_UID} -h ${HOME} \
    && mkdir -p /etc/sudoers.d \
    && echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

RUN apk update \
    && apk add --no-cache \
    build-base \
    musl-dev \
    postgresql-dev \
    python3-dev \
    && pip install --upgrade pip

WORKDIR ${HOME}
COPY ./requirements.txt ${HOME}/requirements.txt
RUN pip install -r requirements.txt
COPY ./app ${HOME}

USER ${USERNAME}

# EXPOSE 8080

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
