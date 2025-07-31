# Assignment 1 - Student's Report

## Ben Murarotto 220292493

## Class of the Agent Program

My AI agent falls under the goal-based and model-based program class.
We define a strict list of rules to follow to reach the food (goal-based).
We maintain an internal model of the environment map to guide the search algorithm and navigate the agent (model-based).
We innately maximise utility by finding the shortest path to the food without a cost function.

## AI Techniques Considered

I considered A-star search initially to ensure my program considered all food options on the map. This ended up being an approach that solved an miniscule issue by over complicating the program. I was fixated on ensuring that the snake was targeting the most efficient food score-wise and to do that I initially incorporated a priority queue with a score cost function that took into account distance and points. However this bloated the number of calculations my program was doing and I felt as though it was not worth the potential minor improvements.

I switched to a breadth first search since all moves have the same cost BFS finds the closest food every time which is sufficient to solve snake.

## Reflections
I had several challenges when solving this issue, the first of which was over engineering which I mentioned in my technique considerations.

The second issue was creating stale states by not reassigning None values to the grids my snake had travelled to and then left - this lead to "invisible walls" on my map which I initially thought was my algorithm calculcating poorly.

The third issue was the edge cases where the first path generated required my snake to make an illegal move (initial value is up and the path to goal was down). I had to in corporate illegal move checking in my expand node AND my AI program to overcome this.