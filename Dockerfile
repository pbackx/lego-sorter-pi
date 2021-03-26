FROM python:3.9-buster

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install jupyter

WORKDIR /notebooks
ENTRYPOINT ["jupyter", "notebook", "--ip=*", "--allow-root", "--no-browser"]
