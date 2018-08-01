import boto3
import click

session = boto3.Session(profile_name='awschecker')
ec2 = session.resource('ec2')

client = boto3.client('ec2')

@click.group()
def cli():
	"Command Line Interface"

@cli.group('securitygroups')
def sg():
	"Commands for security groups"
@sg.command('list')
#@click.option('--project', default=None)
def list_groups():
	"List all security groups"
	response = client.describe_security_groups()
	mylist = response["SecurityGroups"]
	i=0
	print("Group Name\t\tGroup ID\t\tDescription\t\t\t\tVPC ID")
	print("-------------------------------------------------------------------------------------------------------------")
	while i < len(mylist):
		print(' | '.join((mylist[i]["GroupName"], mylist[i]["GroupId"],mylist[i]["Description"], mylist[i]["VpcId"])))
		i+=1

	return

@cli.group('snapshots')
def snapshots():
	"Commands for snapshots"
@snapshots.command('list')
@click.option('--project', default=None)
def list_snapshots(project):
	"List all snapshots"
	if project:
		filters = [{'Name':'tag:Project','Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	for instance in instances:
		for volume in instance.volumes.all():
			for snapshot in volume.snapshots.all():
		#tags = { t['Key']:t['Value'] for t in instance.tags or [] }
				print(', '.join((snapshot.id,snapshot.volume_id,instance.id,snapshot.progress,snapshot.start_time.strftime("%c"),snapshot.state,snapshot.encrypted and 'Encrypted' or 'Not Encrypted')))

	return

@snapshots.command('create')
@click.option('--project', default=None)
def create_snapshots(project):
	"Create snapshots"
	if project:
		filters = [{'Name':'tag:Project','Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	for instance in instances:
		instance.stop()
		print('Stopping instance {0} ...'.format(instance.id))
		instance.wait_until_stopped()
		print('Instance {0} stopped'.format(instance.id))
		for volume in instance.volumes.all():
			volume.create_snapshot(Description='Snapshot for volume {0}'.format(volume.id))
			print('Snapshot initiated for volume {0} on Instance {1}'.format(volume.id, instance.id))

		instance.start()
		print('Instance {0} started'.format(instance.id))

	return

@snapshots.command('copy')
@click.option('--project', default=None)
def copy_snapshots(project):
	"Copy snapshots"
	if project:
		filters = [{'Name':'tag:Project','Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	for instance in instances:
		for volume in instance.volumes.all():
			for snapshot in volume.snapshots.all():

				snapshot.copy(SourceRegion='us-east-2')
				print('Copy initiated for {0}'.format(snapshot.id))


	return

@cli.group('volumes')
def volumes():
	"Commands for volumes"
@volumes.command('list')
@click.option('--project', default=None)
def list_volumes(project):
	"List all volumes"
	if project:
		filters = [{'Name':'tag:Project','Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	print('VolumeId\t\tInstanceId\tStatus\t   Size\tEncryption')
	print('-------------------------------------------------------------------------------------------------')

	for instance in instances:
		for volume in instance.volumes.all():

			print(' '.join((volume.id,instance.id,volume.state,str(volume.size) + ' GiB',volume.encrypted and 'Encrypted' or 'Not Encrypted')))

	return

@cli.group('instances')
def instances():
		"""Commands to list instances"""

@instances.command('list')
@click.option('--project', default=None)
def list_instances(project):
	"List all EC2 instances"
	if project:
		filters = [{'Name':'tag:Project','Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	print('Name\t\tID\t\tStatus\t\tRegion\t\tVPC\t\tDNS')
	print('------------------------------------------------------------------------------------------------------------------------')
	for instance in instances:
		tags = { t['Key']:t['Value'] for t in instance.tags or [] }
		print(' '.join((tags.get('Name',',<no project>'), instance.id,instance.state['Name'],instance.placement['AvailabilityZone'], instance.vpc_id, instance.public_dns_name)))

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
		if i.state['Name'] == 'running':
			print("Stopping instance {0}...".format(i.id))
			i.stop()
		else:
			print('Instance {0} already stopped or not in a state to be stopped'.format(i.id))
	return

@instances.command('start')
@click.option('--project',default=None)

def start_instances(project):
	"Start EC2 instances"
	if project:
		filters = [{'Name':'tag:Project','Values':[project]}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()

	for i in instances:
		if i.state['Name'] == 'stopped':
			print("Starting instance {0}...".format(i.id))
			i.start()
		else:
			print('Instance {0} already started or not in a state to be started'.format(i.id))
	return

if __name__ == '__main__':
	 cli()
