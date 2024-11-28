from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context,
)
import asyncio
import random
from llama_index.utils.workflow import draw_all_possible_flows

class StepTwoEvent(Event):
    query: str

class ParallelFlow(Workflow):
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> StepTwoEvent:
        ctx.send_event(StepTwoEvent(query="Query 1"))
        ctx.send_event(StepTwoEvent(query="Query 2"))
        ctx.send_event(StepTwoEvent(query="Query 3"))

    @step(num_workers=4)
    async def step_two(self, ctx: Context, ev: StepTwoEvent) -> StopEvent:
        print("Running slow query ", ev.query)
        await asyncio.sleep(random.randint(1, 5))

        return StopEvent(result=ev.query)
    
async def main():
    w = ParallelFlow(timeout=10, verbose=True)
    result = await w.run(first_input="Start the workflow.")
    print(result)
    draw_all_possible_flows(ParallelFlow, filename="basic_workflow.html")

if __name__ == "__main__":
    asyncio.run(main())