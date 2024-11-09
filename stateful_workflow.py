import asyncio
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context,
)
from llama_index.utils.workflow import draw_all_possible_flows

class SetupEvent(Event):
    query: str

class StepTwoEvent(Event):
    query: str

class StatefulFlow(Workflow):
    @step
    async def start(
        self, ctx: Context, event: StartEvent
    ) -> SetupEvent | StepTwoEvent:
        db = await ctx.get("some_database", default=None)
        if db is None:
            print("database is setting up.")
            return SetupEvent(query=event.query
                              )
        # do something
        return StepTwoEvent(query=event.query)
    
    @step
    async def setup(self, ctx: Context, event: SetupEvent) -> StartEvent:
        # load data
        await ctx.set("some_database", [1,2,3])

        return StepTwoEvent(query=event.query)
    
    @step
    async def step_two(self, ctx: Context, event: StepTwoEvent) -> StopEvent:
        data = await ctx.get("some_database")
        print("Data is ", data)

        return StopEvent(result=".".join([event.query, str(data[1])]))
    
async def main():
    w = StatefulFlow(timeout=10, verbose=False)
    result = await w.run(query="Some query")
    print(result)
    draw_all_possible_flows(w, filename="stateful_workflow.html")

if __name__ == "__main__":
    asyncio.run(main())