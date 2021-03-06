# aws-health-check
Project to perform operations on AWS EC2 instances, volumes, snapshots and security groups


Uses boto3 AWS SDK

Create a aws profile with access to the resources that you intend to monitor

`aws configure --profile=<profile_name>`

Install pipenv
`pip install pipenv`

To run
`pipenv run python awschecks/awschecks.py <resource> <command> <project>`

or

run setup.py to create .whl file
Install the tool and run commands directly:
`awschecks <resource> <comand> <project>``

where
<resource> is instances, volumes, snapshots or securitygroups
<command> is dependent on resource
  instances:
  list, start, stop

  volumes:
  list

  snapshots:
  list, create, copy

  securitygroups:
  list

<project> is optional - Project name tag to filter resources based on Project tag
--project <project_name>
