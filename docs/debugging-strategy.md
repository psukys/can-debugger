#Debugging strategy

When facing a bunch of data being spitted out with or without any interaction, there needs to be a strategy for crunching data.

Currently the strategy is as follows:
1. Take a root (starting) point, which spits data by simply turning ignition.
2. Start recording - do one action - stop recording.
3. Crunch data

For such strategy we can define a set of test cases, where one test case has the data that flew in during one recording. 
At this point, the root point (i.e. ignition) might also be called the test case, but we should rather call it the root, since we're not directly examining what the values mean.