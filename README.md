# Twitter Coding Challenge

Source codes on Github: https://github.com/liukun2016/TwitterCodingChallenge

### How to run the program?

```
./src/main.py --handler=<handler name> --input_path=<input file> --output_path=<output file> [Optional --verbose=1]
```

### Define the problems and my solutions:

#### 1. The log file is too big to fit in memory on one machine.

<b>Solution</b>: Read each log entry in the input file line by line.

#### 2. There might be missing entries in the log file.
Here I define missing entries as <b>"unpaired"</b> entries as two cases:

&nbsp;&nbsp;
a. The status of the entry is "close", whereas there is no "open" entry <b>before</b> it available, so it is an unpaired "close".
 
&nbsp;&nbsp;
b. The status of the entry is "open", whereas there is no "close" log entry <b>after</b> it available, so it is an unpaired "open".

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
In this case, it can only be known if an "open" entry is unpaired (missing) or not after the last line finished.  

<b>Solution</b>: When read each line, handle unpaired "close" entry, and at the end of the processing, handle those unpaired "open" entries for each user.


### Detailed interface designs and workflow:
 
#### 1. Design

Here as there are various ways to handle unpaired log entries, I design an interface `MissingHandlerInterface` with two methods need to be implemented: `handle_unpaired_open` and `handle_unpaired_close`.

Currently there are 3 implementations/policies to handle missing/unpaired log entries:

&nbsp;&nbsp;
a. Ignore: simply do nothing about those unpaired log entries, so they won't be considered for calculating the average spent time of each user.

&nbsp;&nbsp;
b. Random: randomly pick a time between the global log start or end time and the unpaired log time (start time for "close" entries, end time for "open" entries). Note if the log time is the same as global log start or end time, it will be ignored. 

&nbsp;&nbsp;
c. Average: calculate the average time between the unpaired log time and the gloabl log start or end time. Same as `Random`, if the log time is the same as global log start or end time, it will be ignored as well.
 
#### 2. Workflow

&nbsp;&nbsp;
a. Read each log entry line, parse the user id, log time, and status. Create a entity instance for each user, if not created yet.

&nbsp;&nbsp;
b. If the status is "open", as it is unpaired yet, add it to a FIFO queue of the user.

&nbsp;&nbsp;
c. If the status is "close", if there is any unpaired "open" in the queue, pair this "close" to the first "open", and calculate the duration between them, and update the total duration of the user. Otherwise, handle this unpaired close entry by `handle_unpaired_close` method.

&nbsp;&nbsp;
d. When all lines are processed, iterate each user instance and handle the unpaired "open" log entries in the queue of the user, by `handle_unpaired_open` method.

&nbsp;&nbsp;
e. Save output.

 
### Other comments:

For the interface, if you come up with any other policies/ideas to handle unpaired missing log entries, you need to implement the two interface methods. Those current implementations are very straightforward, and the user stat entity is too simple if we want to handle the missing entries with more complicated ways. For instance, currently only those unpaired open entries will be stored in the queue, but if we want to save all historical open entries so as to handle missing "close" entries based on them, you may have to either change user stat class or define subclass to overwite some methods/fields.


For testing, I haven't thoroughly tested the program. However, there are already some test cases provided here under `sample_inputs` and output created under `sample_outputs`. It was manual test, not unit or functional test.

This is a coding challenge, not a real production level codes. So besides those two simplifications above, there are some others. For instance, there is no input format validation, no exception handling, and no logging mechanism.
