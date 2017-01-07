Neighbour joining widget for Orange3
====================================
Neighbour joining is a bottom-up (agglomerative) clustering method for the creation of phylogenetic trees.
Usually used for trees based on DNA or protein sequence data, the algorithm requires knowledge of the distance between
each pair of taxa (e.g., species or sequences) to form the tree.

We implemented Neighbour joining algorithm as a widget inside Orange3 Network add-on.

Implemented widget requires distance matrix (DistMatrix) as an input. Output of the widget is a Graph which is fully
compatible with the existing widgets found in Orange-Network add-on.



Implementation
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
for joined, new_distances in nj():
    pass
```

Neighbour joining algorithm takes as input a distance matrix specifying the distances between each pair.
(test_distances in example). The algorithm starts with a completely unresolved tree and iterates over the following
steps until the tree is completely resolved:

1. Based on the current distance matrix calculates the matrix Q by the formula:

    ![Q matrix formula](http://shrani.si/f/p/1w/4QMqxWU0/qmatrix.jpg "Q matrix formula")

    where d(i, j) is the distance between items i and j.

2. Finds the pair of distinct items i and j (i != j) for which Q(i, j) has its lowest value. These items are joined
to a newly created node.

3. Calculates the distance from each of the item in the pair to this new node by the formula:

    ![distance formula](http://shrani.si/f/b/wZ/1nJ6SWch/img1.png "distance formula")

    Item f and g are the paired items and u is the newly created node. The branches joining f and u and g and u ,
    and their lengths, δ (f, u) and δ (g, u) are part of the tree which is gradually being created; they neither
    affect nor are affected by later neighbor-joining steps.

4. For each item not considered in the previous step, we calculate the distance to the new node by the formula:

    ![distance to the new node](http://shrani.si/f/2W/KW/1HavHKL/img2.png "distance to the new node")

    where u is the new node, k is the node which we want to calculate the distance to and f and g are the members of the pair just joined.

5. Start the algorithm again, replacing the pair of joined neighbors with the new node and using the distances calculated in the previous step.

Complexity
----------

Neighbor joining on a set of n items requires n-3 iterations. At each step one has to build and search a Q matrix.
Initially the Q matrix is size n × n, then the next step it is (n − 1) × (n − 1), etc. Implementing this in a straightforward way
leads to an algorithm with a time complexity of O( n^3 ); implementations exist which use heuristics to do much better than this on average.

Use cases
---------

Example 1:

    ![example_1](http://shrani.si/f/2H/9j/4IiRAHSr/screenshot-2017-01-07-15.png "example_1")


