from pydantic import BaseModel, ConfigDict


class GatewayOverride(BaseModel):
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    name: str
