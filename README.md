_Accounting using command-line_ (accli) is a simple and extensible
framework and toolkit for business managing for small companies and/or
personal projects. It is written in Python and released under GPLv3.

[![Build Status](https://travis-ci.org/cletomartin/accli.svg?branch=master)](https://travis-ci.org/cletomartin/accli)

## Installation

On GNU/Linux:

```
$ apt-get install libpython3-dev virtualenv
$ virtualenv --python=/usr/bin/python3 accli
$ source accli/bin/activate
(accli) $ pip install -r requirements.txt
```

## accli-repo

accli requires that your accounting information is store in YAML
format. This is very useful since you can track the information using
a VCS like git. See
[accli-repo](https://github.com/cletomartin/accli-repo) for an
example.
