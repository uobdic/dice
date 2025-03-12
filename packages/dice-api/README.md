# DICE API

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/uobdic/dice-api/workflows/CI/badge.svg
[actions-link]:             https://github.com/uobdic/dice-api/actions
[pypi-link]:                https://pypi.org/project/dice-api/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/dice-api
[pypi-version]:             https://img.shields.io/pypi/v/dice-api

<!-- prettier-ignore-end -->

DICE API is a FastAPI-based API for the Data Intensive Computing Environment.
The aim is to provide a simple, easy-to-use API for admin-interaction

## Getting started

```bash
docker run \
    --net=host \
    -v /opt/cvmfs/cms.cern.ch/SITECONF/local:/cvmfs/cms.cern.ch/SITECONF/T2_UK_SGrid_Bristol:ro \
    -v /etc/hadoop:/etc/hadoop:ro \
    -v /etc/alternatives/hadoop-conf:/etc/alternatives/hadoop-conf:ro \
    -ti kreczko/dice-api:latest
```
