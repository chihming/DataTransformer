Data2libFormat
======
A simple tool for converting csv data into [libSVM](http://www.csie.ntu.edu.tw/~cjlin/libsvm/)/[libFM](http://www.libfm.org/) format.

Usage
======
```python
python main.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]
```

To speed up data processing, it supports [pypy](http://pypy.org/) as well. 
```python
pypy main.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]
```

For more details, plase refer to `--help` function.
```python
python main.py --help
```

