## DataTransformer
A simple tool for **Data Splitting** and **Data Encoding**.

## Usage
For Data Splitting:
```python
python DataSplit.py -infile [InputFile] -ofile [Outputfile] [Options]
```
For Data Encoding:
```python
python DataEncode.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]
```
Since no third-party package is used in this tool, so it supports [pypy](http://pypy.org/) for fast execution.
```python
pypy DataSplit.py -infile [InputFile] -ofile [Outputfile] [Options]
pypy DataEncode.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]
```
More parameter options can be found in `--help` or wiki page (not finished for now).
```python
python main.py --help
```

## Supported Task
* **data2sparse** -- convert **general** data into **sparse** data format
* **data2rel** -- convert **general** data into **relational** data format

## TODO Task
* **sparse2rel** -- convert **sparse** data into **relational** data format
* **data2vw** -- convert **general** data into [Vowpal Wabbit](https://github.com/JohnLangford/vowpal_wabbit) (VW) data format
* **sparse2vw** -- convert **sparse**  dataformat into VW format
* **vw2sparse** -- convert VW dataformat into **sparse**  format

## Supported Encoding Method
* `-cat` -- like one-hot encode, usually for categorical feature (supports for multi-labeled features)  
* `-num` -- directly use the value, usually for numerical data
* `-sim` -- automatically get similar features as meta features

## TODO Encoding Method
* `-wcat` -- encode multi-labeled features with different weights

