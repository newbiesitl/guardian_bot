
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app



#FROM continuumio/miniconda3
#
#RUN /bin/bash -c "conda create --name wow_bots python=3.7 && \
#    . activate wow_bots && \
#    pip install pandas && \
#    pip install ../mylocal_package/ && \
#    conda install numpy && \
#    conda install -c conda-forge pyautogui && \
#    conda install aiofiles && \
#    pip install keyboard && \
#    pip install fastapi && \
#    pip install pillow && \
#    pip install python-multipart"



RUN pip install numpy
RUN pip install pyautogui
RUN pip install aiofiles
RUN pip install keyboard
RUN pip install fastapi
RUN pip install pillow
RUN pip install python-multipart
