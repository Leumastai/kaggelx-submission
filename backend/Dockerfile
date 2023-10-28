FROM python:3.10.2

RUN apt-get update
RUN apt-get install --reinstall -y build-essential
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y cmake

ENV INSTALL_PATH /backend
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONPATH="${INSTALL_PATH}:${PYTHONPATH}"

COPY . .

ENV TRANSFORMERS_CACHE=./.cache/huggingface/hub
ENV HF_HOME=./.cache/huggingface

EXPOSE 5000

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]


# First stage: Copy only the .cache folder
# FROM python:3.10.2 AS cache

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends build-essential ffmpeg libsm6 libxext6 cmake && \
#     apt-get clean

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# COPY ./.cache ./.cache

# # Second stage: Copy the rest of the files and build the final image
# FROM python:3.10.2

# ARG RAG_ENV

# ENV RAG_ENV=${RAG_ENV} \
#     INSTALL_PATH=/backend\
#     TRANSFORMERS_CACHE=./.cache/huggingface/hub\
#     PYTHONPATH="${INSTALL_PATH}:${PYTHONPATH}"\
#     HF_HOME=./.cache/huggingface

# RUN mkdir -p $INSTALL_PATH
# WORKDIR $INSTALL_PATH

# # Copy the .cache folder from the first stage
# COPY --from=cache .cache ./.cache

# COPY . .

# EXPOSE 5000

# RUN chmod +x entrypoint.sh

# ENTRYPOINT [ "./entrypoint.sh" ]
