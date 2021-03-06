# cf_logging ROS package

Additional package for the crazyswarm project for saving the specified log-variables from the crazyflies into CSV files

## Installation & Usage
   1. Load your crazyswarm project or the latest version from the [USC-ACTLab](https://github.com/USC-ACTLab/crazyswarm)
   2. Execute following command in the crazyswarm project directory to add `cf_logging` as submodule to the project into the folder `ros_ws/src/`:  
      `git submodule add https://github.com/PDfork/cf_logging ros_ws/src/cf_logging`
   3. Edit the `ros_ws/src/crazyswarm/launch/hover_swarm.launch` file and make sure, following lines are present and uncommented:  
      ```
      <node pkg="crazyswarm" type="crazyswarm_server" name="crazyswarm_server" output="screen" >
         <rosparam>
            genericLogTopics: ["log1"]  
            genericLogTopicFrequencies: [10]  # frequency in ms
            genericLogTopic_log1_Variables: ["log_group.log_variable", ...]  # log variables from the CFs, like "stabilizer.x"
            enable_logging: True
         </rosparam>
      </node>
      <include file="$(find cf_logging)/launch/cf_logging.launch" />
      ```
   4. Build your project as usual with `./build.sh`
   5. Get the log data from the folder `ros_ws/src/cf_logging/data` (The data is separated into folders with its corresponding timestamp and each CF has its own CSV file)
