FROM python:3.12-slim-bookworm

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt && pip cache purge

ADD ./TwitchChannelPointsMiner ./TwitchChannelPointsMiner
COPY ./run.py ./
ENTRYPOINT [ "python", "run.py" ]
