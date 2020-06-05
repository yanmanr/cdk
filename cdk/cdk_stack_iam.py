from aws_cdk import core
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ec2 as ec2
class IAMRoleStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ec_role = iam.Role(self,
                        "FirstRoleCDK",
                        assumed_by= iam.ServicePrincipal("ec2.amazonaws.com"),
                        description= "First Role created by CDK",
                        inline_policies = {
                            "S3IAMFullAccess" : iam.PolicyDocument(
                                statements = [
                                    iam.PolicyStatement(
                                        effect = iam.Effect.ALLOW,
                                        actions = ['s3:*'],
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
        ec_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))

                                                                                                             
