## DataTransform
A simple tool for data splitting and data transforming. e.g. Converting csv data into [libSVM](http://www.csie.ntu.edu.tw/~cjlin/libsvm/)/[libFM](http://www.libfm.org/) format.

## Usage
```python
python main.py -task [Task] -infile [InputFile] -ofile [Outputfile] [Options]
```

It supports [pypy](http://pypy.org/) as well. (a faster way for executoin)
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
* **dsplit** -- split data into train/test according to specified parameters

## TODO Task
* **lib2rel** -- convert libSVM-like data into relational data format
* **csv2vw** -- convert csv data into [Vowpal Wabbit](https://github.com/JohnLangford/vowpal_wabbit) (VW) data format
* **lib2vw** -- convert libSVM-like dataformat into VW format
* **vw2lib** -- convert VW dataformat into libSVM-like format

## Supported Encoding Method
* `-cat` -- like one-hot encode, usually for categorical feature (supports for multi-labeled features)  
* `-num` -- directly use the value, usually for numerical data

## TODO Encoding Method
* `-wcat` -- encode multi-labeled features with different weights
* `-sim` -- automatically get similar features as meta features

## CSV Data -> CSV training data + CSV testing data
Given an **[InputFile]** csv data:
```csv
rating::user::movie::time
9::userA::movieA::5
4::userA::movieB::10
5::userB::movieB::3
4::userB::movieC::8
4::userC::movieA::8
8::userC::movieC::11
3::userD::movieA::2
7::userD::movieC::11
```

By using the instructions:
* `-task 'dsplit'`: do data splitting
* `-infile [InputFile]`: input file name
* `-outfile [OutputFile]`: output file name
* `-target 0`: split data according to column 1
* `-sep '::'`: split data by '::'
* `-ratio 0.8:0.2:0.5`: split targets to 80%/20% as training/testing, 50% of testing data for training
* `-header 1`: skip header

```python
python main.py -task 'dsplit' -infile [InputFile] -outfile [OutputFile] -target 0 -sep '::' -ratio 0.8:0.2:0.5 -header 1
```

It's able to get **[OutputFile].train** and **[OutputFile].test**. For instance:

**[OutputFile].train**
```csv
9::userA::movieA::5
4::userA::movieB::10
5::userB::movieB::3
4::userC::movieA::8
8::userC::movieC::11
3::userD::movieA::2
```
**[OutputFile].test**
```csv
4::userB::movieC::8
7::userD::movieC::11
```

## CSV training/testing data -> libSVM-like data
Given **[InputFiles]** e.g. [InputFile].train,[InputFile].test

By using the instructions:
* `-task 'csv2lib'`: convert data to libSVM-like format
* `-infile [InputFile].train,[InputFile].test`: input file names, splitted by ','
* `-outfile [OutputFile].train,[OutputFile].test`: output file names, splitted by ','
* `-target 0`: get column 0 as prediction target
* `-cat 1,2`: categorical encoding on columns 1,2
* `-num 3`: numerical encoding on column 3
* `-sep '::'`: split data by '::'
* `-header 0`: no header

```python
python main.py -task 'csv2lib' -infile [InputFile].train,[InputFile].test -outfile [OutputFile].train,[OutputFile].test -target 0 -cat 1,2 -num 3 -sep '::' -header 0
```

It's able to get the **[Outputfile].train**
```csv
9 1:1 5:1 8:5
4 1:1 6:1 8:10
5 2:1 6:1 8:3
4 3:1 5:1 8:8
8 3:1 7:1 8:11
3 4:1 5:1 8:2
```
and the **[Outputfile].test**
```csv
4 2:1 7:1 8:8
7 4:1 7:1 8:11
```

## For Multi-labeled Features
Given an **[InputFile]** csv data with multi-labeled *Genre* feature:
```csv
rating::user::item::age::Genre
9::userA::itemA::18::Comedy|Drama
4::userA::itemB::18::Action|Comedy|Drama
5::userB::itemB::29::Action|Comedy|Drama
```
By using the `--msep` instruction:
```python
python main.py -task 'csv2lib' -infile [InputFile] -ofile [Outputfile] -target 0 -cat 1,2,4 -num 3 -sep '::' -msep '|' -head 1
```
It's able to get **[Outputfile]** in libSVM-like format:
```
9 1:1 3:1 5:18 6:0.5 7:0.5
4 1:1 4:1 5:18 8:0.33 6:0.33 7:0.33
5 2:1 4:1 5:29 8:0.33 6:0.33 7:0.33
```

## CSV training/testing data -> libFM relational data
Relational data format of libFM can be found in
* *Steffen Rendle (2013): Scaling Factorization Machines to Relational Data, in Proceedings of the 39th international conference on Very Large Data Bases (VLDB 2013)*

Given the **[RelationalFile]** movie profile:
```csv
movie::Genre
movieA::Comedy|Drama
movieB::Action|Comedy|Drama
movieC::Documentary
movieD::Comedy
```

By using following instructions:
* `-task 'csv2rel'`: convert data to libFM relational format
* `-infile [InputFile].train,[InputFile].test`: train/test file names, splitted by ','
* `-target 0`: get column 0 as mapping data
* `-relfile [RelationalFile]`: relational data file name (must be unique data)
* `-rtarget 0`: get column 0 as mapping target
* `-outfile [OutputFile]`: output file name (automatically get [OutputFile]/[OutputFile].train/[OutputFile].test/)
* `-cat 1,2`: categorical encoding on columns 1,2 of relational data
* `-sep '::'`: split train/test data by '::'
* `-rsep '::'`: split relational data by '::'
* `-msep '|'`: split multi-labeled features by '|'
* `-header 1`: skip header

```python
python main.py -task 'csv2rel' -infile [InputFile].train,[InputFile].test -sep '::' -target 0 -relfile [RelationalFile] -rsep '::' -rtarget 0 -ofile [Outputfile] -cat 1,2 -msep '|' -head 1
```
We get one **[Outputfile]** encoded file:
```csv
0 0:1 4:0.5 5:0.5
0 1:1 6:0.33 4:0.33 5:0.33
0 2:1 7:1
0 3:1 4:1
```
One **[Outputfile].train** file:
```csv
0
1
1
0
2
0
```
One **[Outputfile].test** file:
```csv
2
2
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
