#User experience or simply - Usage

Even though this application is capable of some data manipulation the real value comes in what ways the manipulation can be handled. This document defines the specific ways in handling data.

In any case there is a need for having root and target defined thus this should be mandatory and could be defined through two ways:
 - Defined as command line parameters;
  * Option `-s X` or `--source=X` sets X as the source/root file;
  * Option `-t X` or `--target=X` sets X as the target file.
 - Prompted interactively after starting the program.

Having in mind that the root file is usually the same, this could be saved in a configuration file, thus making only one parameter - target file - mandatory. JSON is readable, if formatted right. 

Another big concern is defining what is the default routine if only root and target files are given. I had a discussion with myself and decided to choose that by default the program would go into interactive mode where the user decides what to do.
An important note is that data is sorted through time frame and whenever it does not change, there should be a counter showing the amount of occurences rather than spamming the screen.

######NOTE:
addresses are only different when there's data difference rather than count/order difference. This is because the test case is like wild west, expect anything.

##Interactive mode
The user receives a list of addresses that have data differences and is prompted for choosing a single address. If there are a lot of addresses, the user can, let's say, input 'all' for getting full output of differences.

In command line this would look like (note that this is only an example:

    Addresses that have different data:
    [ABC123, 00A32F, 789EEE]
    Which address to display?:

By choosing one address there would simply be two listing of what data is outputted in there.

    Which address to display?: ABC123
    -- ROOT --
    [time_started] 0000246 count:10
    [time_started] 00104AC count:5
    [time_started] 0000246 count:3
    ...
    -- TARGET --
    [time_started] 0000246 count:9
    [time_started] 0505050 count:5
    [time_started] 00104AC count:3
    ...

##Command line mode
This mode is defined through interactiveless processing, where the parameters and actions are already defined when starting the application.

Since command line is all about neat functions and crunching data SOMEWHERE, we need to introduce several more command line parameters:
 - Option `-o X` or `--output=X` defines where the results should be output;
 - Option `-f X` or `--format=X` defines the format in which results will be output. Available formats:
  - `text` a simple text representation which would be equivalent to `all` in interactive mode
  - `csv` a spreadsheet format where data is output for later conversions to xls, ods or other formats.