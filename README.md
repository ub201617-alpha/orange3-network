Neighbor-joining widget [project D2]
====================================
Our project focused on implementing an Orange widget, that will compute the results of the neighbor-joining algorithm given a distance matrix. The output network will be compatible with the existing widgets in the Orange-Network add-on. The goal of this widget is to calculate and help visualize the phylogenetic tree and showcase the original nodes and their inferred common ancestors.

Algorithm
----------
Neighbour joining is a bottom-up clustering method for the creation of phylogenetic trees. It is usually used for trees based on DNA or protein sequence data. The algorithm requires knowledge of the distance between each pair of taxa (e.g., species or sequences) to form the tree.
The input a distance matrix specifying the distances between each pair. The algorithm starts with a completely unresolved tree and iterates over the following steps until the tree is completely resolved:

1. Calculate the Q matrix based on the current distance metrix using the following formula:

    ![Q matrix formula](http://shrani.si/f/p/1w/4QMqxWU0/qmatrix.jpg "Q matrix formula")

    where d(i, j) is the distance between items **i** and **j**.

2. Find the pair of distinct items **i** and **j** (i != j) for which **Q(i, j)** has its lowest value. These items are joined to a newly created node.

3. Calculate the distance from both paired items to this new node using the following formula:

    ![distance formula](http://shrani.si/f/b/wZ/1nJ6SWch/img1.png "distance formula")

    Item **f** and **g** are the paired items and u is the newly created node. The branches joining **f** **u** and **g** **u** and their lengths, **δ (f, u)** and **δ (g, u)** are part of the tree which is gradually being created; they neither affect nor are affected by later neighbor-joining steps.

4. For each item not considered in the previous step, calculate the distance to the new node using the following formula formula:

    ![distance to the new node](http://shrani.si/f/2W/KW/1HavHKL/img2.png "distance to the new node")

    where **u** is the new node, **k** is the node which we want to calculate the distance to and **f** and **g**are the members of the pair just joined.

5. Start the algorithm again, replacing the pair of joined neighbors with the new node and using the distances calculated in the previous step.

Complexity
----------

Neighbor joining on a set of N items requires N-3 iterations. At each step one has to build and search a Q matrix. Initially the Q matrix is of size N × N and it gets smaller by 1 in each dimension after each iteration. Implementing this in a straightforward way leads to an algorithm with a time complexity of O(N^3).

UI workflow usage
-----------------

A typical input could be a Distance Matrix widget or a Distance file widget. The output is best visualized using the Network Explorer widget and enabling relative edge widths.

![example 1](http://shrani.si/f/0/115/2P0vSp1q/screen-shot-2017-01-08-a.png "example 1")

Script usage
--------------
Example of usage:
```python
from orangecontrib.network.neighbour_joining import NeighbourJoining
test_distances = [[0, 5, 9, 9, 8],
                  [5, 0, 10, 10, 9],
                  [9, 10, 0, 8, 7],
                  [9, 10, 8, 0, 3],
                  [8, 9, 7, 3, 0]]

nj = NeighbourJoining(test_distances)
nj.get_final_graph()
nodes = nj.get_all_nodes()
edges = nj.get_all_edges()
# edges:
# {(7, 4): 1.0,
# (7, 3): 2.0,
# (6, 5): 3.0,
# (5, 0): 2.0,
# (6, 2): 4.0,
# (5, 1): 3.0,
# (7, 6): 2.0}
```

Use cases
---------

###Slovenian towns

Our first sample use case includes the slovenian-towns.dst data set, which is included in the orange framework data set. To better show the individual results of neigbour joining we used a subset of only 10 major towns and used the UI work flow described in the previous chapters.

The edge nodes contain town name labels, while the nodes interconecting them contain the index of the formed joint node. The width of the line connecting nodes represents their respective relative distance. Nodes further apart are connected by thicker lines and vice-versa. The connected nodes and their drawn distances in the output closely resemble the sequence of towns along the A2 motorway on the sections Ljubljana-Kranj-Bled-Jesenice.

![example 1](http://shrani.si/f/2H/9j/4IiRAHSr/screenshot-2017-01-07-15.png "example 1")
###Iris

Our second example uses the iris dataset, which is also included in the Orange framework data set. To obtain a clearer visualization we performed some additional pruning steps of the input.

![example 2 gui](http://shrani.si/f/3t/AP/49Nvm6nJ/screenshot-2017-01-08-18.png "example 2 gui")

We first sampled the input file to limit the input size, calculated the pair distances,
used hierarchical clustering to choose only the most distant groups of individual species and their members so they were as close to each other as possible.

![example 2 hier](http://shrani.si/f/3T/i3/1KgDpXco/screenshot-2017-01-08-18.png "example 2 hier")

This calculated data set was then connected into the distances widget again and finally into our neigbor-joining widget.

![example 2](http://shrani.si/f/3q/oh/2FFEuFNT/unspecified123.png "example 2")

The result clearly shows the three distinct species (C1, C2, C3) and their separation with the much wider connecting lines.


Team contributions
-----------

1. Žan Anderle
  * Prepared the widget (and the algorithm output) to be compatible with other Orange widgets, implemented the initial graph output.
2. Nejc Ilenič
  * Implemented skeleton for the OWNxNeigbourJoining widget (UI), implemented the set_input_distances method (setting input data).
3. Lovro Podgoršek
  * Writen README documentation.
4. Jure Prevc
  * Tests and refactorization of the algorithm, provided correct output (Graph type), fixed auto commit, implemented progress bar in GUI and provided use case implementations.
5. Jaka Šušteršič
  * Neighbour joining algorithm initial implementation ([orange3-prototypes repository](https://github.com/ub201617-alpha/orange3-prototypes/commits/master)), documentation editing and translating.