FROM amazonlinux:latest

## install required development packages
RUN yum -y groupinstall "Development tools" 
RUN yum -y install gcc-c++ libcurl-devel cmake3 git

## Compile c code

#WORKDIR /app/hello
COPY src/hello-graviton.c /hello-world/
WORKDIR /hello-world/
RUN gcc "-DARCH=\"`uname -m`\"" hello-graviton.c -o hello-graviton
#COPY hello-graviton /app/hello
#WORKDIR /app
CMD ["/hello-world/hello-graviton"]

