from src.ingestion.sec_client import SECClient


def test_apple_company_facts():
    client = SECClient()

    data = client.get_company_facts("0000320193")

    assert data is not None
    assert "entityName" in data
    assert "facts" in data

    print("\nCompany:", data["entityName"])
    print("Fact categories:", list(data["facts"].keys()))