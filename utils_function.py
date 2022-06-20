import turtle
from turtle import *
from queue import Queue, PriorityQueue
import operator
import argparse
import re
import sys
import numpy as np

def readInput(file):

    with open(file,mode = 'r') as f:
        # Line 1
        rs = re.findall('\d+',f.readline())
        if len(rs) == 2:
            w,h = [int(x) for x in rs]
        else:
            raise Exception('Line 1 must have 2 numbers')

        # Line 2
        rs = re.findall('\d+',f.readline())
        if len(rs) == 4:
            Sx,Sy, Gx,Gy = [int(x) for x in rs]
            posS = (Sx,Sy)
            posG = (Gx,Gy)
        else:
            raise Exception('Line 2 must have 4 numbers')

        # Line 3
        rs = re.findall('\d+',f.readline())
        if len(rs) == 1:
            n_obstacle = int(rs[0])
        else:
            raise Exception('Line 3 must have 1 number')

        # Line >=4
        obstacles = []
        line = f.readline()
        i=0
        while(i < n_obstacle and line != ''):
            rs = re.findall('\d+',line)
            if len(rs)%2==0:
                obstacles.append([int(x) for x in rs])
            else:
                raise Exception('Number at line {} must be even'.format(i+3))
            line = f.readline()
            i = i+1
        if len(obstacles) != n_obstacle:
            raise Exception('Number of obstacles is not equal to number of position lines')
        else:
            for i in range(n_obstacle):
                obstacles[i] = np.array(obstacles[i]).reshape(int(len(obstacles[i])/2),2)
            for i in range(0, n_obstacle):
                obstacles[i] = [tuple(x) for x in obstacles[i]]
    
    # Check valid start and target cell
    if not isvalid_neighbour(posS, w, h):
        raise Exception('Start point (x,y) must be in range 0 < x =< {} and 0 < y =< {}'.format(w, h))

    if not isvalid_neighbour(posG,w, h):
        raise Exception('Target point (x,y) must be in range 0 < x =< {} and 0 < y =< {}'.format(w, h))  
    
    return w,h, posS, posG, obstacles

def manhatan_distance(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) 

def square(size):
    for x in range(4):
        forward(size)
        left(90)

def drawGrid(startPos, width, height, size):
    tracer(0, 0)
    squareList = []
    penup()
    y = 0
    while y < height:
        for x in range(0, width, size):
            square(size)
            penup()
            goto(startPos[0] + x, startPos[1] + y)
            pendown()
            middlePos = (pos()[0] + size / 2, pos()[1] + size / 2)
            squareList.append(middlePos)
        y += size
    square(size)

def draw_num(orgin, n_col, size, axis):
    if axis == 'x':
        for i in range(1,n_col+1):
            penup()
            setpos(orgin[0] + i*size - size*0.6, orgin[1]-size)
            pendown()
            write(i,align="center",font=('Arial', 10, 'normal'))
    else:
        for i in range(1,n_col+1):
            penup()
            setpos(orgin[0] -size*0.6, orgin[1] + i*size - size)
            pendown()
            write(i,align="center",font=('Arial',10, 'normal'))

def filled_square(pos, size, name='', color='blue'):
    penup()
    fillcolor(color)
    begin_fill()
    goto(pos)
    pendown()
    square(size)
    end_fill()
    write(name, align= "left",font=('Arial',9))
    penup()

def convert_cor2pos(orgin, pose, size):
    return (orgin[0] + (pose[0]-1)*size, orgin[1] + (pose[1]-1)*size)

def getPoint_belong_line(point1, point2):
    # ax + by = c
    a = point2[1] - point1[1]
    b = point1[0] - point2[0]
    c = a*point1[0] + b*point1[1]
    x_range = abs(point1[0] - point2[0])
    y_range = abs(point1[1] - point2[1])
    edge_point = []
    if x_range >= y_range:
        if point1[0] <= point2[0]:
            x1 = point1[0]
            x2 = point2[0]
        else:
            x1 = point2[0]
            x2 = point1[0]
        for x in range(x1 + 1, x2):
            y = int((c - a*x)/b)
            edge_point.append((x,y))

    else:
        if point1[1] <= point2[1]:
            y1 = point1[1]
            y2 = point2[1]
        else:
            y1 = point2[1]
            y2 = point1[1]
        for y in range(y1 + 1, y2):
            x = int((c - b*y)/a)
            edge_point.append((x, y))
    return edge_point

def isvalid_neighbour(cell, xmax, ymax):
    return (cell[0] > 0) and (cell[0] <= xmax) and (cell[1] > 0) and (cell[1] <= ymax)

def neighbour_cells(pos, xmax, ymax):
    neighbours = [(pos[0]-1, pos[1]),(pos[0], pos[1]+1),(pos[0]+1, pos[1]), (pos[0], pos[1]-1)]
    return [e for e in neighbours if isvalid_neighbour(e,xmax,ymax)]

def genGraph(pos, xmax, ymax):
    return {pos: neighbour_cells(pos, xmax, ymax)}

def show_result(path, expend_cost, cor, algo='',d=None):

    if algo == 'IDS':
        string = 'với depth = {}'.format(d)
    else:
        string = ''
    
    if len(path) > 0:
        penup()
        setpos(cor)
        write("Tìm thấy đường đi từ S tới G",align="center",font=('Arial',14, 'normal'))
        setpos(cor[0], cor[1]-20)
        write("Cost = {}".format(len(path)-1),align="center",font=('Arial',14, 'normal'))
        setpos(cor[0], cor[1]-35)
        write("Total expanded node = {}".format(expend_cost),align="center",font=('Arial',15, 'normal'))
    else:
        penup()
        setpos(cor)
        write("Không tìm thấy đường đi từ S tới G " + string, align="center",font=('Arial',15, 'normal'))