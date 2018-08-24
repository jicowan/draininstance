# draininstance
A CLI for draining an EC2 container instance of its task. 
This CLI loops through the instances in a cluster (rexray-demo) to find the instance that is running tasks.  When an instance is found, it puts that instance into a draining state. 
