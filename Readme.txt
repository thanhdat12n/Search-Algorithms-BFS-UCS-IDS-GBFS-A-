Các thư viện cần cài đặt
turtle
pip install PythonTurtle

numpy
pip install numpy


Cách chạy code
python main.py --input /path/to/input.txt --algo BFS --maxdepth 5
hoặc 
python3 main.py --input /path/to/input.txt --algo BFS --maxdepth 5

Trong đó:
 + --input: đường dẫn tới file input, Ex: /path/to/input.txt, default = 'input.txt'
 + --algo : tên giải thuật, chọn 1 trong 5 loại sau [BFS, UCS, IDS, Greedy, Astar], default = 'BFS'
 + --maxdepth : độ sâu tối đa cho thuật toán IDS, default=5, các thuật toán khác sẽ bỏ qua tham số này nếu được truyền
