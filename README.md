### Why would anyone use this tool

- Integrated benchmark run
- data share (sqlite3 is most common and favorite among data analyst)
- Jupyter integration
- Written as a python library
- Convenience
- Possibility of using cloud based PAAS (TAAC, AGAVE, etc.) for benchmark run.*

\* Not sure about this. Do we really need to add this as a feature?

### Assumptions

- User has prior experience with Jupyter notebook, python, and sqlite3.
- User has prior knowledge of python charting libraries like plotly, matplotlib, etc.
- Benchmarking tools should be preconfigured. Just need to provide the directory of the executable file and relevant command line argument parameters. (Right
 now, only testing with [blazemark](https://bitbucket.org/blaze-lib/blaze/wiki/Blazemark) using [HPX](https://github.com/STEllAR-GROUP/hpx) as backend.)
- This tool only supports chart types having data points in 2-D axis for a set of legends. (Line-chart, scatter-plot, bar-chart, etc.)

### Workflow
![Workflow](figs/workflow.png)


### Database Design
![Database](figs/dbschema.png)

- The `charts` table will hold the information for a specific chart (its name, create date, who created it, x-title, y-title, and legends).
- The `data_points` table will hold the information for a specific data point of a chart. A foreign key indexing has been used to identify the relationship
 between the data-point and the chart. (Specifically which chart a datapoint belongs to)
- The `settings` table will hold additional static and global parameters in key-value format.
- The `legends` column in `charts` table will hold string of comma separated legend title. (Example: `key1, key2, key3`)
- The `legends` column in `data_points` table will hold JSON string. (Example: `{key1:value, key2:vaule2, key3:value3}`)
- The `platform` column will hold the name of a specific benchmark tool. During a benchmark run for a row in `data_points`, it will first find the platform
 name from this column, and then, find the executable file location from the settings table, and then it will run that executable file with the values of
  this row.  

### This bencharmk charting library will provide convenient functions
(A user should be able to use these functions from the Jupyter notebook just by importing this library)
- Create a blank chart (provide chart name, x-axis title, y-axis title, legends, etc. Specifically this will add an entry in the `charts` table)
- Add a datapoint in the chart (This will add an entry in the `data_points` table)
- Add legends in the chart (it will create multiple data points for all possible combination of legend parameters and insert them in the `data_points` table)
- Update or remove legends.
- Swap a specific legend 
- Add benchmark platform (This will add the location of the executable file and required arguments in the `settings` table)
- Run benchmark for specific data points (from the `data_points` table, this will update the `y_value` column)
- Generate plot (from an entry in the `charts` table)

