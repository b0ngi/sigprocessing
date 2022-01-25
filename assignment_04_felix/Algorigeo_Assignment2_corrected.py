# -*- coding: utf-8 -*-
"""AlgoriGeo2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DCs6Ha75im-kioFw5DJfwc5QGiazOxxi
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
 

def graph_output(output_points, output_faces):
 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
 
    """
 
    Plot each face
 
    """
 
    for facenum in range(len(output_faces)):
        curr_face = output_faces[facenum]
        xcurr = []
        ycurr = []
        zcurr = []
        for pointnum in range(len(curr_face)):
            xcurr.append(output_points[curr_face[pointnum]][0])
            ycurr.append(output_points[curr_face[pointnum]][1])
            zcurr.append(output_points[curr_face[pointnum]][2])
        xcurr.append(output_points[curr_face[0]][0])
        ycurr.append(output_points[curr_face[0]][1])
        zcurr.append(output_points[curr_face[0]][2])
 
        ax.plot(xcurr,ycurr,zcurr,color='b')
 
    plt.show()
    
input_points = np.array([
  [-1.0,  1.0,  1.0],
  [-1.0, -1.0,  1.0],
  [ 1.0, -1.0,  1.0],
  [ 1.0,  1.0,  1.0],
  [ 1.0, -1.0, -1.0],
  [ 1.0,  1.0, -1.0],
  [-1.0, -1.0, -1.0],
  [-1.0,  1.0, -1.0]
])


input_faces = np.array([
  [0, 1, 2, 3],
  [3, 2, 4, 5],
  [5, 4, 6, 7],
  [7, 0, 3, 5],
  [7, 6, 1, 0],
  [6, 1, 2, 4],
])



def cube(input_faces, input_points):
  
  face_points = []
  
  for face in input_faces:
    face_points.append(np.mean(input_points[face,:],axis=0))
  
  edge_centers = {}

  for i in range(0,len(input_faces)):
    face = input_faces[i]
    for j in range(0,len(face)):
      edge_center = (input_points[face[j]] + 
                     input_points[face[(j+1)%len(face)]])/2
       
      
      if tuple(edge_center) in edge_centers:
        edge_centers[tuple(edge_center)][1]=i
      else:
        edge_centers[tuple(edge_center)] = [i,None,None, None]

     

      edge_centers[tuple(edge_center)][2] = tuple(input_points[face[j]])
      edge_centers[tuple(edge_center)][3] = tuple(input_points[face[(j+1)%len(face)]])
    
  
  edge_points ={}

  for edge_center in edge_centers:

    edge_point = (np.array(edge_center) + ((face_points[edge_centers[edge_center][0]] + face_points[edge_centers[edge_center][1]])/2))/2
    
    edge_points[tuple(edge_point)] = edge_centers[edge_center]


  vertices = {}
  
  for i in range(0,len(input_faces)):
    face = input_faces[i]
    for j in range(0,len(face)):
      point = input_points[face[j]]
      if tuple(point) in vertices:
        vertices[tuple(point)][0].append(i)
      else:
        vertices[tuple(point)] = [[i],[]]


  for point in vertices:
    for edge_point in edge_points:
      if(tuple(point) in edge_points[edge_point]):
        vertices[tuple(point)][1].append(edge_point)   
  
  

  new_input_points = []
  new_input_points_dict = {}
  new_input_faces = []


  for vertex in vertices:

    old_coords = np.array(vertex)

    avg_face_points=np.array([0,0,0])
    vertex_face_points = []

    for face in vertices[vertex][0]:
      avg_face_points =  avg_face_points + np.array(face_points[face])
      vertex_face_points.append(face_points[face])
    avg_face_points /= len(vertices[vertex][0])

    
    avg_mid_edges = np.array([0,0,0]) 
    vertex_edge_points = []
    i=0
    for edge_point in edge_points:
      if(vertex in edge_points[edge_point]):
        avg_mid_edges = avg_mid_edges + np.array(edge_point)
        i+=1
        vertex_edge_points.append(edge_point)
    avg_mid_edges /= i

    n = len(vertex_edge_points)
    m1 = (n-3)/n
    m2 = 1/n
    m3 = 2/n

    new_vertex = (m1*old_coords) + (m2*avg_face_points) + (m3*avg_mid_edges)

    new_input_points_dict[tuple(new_vertex)] = [list(vertex_face_points)]
    new_input_points_dict[tuple(new_vertex)].append(list(vertex_edge_points))
                           

  for i in range(0,len(new_input_points_dict)):
    vertex = list(new_input_points_dict.keys())[i]
    connected_face_points = new_input_points_dict[vertex][0]
    connected_edge_points = new_input_points_dict[vertex][1]


    connected_face_points = [list(x) for x in connected_face_points]
    connected_edge_points = [list(x) for x in connected_edge_points]

    new_input_points.append(list(vertex))
    new_input_points += connected_face_points
    new_input_points += connected_edge_points


    quadrangles = []
    
    for face_point in connected_face_points:
      quadrangle = [list(vertex)]
      for edge_point in connected_edge_points:
        face_points = [list(x) for x in face_points]
        if(face_points.index(face_point) in edge_points[tuple(edge_point)][:2]):
          quadrangle.append(list(edge_point))
      
      quadrangle.insert(2,face_point)


      quadrangles.append(quadrangle)


    for quadrangle in quadrangles:
      new_input_face = []
      for point in quadrangle:
        new_input_face.append(new_input_points.index(point))
      new_input_faces.append(new_input_face)



  return np.array(new_input_points), np.array(new_input_faces)

iterations = 3
for i in range(0,iterations):
  input_points, input_faces = cube(input_faces, input_points)


output_points, output_faces = input_points, input_faces
graph_output(output_points, output_faces)