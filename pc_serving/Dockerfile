FROM tensorflow/tensorflow:2.16.1-gpu

# Update the package list, install wget, and clean up
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-opencv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python packages from requirements.txt
COPY pc_serving/requirements.txt /tmp/requirements.txt
RUN pip install --requirement /tmp/requirements.txt

# TODO find a better way to copy the labels
WORKDIR /data
COPY ./data/labeled /data/labeled

# Set working directory
WORKDIR /project

COPY ./pc_training/preprocess_lego_image.py /project
COPY ./pc_training/predict_brick.py /project
COPY ./pc_serving/predict_server.py /project
COPY ./pc_training/model.keras /project

# Folder for storing new pictures. Best to mount this as a volume and keep them for future learning
RUN mkdir /new_pictures

# Expose the port
EXPOSE 8000

# Run jupyter-lab
CMD ["fastapi", "run", "predict_server.py"]