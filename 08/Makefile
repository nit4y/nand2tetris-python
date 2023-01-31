# Makefile for a script (e.g. Python)

## Why do we need this file?
# We want our users to have a simple API to run the project. 
# So, we need a "wrapper" that will hide all  details to do so,
# thus enabling our users to simply type 'VMtranslator <path>' in order to use it.

## What are makefiles?
# This is a sample makefile. 
# The purpose of makefiles is to make sure that after running "make" your 
# project is ready for execution.

## What should I change in this file to make it work with my project?
# Usually, scripting language (e.g. Python) based projects only need execution 
# permissions for your run file executable to run. 
# Your project may be more complicated and require a different makefile.

## What is a makefile rule?
# A makefile rule is a list of prerequisites (other rules that need to be run 
# before this rule) and commands that are run one after the other. 
# The "all" rule is what runs when you call "make".
# In this example, all it does is grant execution permissions for your 
# executable, so your project will be able to run on the graders' computers. 
# In this case, the "all" rule has no preqrequisites.

## How are rules defined?
# The following line is a rule declaration: 
# all:
# 	chmod a+x VMtranslator

# A general rule looks like this:
# rule_name: prerequisite1 prerequisite2 prerequisite3 prerequisite4 ...
#	command1
#	command2
#	command3
#	...
# Where each preqrequisite is a rule name, and each command is a command-line 
# command (for example chmod, javac, echo, etc').

# Beginning of the actual Makefile
all:
	chmod a+x *

# This file is part of nand2tetris, as taught in The Hebrew University, and 
# was written by Aviv Yaish. It is an extension to the specifications given
# in https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017),
# as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
# Unported License: https://creativecommons.org/licenses/by-nc-sa/3.0/
