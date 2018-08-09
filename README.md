Simple static code analyzer - 'simpanalyzer'
============================================

Allows to check using verbs in names of function in python scripts.


Installation
------------

You can install 'simpanalyzer' with these commands:
```bash
    $ cd /<installation dir>
    $ git clone git://github.com/max-kim/static-code-analyzer.git
```

Requirements
------------

Python 3.6 (or over)
nltk 3.3

Setting environment:
```bash
    $ pip3 install -r requirements.txt
```

Usage
-----

The 'simpanalyzer' can be used directly:
```bash
    $ python3 /<installed path>/simpanalyzer.py /<some path or python script> --size 10
    (total 1 files in path <some path>)
    (<some path>:)
    (   total 2 words, 2 unique)
    (word: get, occurrence: 11)
    (word: save, occurrence: 1)
```

or similarly for several paths:
```bash
    $ python3 /<installed path>/simpanalyzer.py /<some path or python script> /<another path or python script> --size 10
```

Use the '--size' key to set the top size of result.

Also 'simpanalyzer' can be imported to your code and called there:

```python
from static_code_analyzer import simpanalyzer


if __name__ == '__main__':

    top_size = 15
    verbs = get_top_verbs_in_path(__file__, top_size)
        for word, occurrence in verbs:
            print('word: {}, occurrence: {}'.format(word, occurrence))
```

You can check the 'simpanalyzer' results and warnings in logs by path: /<simpanalyzer path>/logs.


Other
-----

This lib is a homewokr in OTUS Python web-dev.
Original link is [here](https://gist.github.com/Melevir/5754a1b553eb11839238e43734d0eb79).
