# Chn Text Norm

this is a repository for chinese text normalization (no longer maintained).

## Quick Start ##

### Git Clone Repo ###

git clone this repo to the root directory of your project which need to use it.

    cd /path/to/proj
    git clone https://github.com/Joee1995/chn-text-norm.git

after that, your doc tree should be:
```
proj                     # root of your project
|--- chn_text_norm       # this chn-text-norm tool
     |--- text.py
     |--- ...
|--- text_normalize.py   # your text normalization code
|--- ...
```

### How to Use ? ###

    # text_normalize.py
    from chn_text_norm.text import *
    
    raw_text = 'your raw text'
    text = Text(raw_text=raw_text).normalize()
