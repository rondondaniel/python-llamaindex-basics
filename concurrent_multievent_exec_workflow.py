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

class StepAEvent(Event):
    query: str

class StepBEvent(Event):
    query: str

class StepCEvent(Event):
    query: str

class StepACompleteEvent(Event):
    pass

class StepBCompleteEvent(Event):
    pass

class StepCCompleteEvent(Event):
    pass


class ConcurrentFlow(Workflow):
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> StepAEvent | StepBEvent | StepCEvent:
        ctx.send_event(StepAEvent(query="Query 1"))
        ctx.send_event(StepBEvent(query="Query 2"))
        ctx.send_event(StepCEvent(query="Query 3"))

    @step
    async def step_a(self, ctx: Context, ev: StepAEvent) -> StepACompleteEvent:
        print("Doing something A-ish")

        return StepACompleteEvent(result=ev.query)
    
    @step
    async def step_b(self, ctx: Context, ev: StepBEvent) -> StepBCompleteEvent:
        print("Doing something B-ish")

        return StepBCompleteEvent(result=ev.query)
    
    @step
    async def step_c(self, ctx: Context, ev: StepCEvent) -> StepCCompleteEvent:
        print("Doing something C-ish")

        return StepCCompleteEvent(result=ev.query)
    
    @step
    async def step_three(
        self, 
        ctx: Context,
          ev: StepACompleteEvent | StepBCompleteEvent | StepCCompleteEvent
    ) -> StopEvent:
        # wait unitl we receive the result from 3 events

        results = ctx.collect_events(ev, [StepACompleteEvent, StepBCompleteEvent, StepCCompleteEvent])

        if results is None:
            return None
        
        print("Results from 3 events: ", results[0].result, results[1].result, results[2].result)

        return StopEvent(result="Done")
    
async def main():
    w = ConcurrentFlow(timeout=10, verbose=True)
    result = await w.run(first_input="Start the workflow.")
    print(result)
    draw_all_possible_flows(ConcurrentFlow, filename="concurrent_multievent_workflow.html")

if __name__ == "__main__":
    asyncio.run(main())