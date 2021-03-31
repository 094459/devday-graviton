FROM amazonlinux:latest

## install required development packages
RUN yum -y groupinstall "Development tools" 
RUN yum -y install gcc-c++ libcurl-devel cmake3 git

## Compile c code

COPY src/benchmark.c /benchmark/
WORKDIR /benchmark/
RUN gcc "-DARCH=\"`uname -m`\"" -lm benchmark.c -o bench
CMD ["/benchmark/bench"]

