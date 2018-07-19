import boto3
import click

session = boto3.Session(profile_name='awschecker')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
	"List all EC2 instances"
	for i in ec2.instances.all():
		for tag in i.tags:
			if[tag['Key'] == 'Name']:
				name = tag['Value']

		print(', '.join((name, i.id,i.state['Name'],i.placement['AvailabilityZone'], i.public_dns_name)))

if __name__ == '__main__':
	list_instances()
