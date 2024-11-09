import asyncio
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
import random
from llama_index.utils.workflow import draw_all_possible_flows

class FirstEvent(Event):
    first_output: str

class SecondEvent(Event):
    second_output: str

class LoopEvent(Event):
    loop_output: str

class TheWorkflow(Workflow):
    @step
    async def step_one(self, event: StartEvent | LoopEvent) -> FirstEvent | LoopEvent:
        if random.randint(0, 1) == 0:
            print("bad luck, loop again")
            return LoopEvent(loop_output="Back to step one!")
        else:
            print("good luck, continue")
            return FirstEvent(first_output="First step completed!")
    @step
    async def step_two(self, event: FirstEvent) -> SecondEvent:
        print(event.first_output)
        return SecondEvent(second_output="Second step completed!")
    
    @step
    async def step_three(self, event: SecondEvent) -> StopEvent:
        print(event.second_output)
        return StopEvent(result="Workflow completed!")
    
async def main():
    w = TheWorkflow(timeout=10, verbose=True)
    result = await w.run(first_input="Start the workflow.")
    print(result)
    draw_all_possible_flows(TheWorkflow, filename="loops_workflow.html")

if __name__ == "__main__":
    asyncio.run(main())