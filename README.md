Simple static code analyzer - 'simpanalyzer'
============================================

Allows to check using verbs in function names in python scripts.


Instalation
-----------

You can install 'simpanalyzer' with these commands::

    $ cd /<installation dir>
    $ git clone git://github.com/max-kim/static-code-analyzer.git


Requirements
------------

Set environment::

    $ pip install -r requirements.txt


Usage::
-------

The 'simpanalyzer' can be used directly::

    $ python /<installed path>/simpanalyzer.py /<some path or python script> --size 10
    (total 1 files in path <some path>)
    (<some path>:)
    (   total 2 words, 2 unique)
    (word: get, occurrence: 11)
    (word: save, occurrence: 1)

or similarly for several paths::

    $ python /<installed path>/simpanalyzer.py /<some path or python script> /<another path or python script> --size 10

Use the '--size' key to set the top result size.

Also 'simpanalyzer' can be imported to your code and be called there::

```python
from static_code_analyzer import simpanalyzer


if __name__ == '__main__':

    top_size = 15
    verbs = get_top_verbs_in_path(__file__, top_size)
        for word, occurrence in verbs:
            print('word: {}, occurrence: {}'.format(word, occurrence))
```

You can check the 'simpanalyzer' results and warnings in logs by path: '/<installed path>/logs'.
