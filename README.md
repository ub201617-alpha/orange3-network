Project D2
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

![example 1](http://shrani.si/f/1q/CO/1iS39NNK/screen-shot-2017-01-07-a.png "example 1")

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

The edge nodes contain town name labels, while the nodes interconecting them contain the index of the formed joint node. The width of the line connecting nodes represents their respective relative distance. Nodes further apart are connected by thicker lines and vice-versa.

![example 1](http://shrani.si/f/2H/9j/4IiRAHSr/screenshot-2017-01-07-15.png "example 1")

###Drugi primer


Team contributions
-----------
(Widget framework basics and prototype, widget input shaping, widget output shaping, readme formation, widget optimization, widget UI, testing)

1. Žan Anderle
  * ABC
2. Nejc Ilenič
  * Implemented skeleton for the OWNxNeigbourJoining widget (UI), implemented the set_input_distances method (setting input data)
3. Lovro Podgoršek
  * Writed README documentation
4. Jure Prevc
  * Tests and refactorization of the algorithm, provided correct output (Graph type), fixed auto commit
   and implemented progress bar in GUI
5. Jaka Šušteršič
  * Neighbour joining algorithm implementation (orange3-prototypes repository)