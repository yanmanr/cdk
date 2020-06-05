from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb

class ApplicationLoadBalancerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, asg, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lb = elb.ApplicationLoadBalancer(
            self, "FirstLoadBalancer",
            vpc=vpc,
            internet_facing=True,
            vpc_subnets=ec2.SubnetSelection(availability_zones=["ap-south-1a","ap-south-1b"]))
        listener_http = lb.add_listener("ListenerHttp",port=80,
                                    protocol=elb.ApplicationProtocol.HTTP)

        listener_http.add_targets("HttpTargetGroup",
                                    port=80,
                                    protocol=elb.ApplicationProtocol.HTTP,
                                    targets=[asg])

        listener_http.connections.allow_default_port_from_any_ipv4("Open to the World")
