# Installation

Please install this software through docker:
1. install docker
2. pull image with `docker pull andynet/pheri`
3. run with `docker run -v /host/computer/data:/data andynet/hostdetector python3 main.py -i /data/phage.fasta -o /data`

[Dockerhub repository](https://hub.docker.com/r/andynet/pheri/)

# thesis

this project is destined to help biologist to classify bacteriophages according to theirs host organism 

## Dependencies
- snakemake
- biopython
- bash
- prokka
- blast
- EMBOSS needle
- scps
- mcl
- multiprocessing
- sklearn
- pandas
- graphviz
- pickle

## TODO
- refactor code
- use config for snakemake
- use docker for instalation
