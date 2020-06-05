from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_autoscaling as autoscaling
import base64

class AutoScalingStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        amzn_linux = ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                                              edition=ec2.AmazonLinuxEdition.STANDARD,
                                                              virtualization=ec2.AmazonLinuxVirt.HVM,
                                                              storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE)
        linux = ec2.MachineImage.generic_linux({
                    "ap-south-1": "ami-0b9d66ddb2a9f47d1"})

        data = open("./scripts/userdata/userdata.sh", "rb").read()
        user_data=ec2.UserData.for_linux()
        user_data.add_commands(str(data,'utf-8'))

        self.auto_scaling_group = autoscaling.AutoScalingGroup(self,
                                                            "FirstASG",
                                                            instance_type=ec2.InstanceType('t2.micro'),
                                                            machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2),
                                                            vpc = vpc,
                                                            user_data = user_data,
                                                            desired_capacity = 6,
                                                            key_name = "ap-south-1",
                                                            min_capacity = 1,
                                                            vpc_subnets = ec2.SubnetSelection(availability_zones=["ap-south-1a","ap-south-1b"])
                                                            )
