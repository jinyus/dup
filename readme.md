Install:

Clone this repo then install the dependencies:

```
pip install -r reqs.txt
```

```bash
>>> python dup.py --help

Usage: dup.py [OPTIONS] FOLDER

  Find duplicate files in a directory

Options:
  -d, --delete [new|old]  Delete newest/oldest
  -r, --dry-run           Do not delete files
  -y, --yes               skip delete confirmation
  --help                  Show this message and exit.
```
