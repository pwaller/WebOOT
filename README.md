WebOOT
------

A web ROOT viewer.

Fed up with writing plot scripts?

## Introduction

WebOOT aims to make it easy to make navigate between ROOT files and do advanced
manipulation of many plots simultaneously.

The idea is that all plots should be addressable at a URL.

## Prerequisites

To make WebOOT work, you need
[PyROOT](http://root.cern.ch/drupal/content/pyroot),
[ImageMagick](http://www.imagemagick.org/),
[file magic](http://www.darwinsys.com/file/).

Try these commands in a shell to check everything is working:

    $ python -c "import ROOT"
    $ convert
    $ file

## Installation

This will fetch the WebOOT repository and any additional python dependencies:

    git clone git://github.com/rootpy/WebOOT
    cd WebOOT/
    python setup.py develop --user

## Usage

To start the WebOOT server, go to the `WebOOT/` directory and run:

    mkdir results/
    ${HOME}/.local/bin/pserve --reload development.ini

You will get a message on your screen that looks like this:

	Starting subprocess with file monitor
	Starting server in PID 31840.
	serving on http://0.0.0.0:6543

Plots placed the `results/` directory will be available at in the browser at
[http://localhost:6543/browse/](http://localhost:6543/browse/).


## Documentation

The project is still young so documentation is a work in progress.
Please bear with us. You're welcome to share issues and pull requests with us
through github!

Contact us at [weboot-users@cern.ch](mailto:weboot-users@cern.ch).

Please see `CONTRIBUTING`.
