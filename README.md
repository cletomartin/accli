_Accounting using command-line_ (accli) is a simple and extensible
framework and toolkit for business managing for small companies and/or
personal projects. It is written in Python and released under GPLv3.

[![build status](https://gitlab.com/cleto/accli/badges/master/build.svg)](https://gitlab.com/cleto/accli/commits/master)

## Installation

On GNU/Linux:

```
$ apt-get install libpython3-dev virtualenv
$ virtualenv --python=/usr/bin/python3 accli
$ source accli/bin/activate
(accli) $ make develop
```

## accli-repo

accli requires that your accounting information is store in YAML
format. This is very useful since you can track the information using
a VCS like git. See [accli-repo](https://gitlab.com/cleto/accli-repo)
for an example.
