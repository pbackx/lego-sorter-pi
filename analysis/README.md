# Nvidia driver install on Windows

Before downloading or installing anything, first check out the 
[TensorRRT support matrix](https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html).
It will indicate the versions of the different components you should download and
install.

At the time of this writing this combination should work:
* [CUDA toolkit 11.2 update 1](https://developer.nvidia.com/cuda-11.2.1-download-archive)
* [cuDNN 8.1.1](https://developer.nvidia.com/rdp/cudnn-archive)
* [TensorRT 7.2.3](https://developer.nvidia.com/nvidia-tensorrt-7x-download)

## CUDA toolkit installation

This is an installer. Nothing special to report. I did read on some tutorials that you need to have some version
of Visual Studio installed. I already had Visual Studio 2019 on my computer, so I did not run into this issue.

## cuDNN installation

[Installation Guide](https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn-811/install-guide/index.html#install-windows)

[Archived Documentation](https://docs.nvidia.com/deeplearning/cudnn/archives/index.html)

By default, the CUDA Toolkit is installed in `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2`. You will
need to copy a number of files from the downloaded cudnn zip file into this folder.

If the toolkit was correctly installed, the CUDA installation path should be set in the environment:

    > echo $Env:CUDA_PATH
    C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.2

Now extract the cuDNN zip file and `cd` into that folder (in an admin powershell):

    cp -v .\cuda\bin\cudnn*.dll $Env:CUDA_PATH\bin
    cp -v .\cuda\include\cudnn*.h $Env:CUDA_PATH\include
    cp -v .\cuda\lib\x64\cudnn*.lib $Env:CUDA_PATH\lib\x64


## TensorRT installation

[Installation Guide](https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html#installing-zip)

[Documentation](https://docs.nvidia.com/deeplearning/tensorrt/index.html)

To keep all NVidia files together, we'll copy TensorRT into the CUDA toolkit folder.

    cp -v .\TensorRT-7.2.3.4\lib\*.dll $Env:CUDA_PATH\bin

Do not remove the extracted files just yet, we'll need them in the next step.


# Configure virtualenv

Getting started:

    python3 -m venv ./venv
    .\venv\Scripts\activate
    pip install -r requirements.txt

Now in the folder that you extracted TensorRT to, install the following wheels:

    pip install .\TensorRT-7.2.3.4\graphsurgeon\graphsurgeon-0.4.5-py2.py3-none-any.whl
    pip install .\TensorRT-7.2.3.4\uff\uff-0.6.9-py2.py3-none-any.whl
    pip install .\TensorRT-7.2.3.4\onnx_graphsurgeon\onnx_graphsurgeon-0.2.6-py2.py3-none-any.whl


# Start the notebook

Start:

    .\venv\Scripts\activate
    cd ..
    jupyter lab

Note: if Jupyter does not want to start, you may need [to upgrade pip](https://github.com/jupyterlab/jupyterlab/issues/10166)