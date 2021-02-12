### Inputs: input types we want to consume
- Actual data from the experiments (time it took, perf csv, etc) *
- Command line command that they ran (flags, number of threads, executable), that gets parsed so that individual flags are (potential) columns in the output *
- Fixed arbitrary metadata (e.g. load a json, csv, xml file) *
- Ad-hoc arbitrary metadata (e.g. --json {"weird thing I did with this run": "details"}) *
- environment variables that were set, timestamp when it was run, etc. ^
- JetLag/Jupyter metadata (instead of command line / environment variables) ^

##### Some more possible consumable input types
- URLs (not from the response, from the URL itself)
- inline code or markup
- Standard command line output
- Any predefined database (mysql, postgresql, nosql, etc.)
- Object of any class when using any additional library
- Any debugger tool (ex. using *gdb* with `info local` command)
- From the log data of any 3rd party analytic tool
- Old document (really old run where the results were reported formally as a PDF document or powerpoint slide)


##### Additional data not used as a parameter for the program during the benchmark run but still require to capture

- environment variables, timestamp ^
- Hardware or system information (output of `lscpu`, `top`, etc.)

<sup>\* By Kate during the meeting at 5th February 2021,</sup>
<sup>^ from Alex's note</sup>

### What could/should this workflow even look like?
- wrapped command line that forwards commands to an actual one / intercepts the output from the real one?
- a script that consumes .bash_history?
- some kind of notebook interface where people paste things?

### Workflow from users’ perspective
-	Prepare the parameters
-	Prepare the programs for the measurements
-	Pass the parameters to the program
-	Use another program (benchmark, profiler) to manage the parameters and measurement
-	Get the measurements and the parameters, organize it in a specific place
-	Pass these to the plotter program



### Some Step by Step process

Scenario 0
1.	Use inline parameters
2.	Import different program (what’s performance is needed to measure)
3.	Comment in/out related portion
4.	Calculate required measured values
5.  Plot using any plotter library (matplotlib, plotly, etc.) 

Scenario 1
1.	Use inline parameters
2.	Import different program (what’s performance is needed to measure)
3.	comment in/out related portion
4.	run the program from command line and write the measured values and parameters in
a.	Directly to a file
b.	To a command line as stdout, then redirect the output to a file
5.	Read the measured value from the file with that specific format parser and write it out to another CSV file in specific plot configuration.
6.	Open that CSV file in plotter program (Excel or OriginPro).

Scenario 2
1.	Write a profiler (a separate program) to run the program a specific number of times and output its measurement values in a specific format.
2.	Let the profiler read from a config file.
3.	Run the profiler and output to a file.
4.	Make the filename related to the input parameters.
5.	Manually copy paste the measured values and parameters in the plotter program(Excel or OriginPro).

Scenario 3 (with some kind of visual tool running over backend API accessible through url)
1.	Intercept URLs.
2.	Paste the URLs in excel and parse the parameters from the url (excel’s “text to column” feature)
3.	Update the corresponding measured values manually.

Scenario 4
1.	Use a config file for the parameters
2.	Use a benchmark program which will read from the config file.
3.	The benchmark program runs an intended program a specific number of times and output (stdout) its measurement values in its default output format.
4.	Manually record the measured values.

Scenario 5
1.	Use a config file for the parameters
2.	Use a benchmark program which will read from the config file.
3.	The benchmark program runs an intended program a specific number of times and output (stdout) its measurement values in its default output format.
4.	Read the measured value from the file with that specific format parser and write it out to another CSV file in specific plot configuration.
5.	Open that CSV file in plotter program(Excel or OriginPro).

Scenario 6
1.	Manually run the benchmark in machine1 and dump the output to a file
2.	Manually run the benchmark in machine2, dump the output to a file, and so on.
3.	Collect the output using scp (or any other convenient method) and put it in a central location 
4.	Combine the dumped output file and make a single file with the measurements and parameters
5.	Parse and prepare it for plotting

Scenario 7
1.	Write a script to run the benchmark in multiple machines
2.	Make the script to dump output to a local file after completion.
3.	Collect the output using scp and put it in a central location 
4.	Combine the dumped output file and make a single file with the measurements and parameters
5.	Parse and prepare it for plotting

Scenario 8
1.	Write a script to run the benchmark in multiple machines
2.	Read the output stream and redirect it to a location file
3.	Combine the dumped output file and make a single file with the measurements and parameters
4.	Parse and prepare it for plotting

Scenario 9
1.	Use benchmark tool1 to get measurement and write it out to a file
2.	Use benchmark tool2 to get measurement and write it out to a file
3.	If done on multiple machines, then move all output file in a central location.
4.	Combine the output file and make a single file with the measurements and parameters
5.	Parse and prepare it for plotting

Scenario 10
1.	Save the data described from any above mentioned scenario
2.  Rerun with the exact parameters to get the same measurements again.
3.  Save the measurements

Scenario 11
1.	Save the data described from any above mentioned scenario
2.  Rerun with some additional parameters to get the same measurements again.
3.  Save the measurements  

Scenario 12
1.	Save the data described from any above mentioned scenario
2.  Rerun with some additional parameters to get the new measurements.
3.  Save the measurements  
