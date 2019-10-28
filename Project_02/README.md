# Pacman with weight

Try to find **optimal** path for pacman to eat **all the dots**. every cell has a **weight**.

## How to use it

1. [Download](http://py.processing.org/processing.py-windows64.zip) the Processing.py JAR file
2. Put the jar file in project main directory
3. Run command `java -jar processing-py.jar main.py`

## Examples

**Dark Blue** cells => **explored** cells  
**Light Blue** cells => **frontier** cells

### Breadth First Search

- Total Time: **2.06**  
- Total Nodes: **175**  
- Total Cost: **47**  
- 
['LEFT', 'LEFT', 'LEFT', 'DOWN', 'DOWN', 'DOWN', 'DOWN', 'RIGHT', 'UP', 'RIGHT']

![bfs-example](/example/breadth_fs.gif)

### Uniform Cost Search

- Total Time: **1.24**  
- Total Nodes: **109**  
- Total Cost: **36**  
- 
['LEFT', 'LEFT', 'LEFT', 'RIGHT', 'DOWN', 'RIGHT', 'DOWN', 'DOWN', 'DOWN', 'LEFT']

![ucs-example](/example/ucs.gif)

### A*

- Total Time: **0.18**  
- Total Nodes: **14**  
- Total Cost: **36**  
  
['LEFT', 'LEFT', 'LEFT', 'RIGHT', 'DOWN', 'RIGHT', 'DOWN', 'DOWN', 'DOWN', 'LEFT']

![astar-example](/example/a-star.gif)
