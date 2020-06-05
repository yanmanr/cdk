from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
with open("./scripts/userdata/userdata.sh") as f:
    user_data = f.read()

class Ec2Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        amzn_linux = ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                                              edition=ec2.AmazonLinuxEdition.STANDARD,
                                                              virtualization=ec2.AmazonLinuxVirt.HVM,
                                                              storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE)

        linux = ec2.MachineImage.generic_linux({
                    "ap-south-1": "ami-0b9d66ddb2a9f47d1"})
        instance_first = ec2.Instance(self, 'FirstInstance', vpc = vpc ,
                                    user_data=ec2.UserData.custom(user_data), instance_type=ec2.InstanceType('t2.micro'), machine_image=linux)

        instance_first.instance.add_property_override("BlockDeviceMappings", [{
                                                                    "DeviceName": "/dev/xvda",
                                                                    "Ebs": {
                                                                                "VolumeSize": "40",
                                                                                "VolumeType": "gp2",
                                                                                "DeleteOnTermination": "true"
                                                                            }
                                                                    },
                                                                    {
                                                                        "DeviceName": "/dev/sdf",
                                                                        "Ebs": {"VolumeSize": "30"}
                                                                    }
                                                                    ])

