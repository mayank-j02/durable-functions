import azure.functions as func
import azure.durable_functions as df

# Create the durable app
app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Activity Function
@app.activity_trigger(input_name="name")
def hello_activity(name: str) -> str:
    return f"Hello {name}"


# Orchestrator Function
@app.orchestration_trigger(context_name="context")
def hello_orchestrator(context: df.DurableOrchestrationContext):
    name = "World"
    result = yield context.call_activity("hello_activity", name)
    return result


# HTTP Starter Function
@app.route(route="hello_start")
@app.durable_client_input(client_name="client")
async def hello_starter(req: func.HttpRequest, client: df.DurableOrchestrationClient) -> func.HttpResponse:
    instance_id = await client.start_new("hello_orchestrator")
    return client.create_check_status_response(req, instance_id)
