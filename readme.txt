This code uses a library called "copy", but it should be included in your python installation as default library.

I have tested the code with python 3.7.4 and 3.9.4 so atleast they work. Most likely many older (and newer) python versions also work.

This code might run on python 2.7 but DO NOT USE python 2.7 today. Please use python 3.x to run my code.

If you have your own tests, then you can call calculateMaxFlow function to run them. It needs following parameters: -graphfile location
-setfile location

To run my implementation just run FF_template.py file:
$ python FF_template.py

or

$ python3 FF_template.py

Make sure to be in this folder to make sure that the tests load okay

I tried running testdata folder's 100k test files but they will run REALLY REALLY long. (I waited 30minutes :D)