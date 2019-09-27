about
=====
pysud is a tool aimed at helping to create text adventures games
(Collosal Cave for example) and gamebooks (like those
"Choose Your Own Adventure" book series ).

pysud is an object oriented library that uses a main loop and an
internal event mechanism to distinguish when something "interesting" has
happened (either entering a specific command, use of certain object by 
player, etc..). 

Currently it provides classes to represent the game, the player, the
rooms a player can visit and the items a player could collect and use.
Also a hierarchy with common game events (such as collecting an item,
moving to another room...) is provided. 

pysud is developed and tested in python3.

license 
=======
pysud (all modules that compose it and the accompanying demos) are 
released under a lgpl3 license. See files COPYING and COPYING.LESSER.
