FROM tensorflow/tensorflow:2.16.1-gpu-jupyter

# Update the package list, install wget, and clean up
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-opencv \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python packages from requirements.txt
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# There should be a better way to deal with this, like setting the Jupyter Lab folder
#RUN mkdir /.local && chown -R 1000:1000 /.local
#RUN mkdir /.cache && chown -R 1000:1000 /.cache

# Set working directory
WORKDIR /project

# Run jupyter-lab
CMD ["jupyter-lab", "--ip=0.0.0.0"]