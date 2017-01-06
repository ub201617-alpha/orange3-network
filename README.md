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
```python
    def foo():
        print("bar")
```

Use cases
---------
