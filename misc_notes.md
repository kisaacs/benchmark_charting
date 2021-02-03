### My short analysis on the [Adiak tools (by LLNL)](https://github.com/LLNL/Adiak)

- It just provides an interface to store (in-memory) name-value pairs of subscriber tools
- Storing data in-memory only. (they are storing and then flushing the data when program terminates)
- name-value pairs are being updated using a callback function.
- Tools are being stored in a doubly-linked-list type data structure.
- Used category (hardcoded 4 types) and subcategory (user provided) to organize the name-value pairs

Since this is just a name-value store, need to find out what makes this tool special compared to other sophisticated C++ STL libraries?
what makes this good?

- separate MPI, glib, osx, posix, unix library interfacing
----
### Ways data can be fetched

- Command line parameters
- Separate file
- Separate API functions
- Provide a callback functions (Adiak used this approach)


### Things to address
- How to collect data from the user
- Store and organize the data
- Pass that value to the benchmark tools 
- collect information from the benchmark tools 

#### Idea
user data can be collected directly from the benchmark tools (test its viability and practicality using the blazemark in Rostam)

Pros

- Reduce the step to pass the same data separately this tool and then to the benchmark tool
- One time data collection
- Users do not need to worry about the data passing formats.

Cons

- Multiple benchmark tools. Need some system to generalize this thing
- A benchmark Tool might not output any required parameters

Ways to do this
- PIPE, read through the output and parse it
- Dump benchmark output to a file and read it from there


### Use cases
- add/update/delete any number of parameters and measurements (possibly in key-value format)
- take a subset of the parameters and measurements from an old run and generate a new dataset
- take a subset of the parameters and generate new measurements
- swap different parameters and measurements
- view measurements and parameters from an old benchmark run
- add/remove different benchmarking tools
- get measurement data from multiple benchmarking tools (possibly from a subset of the tools which are added) and save the measurements
- share the data or a subset of the data


### What to do under the hood
With the moto: *define ones, use multiple times*.

- Let users define multiple parameters, and their value range. Automatically generate all possible combination of parameter list.