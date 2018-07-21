import boto3
import click

session = boto3.Session(profile_name='awschecker')
ec2 = session.resource('ec2')

@click.group()
def cli():
	"Command Line Interface"

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
				print(', '.join((snapshot.id,snapshot.volume_id,instance.id,snapshot.progress,snapshot.state,snapshot.encrypted and 'Encrypted' or 'Not Encrypted')))

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

	for instance in instances:
		for volume in instance.volumes.all():
		#tags = { t['Key']:t['Value'] for t in instance.tags or [] }
			print(', '.join((volume.id,instance.id,volume.state,str(volume.size) + ' GiB',volume.encrypted and 'Encrypted' or 'Not Encrypted')))

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
		print("Starting {0}...".format(i.id))
		i.start()
	return

if __name__ == '__main__':
	 cli()
