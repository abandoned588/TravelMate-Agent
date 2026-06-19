from __future__ import annotations

from pydantic import BaseModel, Field


class WeatherForecastInput(BaseModel):
    city: str = Field(..., description="目的地城市名称，例如杭州、成都、上海")
    days: int = Field(..., ge=1, le=7, description="查询未来几天的天气，最多 7 天")


class AttractionSearchInput(BaseModel):
    city: str = Field(..., description="目的地城市，例如杭州、成都、北京")
    interests: list[str] = Field(..., description="用户兴趣，例如美食、拍照、历史、自然风景、亲子、购物")
    limit: int = Field(10, ge=1, le=20, description="最多返回的 POI 数量")


class BudgetInput(BaseModel):
    days: int = Field(..., ge=1, le=14, description="旅行天数")
    user_budget: float = Field(..., ge=0, description="用户总预算")
    transport_cost: float = Field(0, ge=0, description="往返交通费用估算")
    hotel_per_night: float = Field(250, ge=0, description="每晚住宿费用估算")
    food_per_day: float = Field(120, ge=0, description="每日餐饮费用估算")
    ticket_cost: float = Field(200, ge=0, description="门票和活动费用估算")


class SaveItineraryInput(BaseModel):
    title: str = Field(..., description="行程标题")
    content: str = Field(..., description="完整行程 Markdown 内容")




class LocalKnowledgeSearchInput(BaseModel):
    city: str = Field(..., description="Target city for local CSV knowledge lookup.")
    categories: list[str] = Field(default_factory=list, description="Categories to search, such as attraction or food.")
    query: str = Field("", description="Optional keyword filter for local knowledge rows.")
    limit: int = Field(8, ge=1, le=20, description="Maximum number of local records to return.")
