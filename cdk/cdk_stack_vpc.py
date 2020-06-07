from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

class InfraStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        self.vpc = ec2.Vpc(self, "VPC",
                           cidr="10.10.0.0/16",
                           # configuration will create 3 groups in 2 AZs = 6 subnets.
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public",
                               cidr_mask=24
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE,
                               name="Private",
                               cidr_mask=24
                           )])

        self.vpc.add_gateway_endpoint("DynamoDbEndpoint", service=ec2.GatewayVpcEndpointAwsService.DYNAMODB)
        self.vpc.add_gateway_endpoint("S3Endpoint",service=ec2.GatewayVpcEndpointAwsService.S3)
        self.vpc.add_interface_endpoint("EcrDockerEndpoint",service= ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER)

        self.vpc.add_interface_endpoint("EcrEndpoint", service= ec2.InterfaceVpcEndpointAwsService.ECR)

        self.vpc.add_interface_endpoint("Ec2Endpoint", service=ec2.InterfaceVpcEndpointAwsService.E_C2)

        self.vpc.add_interface_endpoint("SSMEndpoint", service=ec2.InterfaceVpcEndpointAwsService.SSM)

        self.vpc.add_interface_endpoint("SSMMessagesEndpoint", service= ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES)

        self.vpc.add_interface_endpoint("ECSEndpoint", service=ec2.InterfaceVpcEndpointAwsService.ECS)

        self.vpc.add_interface_endpoint("ECSAgentEndpoint", service=ec2.InterfaceVpcEndpointAwsService.ECS_AGENT)

        self.vpc.add_interface_endpoint("ECSTelemetryEndpoint",service= ec2.InterfaceVpcEndpointAwsService.ECS_TELEMETRY)

        self.vpc.add_interface_endpoint("CloudFormationEndpoint", service= ec2.InterfaceVpcEndpointAwsService.CLOUDFORMATION)

        # self.azs1 = core.Stack.availability_zones
        # azcount = self.node.try_get_context(self.azs1)
        # print(azcount)
        self.azs = self.vpc.select_subnets(subnet_type = ec2.SubnetType.PRIVATE)

#        num = 0
#        for i in core.Fn.get_azs(region= 'ap-south-1'):
#            ec2.PublicSubnet(self, "PublicSubnet" + str(num), availability_zone= str(i), cidr_block= "10.0." + str(num) + ".0/24", vpc_id = self.vpc.vpc_id)
#            num += 1
