from aws_cdk import core
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ec2 as ec2

with open("./scripts/userdata/userdata.sh") as f:
    user_data = f.read()


class Ec2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, azs, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        amzn_linux = ec2.MachineImage.latest_amazon_linux(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                                              edition=ec2.AmazonLinuxEdition.STANDARD,
                                                              virtualization=ec2.AmazonLinuxVirt.HVM,
                                                              storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE)

        linux = ec2.MachineImage.generic_linux({
                    "ap-south-1": "ami-0b9d66ddb2a9f47d1"})
        instance_role = iam.Role(self,
                        "InstanceRole",
                        assumed_by= iam.ServicePrincipal("ec2.amazonaws.com"),
                        description= "ECS Instance Role",
                        path = "/",
                        inline_policies = {
                            "s3-access-policy" : iam.PolicyDocument(
                                statements = [
                                    iam.PolicyStatement(
                                        effect = iam.Effect.ALLOW,
                                        actions = ['kms:*'],
                                        resources = [
                                            '*'
                                        ]
                                    ),
                                    iam.PolicyStatement(
                                        effect = iam.Effect.ALLOW,
                                        actions = ['iam:*'],
                                        resources = [
                                            '*'
                                        ]
                                    ),
                                ]
                            )
                        }
                        )
        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2ContainerServiceforEC2Role"))

        iam_profile = iam.CfnInstanceProfile(self,
                                            "CDKInstanceProfile",
                                            roles= [instance_role.role_name],
                                            path="/")

        count, num = 8, 0

        az_count = len(azs.availability_zones) #Fetch list/count of azs from Infra(VPC) Stack

        instance_securitygroup = ec2.SecurityGroup(self,
                                                "WeblogicSecurityGroup",
                                                vpc = vpc,
                                                description = "WeblogicSecurityGroup",
                                                security_group_name = "WeblogicSecurityGroup")

        instance_securitygroup.add_ingress_rule(ec2.Peer.ipv4("192.168.12.21/32"),
                                                ec2.Port.tcp(22),
                                                description = "SSH Access"
                                                )
        for i in range(count):

            instance_first = ec2.Instance(self, f"awsweblogic{i}d", vpc=vpc, instance_name= "AWS" + str(i), role = instance_role, 
                                        availability_zone = azs.availability_zones[num], security_group = instance_securitygroup,
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

            if int(az_count)-1 == num:
                num = 0

            num += 1

#Notes to review: CDK creates instance profile everytime while creating instance rather than re-use. Issue: https://github.com/aws/aws-cdk/issues/8348
# Above script creates instances one in each azs with 8 instances in total spread across each az. Configuration will differ and vary like in case of configuring web-logic servers, if we need 8 servers as worker nodes but configuration differs, here we can use ansible to run playbooks for configuration.
