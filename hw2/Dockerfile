FROM qmcgaw/latexdevcontainer:latest

RUN mkdir -p /opt
ADD fib.py /opt/fib.py
ADD to_tex.py /opt/to_tex.py
ADD requirements.txt /opt/requirements.txt


# # Create a python3 symlink pointing to latest python version
# RUN ln -sf /usr/bin/python3.9 /usr/bin/python3

# Install matching pip version

RUN apt-get update -y

RUN apt-get install -y python3 python3-distutils curl

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.9 get-pip.py \
    && rm get-pip.py

RUN tlmgr install pgf fontspec

WORKDIR /opt

RUN  python3 -m pip install -r requirements.txt \
    && python3 -m pip install -i https://test.pypi.org/simple/ image-gen-deeppython

RUN python3 to_tex.py

RUN pdflatex test_array.tex

RUN pdflatex test_image.tex



