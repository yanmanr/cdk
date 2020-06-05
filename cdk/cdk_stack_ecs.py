from aws_cdk import core
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_autoscaling as autoscaling

ec2_type = "t2.micro"


#linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
#                                 edition=ec2.AmazonLinuxEdition.STANDARD,
#                                 virtualization=ec2.AmazonLinuxVirt.HVM,
#                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
#                                 )

class ECSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

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
                                ]
                            )
                        }
                        )
        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        instance_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2ContainerServiceforEC2Role"))


        task_execution_role = iam.Role(self,
                                        "TaskExecutionRole",
                                        assumed_by= iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
                                        description= "ECS Task Execution Role"
                                       )
        task_execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"))

        self.ecs_asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                    vpc=vpc,
                                                    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                                    instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                    machine_image=ecs.EcsOptimizedImage.amazon_linux(),
                                                    desired_capacity=2,
                                                    min_capacity=2,
                                                    max_capacity=2,
                                                    role= instance_role
                                                   )

        cluster = ecs.Cluster(self, "Cluster",
                                vpc=vpc,
                                cluster_name="NginxECSCluster"
                                )


        cluster.add_auto_scaling_group(self.ecs_asg),
