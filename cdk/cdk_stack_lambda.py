from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    core,
)


class LambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        for i in ["lambda-handler", "lambda-handler1", "lambda-handler2" ]:

            with open(f"./scripts/{i}.py", encoding="utf8") as fp:
                handler_code = fp.read()
    
            lambda_function = lambda_.Function(
                self, f"MyFun-{i}",
                code=lambda_.InlineCode(handler_code),
                handler="index.main",
                timeout=core.Duration.seconds(300),
                runtime=lambda_.Runtime.PYTHON_3_7,
            )


#alternative way to achieve above functionality
            lambda_function = lambda_.Function(
                self, f"MyFun-{i}",
                code=lambda_.Code.asset("scripts"),,
                handler=f"{i}.main",
                timeout=core.Duration.seconds(300),
                runtime=lambda_.Runtime.PYTHON_3_7,
            )

