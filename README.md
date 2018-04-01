# ordered-substring-solver
Find ordered substrings that are common to multiple strings

# Example
The strings HELLODARKNESS, DARKNESSHELLO and HEDAKLLKNEOSS all contain the substrings HELLO and DARKNESS in correct order of letter appearance when considering each substring individually.

# Rules
 - Letters can be skipped, but must appear in correct order
 - All letters must be used, thus all strings have the same length

# Usage
Pass the list of strings to process, with optional --benchmark flag  
*solver.py HELLODARKNESS DARKNESSHELLO HEDAKLLKNEOSS --benchmark*

# Possible improvements
Only generate substrings when needed. Right now, for 10 strings, we generate all substrings of those 10 strings. Technically we only need to generate for string 1 and 2, intersect those, then generate for string 3, intersect, string 4, intersect... This would improve memory usage but not processing speed.