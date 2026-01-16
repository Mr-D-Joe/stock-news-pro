from typing import TypeVar, Generic, List, Optional, Callable, Any
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

I = TypeVar("I")
O = TypeVar("O")

class PipelineStep(Generic[I, O]):
    name: str = "step"

    def process(self, input_data: I, context: PipelineContext) -> O:
        raise NotImplementedError
