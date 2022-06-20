
import os
try:
    import turtle
    import numpy as np
except:
    os.system("pip install numpy")
    os.system("pip install PythonTurtle")

import turtle
from turtle import *
from queue import Queue, PriorityQueue
import operator
import argparse
import re
import sys

from algorithms import *
from utils_function import *

def GeneralSearch(graph, start_node, target_node, obstacle_list, xmax, ymax, algo, maxdepth):
    if algo == 'BFS':
        final_path, expand_cell_each_step = BFS(graph, start_node, target_node, obstacle_list, xmax, ymax)
    elif algo == 'UCS':
        final_path, expand_cell_each_step = UCS(graph, start_node, target_node, obstacle_list, xmax, ymax)
    elif algo == 'IDS':
        final_path, expand_cell_each_step = IDDFS(graph, start_node, target_node, maxdepth, obstacle_list, xmax, ymax)
    elif algo == 'Greedy':
        final_path, expand_cell_each_step = GreedybestfirstSearch(graph, start_node, target_node, obstacle_list, xmax, ymax)
    elif algo == 'Astar':
        final_path, expand_cell_each_step = AstarSearch(graph, start_node, target_node, obstacle_list, xmax, ymax)
    else:
        raise Exception("Không tìm thấy giải thuật")

    return final_path, expand_cell_each_step

def init_visualize():
    title('Lab 1 - Nguyen Thanh Dat')
    hideturtle()
    speed(0)
    Screen()
    setup(width=0.45, height=0.7)
    # screensize(500, 500)
    penup()

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str,default='input.txt',
        help="Path of input file (*.txt) ", action="store")
    
    parser.add_argument("--algo", type=str, default='BFS',
        help="Name of algorithm searchs [BFS, UCS, IDS, Greedy, Astar]", action="store")   
    
    parser.add_argument("--maxdepth", type=int, default=5,
        help="Max depth for IDS algorithm, will skip for if algo is different IDS", action="store") 
    return parser.parse_args(argv)

def main(argvs):
    # Parse input
    file = argvs.input
    ALGO = argvs.algo
    MAXDEPTH =  argvs.maxdepth

    n_col, n_row, start, target, obstacles = readInput(file) 
    size = 20 # length of edge of square
    init_visualize()

    goto(-n_col*size/2 , -n_row*size/2)
    pensize(1)
    orgin = pos()
    tracer(0,0)
    drawGrid(orgin, n_col*size, n_row*size, size)
    penup()
    goto(orgin)
    pencolor('black')

    # Draw number of axis
    draw_num(orgin, n_col, size, 'x')
    draw_num(orgin, n_row, size, 'y')
    
    # Fill color start and target cell
    filled_square(convert_cor2pos(orgin, start,size) , size, color='blue', name = 'S')
    filled_square(convert_cor2pos(orgin, target,size), size, color='red', name = 'G')
    
    # Fill color polygon
    all_wall_point = []
    for obstacle in obstacles:
        # Fill color for vertex
        for vertex in obstacle:
            filled_square(convert_cor2pos(orgin, vertex,size) , size, color = 'yellow')

        # Fill color for edge
        all_wall_point = all_wall_point + obstacle
        obstacle.append(obstacle[0]) # noi diem dau va diem cuoi cua da giac
        for idx in range(0, len(obstacle)-1):
            poly_edge = getPoint_belong_line(obstacle[idx], obstacle[idx+1])
            all_wall_point = all_wall_point + poly_edge
            for point in poly_edge:
                filled_square(convert_cor2pos(orgin, point,size) , size, color = 'gray')
    
    # Search
    init_graph = genGraph(start,n_col,n_row)
    final_path, expand_cell_each_step = GeneralSearch(init_graph, start, target, all_wall_point,n_col,n_row, ALGO, MAXDEPTH)
    expend_cost = len(expand_cell_each_step)
    path_cost = len(final_path)
    for step in expand_cell_each_step:
        for point in step:
            filled_square(convert_cor2pos(orgin, point,size) , size, color = 'green')

    # tracer(0,0)
    for point in final_path[1:-1]:
        filled_square(convert_cor2pos(orgin, point,size) , size, color = 'orange')

    info_cor = tuple(map(operator.add, orgin, (n_col*size/2, n_row*size+50)))
    # name of algorithm
    setpos(info_cor[0], info_cor[1]+20)
    write("Giải thuật: "+ ALGO, align="center",font=('Arial',15, 'normal'))
    show_result(final_path,expend_cost, info_cor,ALGO, d = MAXDEPTH)
    print("===> Total expanded node =", expend_cost)
    if path_cost > 0:
        print("===> Path cost =", path_cost-1)
    else:
        print("===> Không tìm thấy đường đi từ S tới G")

    done()

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))