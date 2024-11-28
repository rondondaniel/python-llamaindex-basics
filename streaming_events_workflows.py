from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context,
)
import asyncio
import dotenv
import os
from llama_index.llms.openai import OpenAI
from llama_index.utils.workflow import draw_all_possible_flows

dotenv.load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise Exception("OpenAI API key not found!")

class FirstEvent(Event):
    first_output: str

class SecondEvent(Event):
    second_output: str
    response: str

class ProcessEvent(Event):
    msg: str

class TheWorkflow(Workflow):
    @step
    async def step_one(self, ctx: Context, event: StartEvent) -> FirstEvent:
        print(event.first_input)
        ctx.write_event_to_stream(ProcessEvent(msg="Step one started."))
        
        return FirstEvent(first_output="First step completed!")
    
    @step
    async def step_two(self, ctx: Context, event: FirstEvent) -> SecondEvent:
        llm = OpenAI(model="gpt-4o-mini", api_key=API_KEY)
        generator = await llm.astream_complete("write a short novel about the capital of France?")
        async for response in generator:
            ctx.write_event_to_stream(ProcessEvent(msg=response.delta))

        return SecondEvent(
            second_output="Second step completed!",
            response=str(response),
        )
    
    @step
    async def step_three(self, ctx: Context, event: SecondEvent) -> StopEvent:
        ctx.write_event_to_stream(ProcessEvent(msg="Step three started."))

        return StopEvent(result="Workflow completed!")

async def main():
    w = TheWorkflow(timeout=30, verbose=True)
    handlre = w.run(first_input="Start the workflow.")

    async for event in handlre.stream_events():
        if isinstance(event, ProcessEvent):
            print(event.msg)

    final_result = await handlre
    print(final_result)

    draw_all_possible_flows(TheWorkflow, filename="Streaming_workflow.html")

if __name__ == "__main__":
    asyncio.run(main())