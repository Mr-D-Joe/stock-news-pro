from typing import TypeVar, Generic, List, Optional, Callable
from pydantic import BaseModel

class PipelineConfig(BaseModel):
    stocks: List[str] = []
    sectors: List[str] = []
    language: str = "English"

class PipelineContext(BaseModel):
    config: PipelineConfig
    on_wait_start: Optional[Callable[[int, bool], None]] = None
    on_wait_tick: Optional[Callable[[int], None]] = None
    
    model_config = {"arbitrary_types_allowed": True}

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")

class PipelineStep(Generic[InputT, OutputT]):
    name: str = "step"

    def process(self, input_data: InputT, context: PipelineContext) -> OutputT:
        raise NotImplementedError
