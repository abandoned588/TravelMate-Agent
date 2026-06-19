from __future__ import annotations

from config.constants import (
    DEFAULT_FOOD_PER_DAY,
    DEFAULT_HOTEL_PER_NIGHT,
    DEFAULT_TICKET_COST,
    DEFAULT_TRANSPORT_COST,
)


def calculate_budget(
    days: int,
    user_budget: float,
    transport_cost: float = DEFAULT_TRANSPORT_COST,
    hotel_per_night: float = DEFAULT_HOTEL_PER_NIGHT,
    food_per_day: float = DEFAULT_FOOD_PER_DAY,
    ticket_cost: float = DEFAULT_TICKET_COST,
) -> dict:
    """Estimate total travel cost and compare it against the user's budget."""
    hotel_total = hotel_per_night * max(days - 1, 0)
    food_total = food_per_day * days
    total_cost = transport_cost + hotel_total + food_total + ticket_cost
    remaining_budget = user_budget - total_cost
    is_over_budget = total_cost > user_budget

    if is_over_budget:
        advice = "预算偏紧，建议减少天数、选择经济型住宿、增加免费景点并压缩餐饮预算。"
    elif remaining_budget <= max(user_budget * 0.1, 100):
        advice = "预算基本够用，建议预留一些机动资金应对临时交通、排队打车或额外餐饮。"
    else:
        advice = "预算相对充足，可以适当提升住宿舒适度或增加一项特色体验。"

    result_data = {
        "transport_cost": transport_cost,
        "hotel_total": hotel_total,
        "food_total": food_total,
        "ticket_cost": ticket_cost,
        "total_cost": total_cost,
        "user_budget": user_budget,
        "remaining_budget": remaining_budget,
        "is_over_budget": is_over_budget,
        "advice": advice,
    }
    return {
        "success": True,
        "data": result_data,
        "summary": f"预算估算完成，总费用约 {total_cost:.0f} 元，剩余预算约 {remaining_budget:.0f} 元。",
    }

