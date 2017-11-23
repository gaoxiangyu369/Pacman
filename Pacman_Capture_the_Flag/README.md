![](https://s3-us-west-2.amazonaws.com/cs188websitecontent/projects/release/contest/v1/002/capture_the_flag.png)

# Aim

The purpose of this project is to implement a Pac Man Autonomous Agent that can play and compete in a tournament.

# Task

### Axiomatisation of Pac Man in PDDL

* PDDL model successfully generates good plans suitable to be used for Pacman

* PDDL model is sound (correctly models a deterministic Pacman game) and complete (models all required behaviour: ghost and pacman)

* PDDL model uses the appropriate levels of abstraction

    - Encode the Grid

    - Point of View of Ghost (static Pacman, goal eat pacmans)

    - Point of View of Pacman (static Ghosts, goal eat food and come back to home area)

    - Power Level (just check whether is SuperPacman or not)
        
    - Make sure that the PDDL files can be solved using the [online solver](http://editor.planning.domains/).

### Implementation of Pac Man

Produce a working agent that can play Pacman within the Pacman game engine, based on [Berkeley Pac Man](http://ai.berkeley.edu/contest.html).

Only myTeam.py got edited.

#### To run the planner:

-------

The planner is implimented in python 2.7 and is located in the file 'myTeam.py'.

To run this planner, use the team color to choose side then the file name as follows:

```
-r myTeam
-b myTeam
```

#### Code documentation:

-------


The planner creates two Pacman agents. 

First select the closet food x-coordinate one moves to 1/4 the other to the 3/4. 

The planner uses two tactics - DEFFENCE and OFFENCE. Which tactic is implimented is dependent on the state of the game.

All legal actions are considered to choose the best next move to make. For each legal, a set of tactic dependent heuristics are used to calculate an overall score for that action. The heuristics consists of a number of features that are relevant to the tactic and their associated weightings of importance. All features are given the equal weights but with different feature values. All feature/weighting products for a tactic are summed together and the result is that action's desirability score. The best action is chosen with the highest score is chosen as the best move to make.

Due to the range of sight, the enemy location can be speculated through iteratively filtering noisy distance data to infer the mostly likely position of the enemy.

#### Planning approach:

-------

The strategies that each Pacman agent can impliment are as follows:

At the start of the game, each agent moves to the centre along the shortest path possible. Taking the shortest path improves the chance that our agents can reach the expected point first to guard our foods. The centre is determined by the closest food to enemy territory and the available positions which are the closest to the enemy territory.
 
**OFFENCE:**

If one of our agents realize that our team is losing on points or two invaders are constrained by one of our ghosts, the other one will take this opportunity to be more aggressive on offense. 

One a food piece is eaten, the agent makes a decision to either return and deposit the food or to continue to the next closest food and eat that. As the agent eats more food and moves further away from its homeside, it becomes increasingly 'nervous' and is more likely to go back and deposit food rather than continue to venture further into enemy territory. 

If the attacking agent sees a ghost, it begins moving away from it, but still searches for more food. When the ghost begins to close in, the Pacman will begin to move directly away from the ghost towards its own side for safety and to deposit food. If a power capsule is close by, the Pacman will reach the capsule for defence. 

**DEFENCE:**

the defensive ghost would hover along its defend position if no enemy on site.
Once the invading enemy is within line of sight, the defensive ghost agents starts to chase the enemy and if two invaders appear in our home area, the attack agent would be call to help defends. If the invading Pacman eats a power capsule, the ghosts still converge on the invader, but stay one space away for safety. Once the invader powers down, it can be killed instantly. 

These tactics also penalise the STOP action.

# Important notes:

This version's Pacman is more **Defensive** style. If you want to win the competition, it is better to add some offensive features.

All files are completed by my excellent teammate Liang Zhang and I.
