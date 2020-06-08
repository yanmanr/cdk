# cdk

Project contains code samples to create AWS Resources using CDK (Code snippets and syntaxes for ready-to-go).

IAM Stack - Sample code on how to create IAM Roles, inline policies and a little more.

ECS Stack: Sample code on how to create clusters (including auto-scaling), services, task definition and loadbalancers. Creates image, push to ecr and use the same image to add container to task defintion for ECS.

LoadBalancer Stack: Sample code on how to create load balancers and add their listeners, health checks while targets groups in place to forward traffic.

EC2 Stack: Create Role for EC2 instance, configure userdata, run/create multiple EC2s using loops. Creates 8 instances along with their roles. Generally can use this if we would like to spin some stack of servers with same config but with diff name where configuration on every server will vary (can use ansible to configure at server level based on name tag for the server, need to add scripts shortly to configure
). 
Lambda Stack: Sample code on how to deploy your lambda functions. Using cdk lambda, deploys many lambda in on go.

VPC Stack: Sample code on how to deploy your vpc infra in one-go and other configurations for your vpc.

More to learn and code.
