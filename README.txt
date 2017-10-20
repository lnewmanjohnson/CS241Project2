
Team:
  <awchen19@amherst.edu;lnewmanjohnson18@amherst.edu>

Evaluation function for Q5:
  <We evaluated the number of capsules left, the number of food left; as well as an a 1/distance from food, ghost, and capsule; and if the Ghost is scared or not. We returned a value by adding together those values in a way that weights their importance. When the ghost was scared, we wanted pacman to chase and eat the ghost, and that to be more important than eating the food, so we left out the part of the function about food, and increased the weight of the distancefromghost. Otherwise, we wanted to encourage pacman to eat food and capsules by subtracting the number of food and capsules from the total value. This means the result of the function would increase as the number of food and capsules decreased. We also weighted currGhostDistance as higher than the rest because it is most important that Pacman doesn't get eaten by the ghost.>

Resources used:
  <We used GitHub to share code with eachother, also stack overflow to look up how python works>

Time spent on assignment: <10 hours>

On a scale from -2 to 2:
  How hard was the assignment? 
  <0>
  
How much did you learn from the assignment? 
  <1>
  
How much did you enjoy the assignment? 
  <0>
Additional notes: <Pacman was cute.>