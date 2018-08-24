import boto3, sys, argparse, ConfigParser

parser = argparse.ArgumentParser()
parser.add_argument("--region", help="The name of the AWS region where you've deployed your cluster")
args = parser.parse_args()

if args.region == None:
    print "Please specify a region.\nUSAGE: draininstance --region <aws_region>"
    sys.exit()
else:
    aws_region = args.region

cluster_name = 'rexray-demo'

ecs = boto3.client('ecs', region_name=aws_region)
cluster = ecs.list_container_instances(cluster=cluster_name, status='ACTIVE')
container_instances = cluster.pop('containerInstanceArns')

for container_instance in container_instances:
    has_tasks = ecs.list_tasks(
        cluster=cluster_name,
        containerInstance=container_instance,
        desiredStatus='RUNNING'
    ).pop('taskArns')
    instance_id = container_instance[container_instance.rfind('/')+1:-1]
    if has_tasks != []:
        print "Draining instance %s of tasks" % instance_id
        ecs.update_container_instances_state(
            cluster = 'rexray-demo',
            containerInstances = [ container_instance ],
            status = 'DRAINING'
        )
    else:
        print "No tasks running on %s" % instance_id
