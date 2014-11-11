## Data2libFormat
A simple tool for converting csv data into [libSVM](http://www.csie.ntu.edu.tw/~cjlin/libsvm/)/[libFM](http://www.libfm.org/) format.

## Usage
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

## Supported Task
* **csv2lib** -- convert csv data into libSVM-like data format

## TODO Task
* **csv2rel** -- convert csv data into relational data format
* **lib2rel** -- convert libSVM-like data into relational data format
* **csv2vw** -- convert csv data into [Vowpal Wabbit](https://github.com/JohnLangford/vowpal_wabbit) (VW) data format
* **lib2vw** -- convert libSVM-like dataformat into VW format
* **vw2lib** -- convert VW dataformat into libSVM-like format


## Simple CSV Data
For a csv data:
```csv
rating::user::item::age
9::userA::itemA::18
4::userA::itemB::16
5::userB::itemB::29
```
By using following instruction: 
```python
python main.py -task 'csv2lib' -infile [InputFile] -ofile [Outputfile] -target 0 -cat 1,2 -num 3 -sep '::' -head 1
```
It's able to get a converted data with libSVM-like format.
```csv
9 1:1 3:1 5:18
4 1:1 4:1 5:16
5 2:1 4:1 5:29
```

## CSV Data with Multiple Labels
Suppose there is a feature containing multiple labels, saying **Movie A** is belong to **Comedy** and **Romance**.
The dataset may looks like this:
```csv
rating::user::item::age::Genre
9::userA::itemA::18::Comedy|Drama
4::userA::itemB::16::Action|Comedy|Drama
5::userB::itemB::29::Documentary
```
By using `--msep` instruction:
```python
python main.py -task 'csv2lib' -infile [InputFile] -ofile [Outputfile] -target 0 -cat 1,2,4 -num 3 -sep '::' -msep '|' -head 1
```
It's able to get:
```
9 1:1 3:1 5:18 6:0.5 7:0.5
4 1:1 4:1 5:16 8:0.33 6:0.33 7:0.33
5 2:1 4:1 5:29 10:1
```

## Demo on [Movielens 1M/10M](http://grouplens.org/datasets/movielens/) dataset
Generate pure **User-Item** matrix in libSVM-like format:
```python
python main.py -task 'csv2lib' -infile ml-1m/ratings.dat -outfile [Outputfile] -sep '::' -target 2 -cat 0,1 -header 0
```
