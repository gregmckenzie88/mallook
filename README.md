# Malware Detection 👀 Back End

This repository captures the back end API for receiving a portable executable file from the [front end application](https://github.com/gregmckenzie88/Malware-Detection-Front-End), generating a classification, and returning that payload to the front end.

Data analysis and modelling can be found in [this repository](https://github.com/gregmckenzie88/Springboard-Capstone-3-Email-Threat-Detection-System).

This project is forked from (https://github.com/fieldsfieldsfields/mallook)

## Installation

Make sure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

In the project directory, run the following command:

```bash
docker build -t malware-detection . && docker run -p 4000:5000 malware-detection:latest
```

Install and run the [front end application](https://github.com/gregmckenzie88/Malware-Detection-Front-End) to submit files for classification.
