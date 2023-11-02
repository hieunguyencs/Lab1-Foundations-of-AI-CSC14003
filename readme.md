# Implement some search algorithms in AI

## Information
* **Course**: 
    - Foundations of Artificial Intelligence 
    (Cơ sở Trí tuệ Nhân tạo)
* **University**: 
    - Viet Nam National University, Ho Chi Minh City - HCMUS 
    (Đại học Quốc gia Tp.HCM - Đại học Khoa học Tự nhiên)
*  **Class**: 
    - 21 IT Honors 
    (21 Cử nhân Tài năng CNTT)
* **Author**: 
    - Tan
    - Hieu
    - Hoang

## How to run
### Run  all by bash
```
bash run.sh
```
**or**
### Run all by cmd
```
pip install requirements.txt
python main.py
```

### Run an specific algrorithm by cmd
* Usage: 
```
python [algorithm's file] [input's path]
```
Eg: 
```
python bfs.py ../input/level_1/input3.txt
```

## Symbols of the map
* Symbols of input (.txt)
    * **x**: wall
    * **'space'**: can-go point (can be moved)
    * **S**: start point
    * **+**: gift or station 
    * **o**: teleporter entry (in)
    * **O**:  teleporter exit (out)

* Symbols of output

![All symbols](Assets/Map-symbols.png)

## An example of input, output
* Input:
```
0
xxxxxxxxxxxxxxxxxxxxxx
    x   xx           x
x     x     xxx     xx
x x    xx  xxxx xxx xx
x x  xx x xx    xxx  x
x          xx   x  x x
xxxxxxx x       x  x x
x    xxxx  x x xxx   x
x          x x Sx x  x
xxxxx x  x x x     x x
xxxxxxxxxxxxxxxxxxxxxx
```
* Output

![output eg image](Assets/eg-input-output/level_1-output1-bfs.jpg)

## Demo
- Youtube video: https://youtu.be/sQ6hg4P4AWQ

## For more information: 
* Contact via: hieunt.wk@gmail.com