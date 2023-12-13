# Cosmic-Crusader
Platformer videogame set in space

START:
The start page will run the game once you press the icon.

OVERWORLD:
Here, the player will navigate through the unlocked levels with the arrow keys. 
If the player presses the space bar, the level will run normally.
If the player presses 'h', the level will load a ghost runner that has learnt the most convenient path.

LEVELS and storyline:
The levels are ordered in a such a way, to represent how the game would work if it were developed in a bigger scale. 
Our character must use the obelisk (or flying stone) to get into the labs that a company has set up in different planets, asteroids, and moons.

- On the first level (Earth), the player will learn how to move with the arrow keys. Some static enemies are displayed.
- Level 2 (Moon) shows an NPC enemy that has been programmed to act in a determined way.
- The last level shows an upgraded enemy that acts based on its position and the position of our character. It will follow it indefinitely until they collide.

RETURNING:
To return to the overworld the player can press the Escape key.

DEATH:
If a player loses all its hearts, the game will be over. Make sure to get as many hearts as possible. 
Coins and diamonds might be of help. Once you obtain one hundred, you will get an extra life.

GHOST RUNNER:
For all levels, the ghost runner can be used as an extra help for reaching the obelisk. It should guide you through the level, to complete it as fast as possible.
However, on level (Fire), the ghost runner will race the player until the end. If it reaches the obelisk before the player, they will be returned to the overworld.

--> The path for the ghost runner was created following the principle of Q-learning. The lists in the file 'map_info' were used as a matrix were each character represented a state. Based on the rewards of each action, the J tiles or Jump tiles have been added in specific parts of the map. This was done through trial and error using random movements, which is basically how this type of process learns.

NO WIN?
Cosmic Crusader cannot be won. It was created to represent a basis of what could be a bigger game. Having set up all files, creating new levels is not as time-consuming. By not winning, the player can play all levels as many times as they want, with or without the ghost runner.
