import boto3
import click

session = boto3.Session(profile_name='awschecker')
ec2 = session.resource('ec2')

@click.group()
def instances():
	"commands to list instances"

@instances.command('list')
@click.option('--project', default=None)
def list_instances(project):
	"List all EC2 instances"
	if project:
		filters = [{'Name':'tag:Project','Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	for instance in instances:
		tags = { t['Key']:t['Value'] for t in instance.tags or [] }
		print(', '.join((tags.get('Name',',<no project>'), instance.id,instance.state['Name'],instance.placement['AvailabilityZone'], instance.public_dns_name)))

@instances.command('stop')
@click.option('--project',default=None)

def stop_instances(project):
	"Stop EC2 instances"
	if project:
		filters = [{'Name':'tag:Project','Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	for i in instances:
		print("Stopping {0}...".format(i.id))
		i.stop()
	return		
if __name__ == '__main__':
	instances()
