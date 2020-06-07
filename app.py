#!/usr/bin/env python3

from aws_cdk import core

from cdk.cdk_stack_vpc import InfraStack
from cdk.cdk_stack_ec2 import Ec2Stack
from cdk.cdk_stack_asg import AutoScalingStack
from cdk.cdk_stack_elb import ApplicationLoadBalancerStack 
from cdk.cdk_stack_iam import IAMRoleStack
from cdk.cdk_stack_ecs import ECSStack
from cdk.cdk_stack_lambda import LambdaStack

env_AS = core.Environment(account="320537072716", region="ap-south-1")

app = core.App()

vpc_stack = InfraStack(app, "InfraStack", env = env_AS)

azs1 = vpc_stack.availability_zones
print(azs1)

ec2_stack = Ec2Stack(app, "Ec2Stack", vpc = vpc_stack.vpc, azs = vpc_stack.azs, env=env_AS)

asg_stack = AutoScalingStack(app, 'AutoScalingStack', vpc = vpc_stack.vpc, env = env_AS)

elb_stack = ApplicationLoadBalancerStack(app, 'ApplicationLoadBalancerStack', vpc = vpc_stack.vpc, asg= asg_stack.auto_scaling_group, env = env_AS)

iam_stack = IAMRoleStack(app, 'IAMRoleStack', env= env_AS)

ecs_stack = ECSStack(app, 'ECSStack', vpc= vpc_stack.vpc, env = env_AS)

lambda_Stack = LambdaStack(app, "LambdaStack", env = env_AS)

app.synth()

