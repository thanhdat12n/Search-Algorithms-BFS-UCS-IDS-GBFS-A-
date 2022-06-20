import turtle
from turtle import *
from queue import Queue, PriorityQueue
import operator
import argparse
import re
import sys
from utils_function import *

def BFS(graph, start_node, target_node, obstacle_list, xmax, ymax):
    # Set of visited nodes to prevent loops
    visited = set()
    queue = Queue()
    expand_cell_each_step = []
    # Add the start_node to the queue and visited list
    queue.put(start_node)
    visited.add(start_node)
    
    # start_node has not parents
    parent = dict()
    parent[start_node] = None
    
    path_found = False
    while not queue.empty():
        current_node = queue.get()
        graph = genGraph(current_node, xmax, ymax)
        # If find target node
        if current_node == target_node:
            path_found = True
            break
        # Go to neighbours of current_node
        for neighbour in graph[current_node]:
            expand_cell = []
            if (not neighbour in obstacle_list) and (neighbour not in visited):
                queue.put(neighbour)
                parent[neighbour] = current_node
                visited.add(neighbour)
                if neighbour != target_node:
                    expand_cell.append(neighbour)
            else:
                pass
            if len(expand_cell) > 0:
                expand_cell_each_step.append(expand_cell)    
    # Path reconstruction
    path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node]) 
            target_node = parent[target_node]
        path.reverse()
    return path, expand_cell_each_step

def UCS(graph, start_node, target_node, obstacle_list, xmax, ymax):
    return BFS(graph, start_node, target_node, obstacle_list, xmax, ymax)

def IDDFS(graph, start_node, target_node, maxdepth, obstacle_list, xmax, ymax):
    depth = 0
    # Set of visited nodes to prevent loops
    visited = set()
    stack = []
    expand_cell_each_step = []
    # Add the start_node to the queue and visited list
    stack.append(start_node)
    visited.add(start_node)
    
    # start_node has not parents
    parent = dict()
    parent[start_node] = None

    # Perform step 3
    path_found = False
    n_adj=1
    i=0
    while stack:
        current_node = stack.pop()
        i += 1
        if i == n_adj:
            depth +=1
            i=0
        if depth > maxdepth:
            break
        graph = genGraph(current_node, xmax, ymax)
        n_adj = len(graph[current_node])
        
        # If find target node
        if current_node == target_node:
            path_found = True
            break
        # Go to neighbours of current_node
        
        for neighbour in graph[current_node]:
            expand_cell = []
            if (not neighbour in obstacle_list) and (neighbour not in visited):
                stack.append(neighbour)
                parent[neighbour] = current_node
                visited.add(neighbour)
                if neighbour != target_node:
                    expand_cell.append(neighbour)
            else:
                pass
            if len(expand_cell) > 0:
                expand_cell_each_step.append(expand_cell)    
    # Path reconstruction
    path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node]) 
            target_node = parent[target_node]
        path.reverse()
    return path, expand_cell_each_step

def GreedybestfirstSearch(graph, start_node, target_node, obstacle_list, xmax, ymax):
    # Set of visited nodes to prevent loops
    visited = set()
    queue = PriorityQueue()
    expand_cell_each_step = []
    # Add the start_node to the queue and visited list
    queue.put((0,start_node))
    visited.add(start_node)
    expand_cell_each_step = []
    
    # start_node has not parents
    parent = dict()
    parent[start_node] = None

    # Perform step 3
    path_found = False
    while not queue.empty():
        current_node = queue.get()[1]
        graph = genGraph(current_node, xmax, ymax)
        # If find target node
        if current_node == target_node:
            path_found = True
            break
        # Go to neighbours of current_node
        for neighbour in graph[current_node]:
            expand_cell = []
            if (not neighbour in obstacle_list) and (neighbour not in visited):
                # Manhatan distance from neighbour to target
                distance = manhatan_distance(neighbour, target_node)
                
                queue.put((distance,neighbour))
                parent[neighbour] = current_node
                visited.add(neighbour)
                if neighbour != target_node:
                    expand_cell.append(neighbour)
                
            else:
                pass
            if len(expand_cell) > 0:
                expand_cell_each_step.append(expand_cell)    
    # Path reconstruction
    path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node]) 
            target_node = parent[target_node]
        path.reverse()
    return path, expand_cell_each_step

def AstarSearch(graph, start_node, target_node, obstacle_list, xmax, ymax):
    # Set of visited nodes to prevent loops
    cost_from_start = {}
    cost_from_start[start_node] = 0
    visited = set()
    queue = PriorityQueue()
    expand_cell_each_step = []
    
    # Add the start_node to the queue and visited list
    queue.put((0,start_node))
    visited.add(start_node)
    
    # start_node has not parents
    parent = dict()
    parent[start_node] = None

    # Perform step 3
    path_found = False
    while not queue.empty():
        current_node = queue.get()[1]
        graph = genGraph(current_node, xmax, ymax)
        # If find target node
        if current_node == target_node:
            path_found = True
            break
        # Go to neighbours of current_node
        for neighbour in graph[current_node]:
            expand_cell = []
            if (not neighbour in obstacle_list) and (neighbour not in visited):
                cost_from_start[neighbour] = cost_from_start[current_node] + 1
                distance = manhatan_distance(neighbour, target_node) + cost_from_start[neighbour]
                queue.put((distance,neighbour))
                parent[neighbour] = current_node
                visited.add(neighbour)
                if neighbour != target_node:
                    expand_cell.append(neighbour)
            else:
                pass
            
            if len(expand_cell) > 0:
                expand_cell_each_step.append(expand_cell)
                
    # Path reconstruction
    path = []
    if path_found:
        path.append(target_node)
        while parent[target_node] is not None:
            path.append(parent[target_node]) 
            target_node = parent[target_node]
        path.reverse()
    return path, expand_cell_each_step