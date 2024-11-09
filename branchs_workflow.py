import asyncio
import random
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
from llama_index.utils.workflow import draw_all_possible_flows

class BranchA1Event(Event):
    payload: str

class BranchA2Event(Event):
    payload: str

class BranchB1Event(Event):
    payload: str

class BranchB2Event(Event):
    payload: str

class TheWorkflow(Workflow):
    @step
    async def step_one(self, event: StartEvent) -> BranchA1Event | BranchB1Event:
        if random.randint(0, 1) == 0:
            print("Branch A")
            return BranchA1Event(payload="Branch A1")
        else:
            print("Branch B")
            return BranchB1Event(payload="Branch B1")

    @step
    async def step_a1(self, event: BranchA1Event) -> BranchA2Event:
        print(event.payload)
        return BranchA2Event(payload="Branch A2")

    @step
    async def step_b1(self, event: BranchB1Event) -> BranchB2Event:
        print(event.payload)
        return BranchB2Event(payload="Branch B2")

    @step
    async def step_a2(self, event: BranchA2Event) -> StopEvent:
        print(event.payload)
        return StopEvent(result="Workflow A completed!")
    
    @step
    async def step_b2(self, event: BranchB2Event) -> StopEvent:
        print(event.payload)
        return StopEvent(result="Workflow B completed!")
    
async def main():
    w = TheWorkflow(timeout=10, verbose=True)
    result = await w.run(first_input="Start the workflow.")
    print(result)
    draw_all_possible_flows(TheWorkflow, filename="branchs_workflow.html")

if __name__ == "__main__":
    asyncio.run(main())