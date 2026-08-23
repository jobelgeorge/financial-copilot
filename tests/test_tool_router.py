from src.tools.tool_router import ToolRouter


def test_revenue_question_routes_correctly():

    router = ToolRouter()

    result = router.route_question(
        "How has Apple's revenue grown?"
    )

    assert result is not None

    assert result["tool"] == "get_revenue_growth"