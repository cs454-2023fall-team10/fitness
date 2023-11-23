# 0. Prerequisite
You should install numpy
```
$ pip install numpy
```
Also, you should install model you want to use
```
$ pip install sentence_transformers
$ pip insall openai
```
**(Optional)** If you want to test just this file, you should install networkx
```
$ pip install networkx
```

# 1. How to use
1) If you want to **use default settings** of our fitness function, just import `fitness.py` and call `fitness`
```python
import fitness

  val = fitness.fitness(graph)
```
   
2) If you want to **change some settings** in our fitness function, edit `functions.py`.
