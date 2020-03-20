# Yuki Lang

Yuki Lang is a simple functional language that I'm develop whit hope to learn about compilers 

## Dependences  
* Python3
* [Lark](https://github.com/lark-parser/lark)  

## Usage 

Just run one of 

~~~ssh
python3 main.py 
~~~

~~~ssh
python3 trees.py
~~~

## TODO 

* Implement a G-machine in C to run the program 
* Implement types
* Implement scopes
* Implement pattern matching
* Implement reduction of tree to G-machine code
* Chosse betwen byte-code like or string (human readable) code generacion for the G-machine

## Current status 

* Console
    * Is for debug, currently shows the pretty printed tree of expression 
    * Console saves history of commands
    * Accepts :b [int] and :l [int] commands to show previus commands or to execute a previus command
    * TODO : Use curses python module to re-write (i don't want to do this now.)
* Language grammar
    * Only can handle name of functions and no numeric values
    * Just can define combinators and evals
* BTree
    * Suports pretty printing of nodes


