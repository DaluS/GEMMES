# Model: Spring_Network


    * **Creation** : 2024/06/04
    * **Coder**    : Paul Valcke
    * **Article**  : https://en.wikipedia.org/wiki/Spring_system
    * **Keywords** : ['Network', 'springs', 'mesh']
    

## What is this model ?

A Spring Network is an ensemble of nodes, that are linked by springs. 
Springs, depending of their compression, will apply forces on the nodes they connect. 
Those forces are then going to move the nodes, which change spring tensions. 

Typically, it is an excellent example of local wave propagation on a network structure.

The way it is coded here is the following: 
* Each nodes $_i \in N_{nodes}$ has a position $x_i,y_i$, and a speed $v^x_i,v^y_i$
* The dynamics is a classic $\dot{v}^x_i = (F^x_i - damp*v^y_i)/m_i$ where damp is fluid friction, and F the force resulting from the spring network

### How to represent the spring network 

Spring are here represented by tensors, and not as individuals. 
Preliminarily, we consider $N_{springs}$. They have four characteristics:
1. The index of their first node extremity $I^1_j$
2. The index of their second node extremity $I^2_j $
3. A stiffness $k_j$
4. An unstrenched length $L^0_j$

The strategy is to consider that each node is linked to each node, but with a stiffness 0 by default
In consequence, we define $k_{ij}$ the stiffness matrix of the network

In consequence, the dynamics is : 
$$\dot{v}_i = - \sum_j k_{ij} (dist(x_i,x_j)-L0_{ij}) cos(	heta_i) - \eta v_i$$

With $dist(x_i,x_j)= ((x_i - x_j )**2 + (y_i - y_j )**2)**{1/2}$ and $	heta_i = atan( (y_i-y_j) / (x_i-x_j))$

To create $k_{ij}$ and $L^0_{ij}$:


Instead of calculating this using loops, the calculations can be done using networks.

1. $k$ and $L^0$ are now matrices with 


## Why is it interesting ? 



## what is the purpose of your model,
## Expected behavior

DO NOT EDIT THIS FILE ! COPY AND PASTE IT THEN MODIFY THE COPY TO WRITE YOUR MODEL


## Presets

## Supplements
|                    | documentation                                                             | signature                               |
|:-------------------|:--------------------------------------------------------------------------|:----------------------------------------|
| Springlist_to_K_L0 | Give a weighted matrix representation of a network from a list approach.  | (Node1, Node2, k, L0, Nnodes, **kwargs) |
|                    |     Node1 and Node2 are the list of nodes at both extremity of the spring |                                         |
|                    |     k is the stiffness of the spring as a list                            |                                         |
|                    |     l0 is the length at which there is no force in the spring as a list   |                                         |
|                    |     Nnodes is the number of nodes in the Network.                         |                                         |
## Todo
* Nothing is done
* that should be done

## Equations
|          | eqtype       | definition                     | source_exp                                         | com   |
|:---------|:-------------|:-------------------------------|:---------------------------------------------------|:------|
| Nnodes   | size         | Number of nodes in the network |                                                    |       |
| vx       | differential | horizontal velocity            | dvx/dt=Fx/m - damp*vx/m,                           |       |
| vy       | differential | vertical velocity              | dvy/dt=Fy/m - damp*vy/m,                           |       |
| x        | differential | horizontal position            | dx/dt=vx,                                          |       |
| y        | differential | vertical position              | dy/dt=vy,                                          |       |
| dx       | statevar     |                                | dx=x - np.moveaxis(x, -1, -2)),                    |       |
| dy       | statevar     |                                | dy=y - np.moveaxis(y, -1, -2)),                    |       |
| distance | statevar     |                                | distance=(dx**2 + dy**2)**(1/2)),                  |       |
| angle    | statevar     |                                | angle=np.arctan2(dy, dx)),                         |       |
| Fmx      | statevar     |                                | Fmx=-Kmat*(distance-L0Mat)*np.cos(angle)),         |       |
| Fmy      | statevar     |                                | Fmy=-Kmat*(distance-L0Mat)*np.cos(angle)),         |       |
| Fx       | statevar     |                                | Fx=O.ssum2(-Kmat*(distance-L0Mat)*np.cos(angle))), |       |
| Fy       | statevar     |                                | Fy=O.ssum2(-Kmat*(distance-L0Mat)*np.sin(angle))), |       |
| Kinetic  | statevar     |                                | Kinetic=0.5*O.ssum(m*(vx**2 + vy**2))),            |       |
| L0Mat    |              |                                |                                                    |       |
| Kmat     |              |                                |                                                    |       |
| m        |              |                                |                                                    |       |
| damp     |              |                                |                                                    |       |