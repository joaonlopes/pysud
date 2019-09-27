README.md
=========

Introduction
------------

The modules pỳsud_xml and pysud_make can be used to parse xml files
and generate an initial game data file.

pysud_xml provides xml parsers for two kind of files:

* configuration file
* rooms data file

pysud_make uses pysud_xml to populate a new pysud.Game object and persist it
using pysud_gm.

Basic usage
-----------

Set game configuration variables in a *config.xml* file.

Set game rooms descriptions (and optionally possible transitions) in a
new file called *rooms.xml*.

Examples for both xml files can be found in this directory. Those are meant to be played with the script */demos/demoscript_2.py*.

Execute pysud_make to create a new game.data file. This file can be loaded from
using pysud_gm.GameManager.load_game_data().

NOTE: This modules needs to be on the same directory as the xml files and the
rest of the pysud modules.
