FROM python:3.10.2-alpine
LABEL maintainer="Insights Engineering <basel.nestcicd@roche.com>"

# Build arguments
ARG SRC_DIR="/usr/src/presidio"
ARG USER="presidio"
ARG USER_ID=101
ARG USER_GROUP="presidio"
ARG USER_GROUP_ID=101
ARG USER_HOME="/home/${USER}"

# Create a non-root user and group, and create source dir
RUN addgroup -S -g ${USER_GROUP_ID} ${USER_GROUP} \
    && adduser -S -u ${USER_ID} -h ${USER_HOME} -G ${USER_GROUP} ${USER} \
    && mkdir -p ${SRC_DIR}

# Add source files
ADD . ${SRC_DIR}/

# Install presidio
WORKDIR ${SRC_DIR}
RUN python3 setup.py install

# Set the user and work directory
USER ${USER_ID}
WORKDIR ${USER_HOME}

# Remove source code
RUN rm -rf ${SRC_DIR}

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/presidio"]
