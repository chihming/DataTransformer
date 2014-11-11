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
* **csv2lib** -- convert **csv** data into **libSVM-like** data format
* **csv2rel** -- convert **csv** data into **relational** data format

## TODO Task
* **lib2rel** -- convert libSVM-like data into relational data format
* **csv2vw** -- convert csv data into [Vowpal Wabbit](https://github.com/JohnLangford/vowpal_wabbit) (VW) data format
* **lib2vw** -- convert libSVM-like dataformat into VW format
* **vw2lib** -- convert VW dataformat into libSVM-like format


## CSV Data -> libSVM-like Data
Given an [InputFile] csv data:
```csv
rating::user::item::age
9::userA::itemA::18
4::userA::itemB::18
5::userB::itemB::29
```
By using following instruction: 
```python
python main.py -task 'csv2lib' -infile [InputFile] -ofile [Outputfile] -target 0 -cat 1,2 -num 3 -sep '::' -head 1
```
It's able to get a [Outputfile] converted data with libSVM-like format.
```csv
9 1:1 3:1 5:18
4 1:1 4:1 5:18
5 2:1 4:1 5:29
```

## CSV Data with Multiple Labels -> libSVM-like Data
Given an [InputFile] csv data with multi-labeled *Genre* feature:
```csv
rating::user::item::age::Genre
9::userA::itemA::18::Comedy|Drama
4::userA::itemB::18::Action|Comedy|Drama
5::userB::itemB::29::Documentary
```
By using `--msep` instruction:
```python
python main.py -task 'csv2lib' -infile [InputFile] -ofile [Outputfile] -target 0 -cat 1,2,4 -num 3 -sep '::' -msep '|' -head 1
```
It's able to get [Outputfile] in libSVM-like format:
```
9 1:1 3:1 5:18 6:0.5 7:0.5
4 1:1 4:1 5:18 8:0.33 6:0.33 7:0.33
5 2:1 4:1 5:29 10:1
```

## CSV Data -> Relational Data
Given [TrainFile]:
```csv
rating::user::item
9::userA::itemA
4::userA::itemB
5::userB::itemB
```
, [TestFile]:
```csv
rating::user::item
8::userB::itemA
4::userC::itemB
```
and the [RelationalFile] user profile:
```csv
user::gender::age
userA::M::18
userB::F::16
userC::M::29
```
By using following instructions:
```python
python main.py -task 'csv2rel' -infile [TrainFile],[TestFile] -target 0 -ofile [Outputfile] -rel [RelationalFile] -rtarget 0 -cat 1,2,4 -num 3 -sep '::' -msep '|' -head 1
```
We get one [Outputfile].train file:
```csv
0
0
1
```
One [Outputfile].test file:
```csv
1
2
```
One [Outputfile] encoded file:
```csv
0:1 3:1 5:18
1:1 4:1 5:16
2:1 3:1 5:29
```

## Demo on [Movielens 1M/10M](http://grouplens.org/datasets/movielens/) dataset
Generate pure **User-Item** matrix in libSVM-like format:
```python
python main.py -task 'csv2lib' -infile ml-1m/ratings.dat -outfile [Outputfile] -sep '::' -target 2 -cat 0,1 -header 0
```

Generate **User-Item-Time** matrix in libSVM-like format:
```python
python main.py -task 'csv2lib' -infile ml-1m/ratings.dat -outfile [Outputfile] -sep '::' -target 2 -cat 0,1 -num 2 -header 0
```
