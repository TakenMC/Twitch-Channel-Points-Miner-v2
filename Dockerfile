FROM python:3.12-slim-bookworm

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt && pip cache purge

ADD ./TwitchChannelPointsMiner ./TwitchChannelPointsMiner
ADD ./assets ./assets
COPY ./run.py ./
ENTRYPOINT [ "python", "run.py" ]
