## UAM

UAM stands for Universal AutoMarker. It is a framework for testing
student assignments written in a variety of programming languages,
collecting the results, and exporting them for easy viewing using
templates.

We currently provide full support for Python (pam) and Java (jam).

We are working on supporting SQL (sqam), Racket (ram), and Haskell
(ham).

We welcome collaboration and contributions!

## Requirements

You need Python >= 3.3 installed on your system. Then, install the
requirements listed in the file requirements.txt. The easiest way to
do this is to use pip (pip3 for Python 3):

`pip install -r /path_to_uam/requirements.txt`

You can use [virtualenv](https://virtualenv.pypa.io) to avoid
installing the packages system-wide.

To use JAM, you also need Java >= 7 installed in your system.

## Usage

The top level directory contains the framework scripts (test runner,
aggregator, and templator). The pam directory contains the Python
AutoMarker with instructions and examples, and the jam directory
contains the Java AutoMarker with instructions and examples.

See README files for pam and jam for specific instructions.


## Support

Please send comments, feedback and bugs to
[anya@cs.utoronto.ca](mailto:anya@cs.utoronto.ca). Currently, there is
very limited support provided. We hope to improve.
