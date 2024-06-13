# Drone simulation

### Authors:
- Sahar Tuvyahu
- Yehonatan Baruchson
- Guy Gur-Arieh
- Harel Gilad

### Abstract:
This project focuses on implementing a basic autonomous control system for a small drone with sensors and a controller. The primary objective is to enable the drone to autonomously navigate and cover as much area as possible. Our implementation uses a simulated environment that we have built ourselves using the OpenAI Gym platform to model the drone's behavior, including a basic obstacle avoidance mechanism and path planning algorithm.

## Implementation Roadmap
### Building the Environment and Drone Components
The first phase of our project involved constructing the simulation environment and implementing the fundamental components necessary for the drone's movement and sensing capabilities. Using the OpenAI Gym platform, we created a 2D map to represent the drone's operating area. 

also, we implemented the control mechanisms for yaw, roll, and pitch, allowing the drone to rotate and move in any direction. The drone is equipped with sensors, allwoing it to detect walls and obstacles in its path. we colored the area that the sensors move through in blue to track the drone's path and visualize its coverage.

### Attempting Navigation with Reinforcement Learning
In the second phase, we worked on implementing a navigation algorithm using Reinforcement Learning (RL). Our goal was to train the drone to autonomously navigate the environment, avoiding obstacles and covering as much area as possible. We set up a reward system to incentivize efficient exploration and safe navigation.

However, we encountered significant challenges with this approach. The vast number of pixels and possible paths created a highly complex state space, making it difficult for the RL algorithm to converge on an optimal policy within a reasonable timeframe. Despite extensive training, the performance improvements were marginal, and the drone's navigation remained suboptimal.

### Developing a Simple Navigation Algorithm
After evaluating the limitations of the RL approach, we decided to pivot towards a simpler, rule-based navigation algorithm. This final phase focused on leveraging the drone's sensor data to implement a straightforward yet effective obstacle avoidance and area coverage strategy.


## Usage:
Open a terminal, clone the repo:
```bash
git clone https://github.com/s4646/Drone_Simulation.git
```
navigate to the main.py file and run the program using python:
```bash
python main.py
```
