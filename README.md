# Code repository for coding challenge adventofcode2018  
https://adventofcode.com/2018

Run make on a BASH shell.  
  
Create new day code:  
<code>make create dayname="01 DayTitle"</code>  
  
Delete day code:  
<code>make delete day=01</code>    
  
If there is more than 1 test case, sepearte test cases in file <code>input_testxx.txt</code> with <code>#####INPUT_SEPERATOR#####</code>.  
Example - <code>input_test01.txt</code> with 3 test cases:  
<code>
1 2
3 4
#####INPUT_SEPERATOR#####
5 6
7 8
#####INPUT_SEPERATOR#####
9 10
11 12
</code>