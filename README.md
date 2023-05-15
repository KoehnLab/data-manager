# data-manager

Python toolkit for managing data from quantum-chemical calculations.

We make use of [SQLAlchemy](https://www.sqlalchemy.org/) to handle the abstraction over the native SQL access statements (via an
object-relational-mapping (ORM)). Therefore, you'll have to install this package on your system before being able to use `data-manager`:
```shell
pip3 install SQLAlchemy
```
(see https://docs.sqlalchemy.org/en/20/intro.html#installation for alternative installation methods).


## Installation

After having cloned this repository, you'll have to make sure that the `packages` directory is within your `PYTHONPATH`. To ensure that, add the
following to your `~/.bashrc`:
```bash
export PYTHONPATH="$PYTHONPATH:/path/to/this/repo/packages"
```
