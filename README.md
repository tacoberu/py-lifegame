py-lifegame
===========

## Use
Run by: `python main.py`

## Description
Consider a representation of a "world" as an n by n matrix. Each element in
the matrix may contain 1 organism. Each organism lives, dies and reproduces
according to the following set of rules:

- If there are two or three organisms of the same type living in the elements surrounding an organism of the same, type then it may survive. 
- If there are less than two organisms of one type surrounding one of the same type then it will die due to isolation. 
- If there are four or more organisms of one type surrounding one of the same type then it will die due to overcrowding.
- If there are exactly three organisms of one type surrounding one element, they may give birth into that cell. The new organism is the
same type as its parents.   If this condition is true for more then one
species on the same element then species type for  the new element is chosen randomly. 
- If two organisms occupy one element, one of them must die (chosen
randomly) (only to resolve initial conflicts).

The "world" and initial distribution of organisms within it is defined by
an XML file of the following format:

	<?xml version="1.0" encoding="UTF-8"?>
	<life>
	    <world>
	        <cells>n</cells> // Dimension of the square "world"
	        <species>m</species> // Number of distinct species
	        <iterations>4000000</iterations> // Number of iterations to be calculated
	    </world>
	    <organisms>
	        <organism>
	            <x_pos>x</x_pos> // x position
	            <y_pos>y</y_pos> // y position
	            <species>t</species> // Species type
	        <organism>
	    </organisms>
	</life>


After  iterations, the state of the "world" is to be saved in an XML file, out.xml, of the same format as the initial definition file.

It is possible to realise visual output using http://www.pygame.org/news.html .

Code should be understandable and commented. If it is not obvious from the
code or comments then the code should be supplied with a written overview of the
application structure and thought processes.

The aim is not speed of implementation, rather a "beautiful" solution.  
However, an overcomplicated solution is not desired, (conditions are fixed,
think only in 2d n by n, the number of species can be limited to a maximum of 5).
