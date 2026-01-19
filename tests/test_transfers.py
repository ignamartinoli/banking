from tests.conftest import API_PREFIX, register_and_get_token, auth_headers


def get_currency_map(client):
    r = client.get(f"{API_PREFIX}/currencies")
    assert r.status_code == 200, r.text
    return {c["code"]: c["id"] for c in r.json()}


def create_account(client, token, name, balance, currency_id=None):
    payload = {"name": name, "initial_balance_cents": balance}
    if currency_id is not None:
        payload["currency_id"] = currency_id

    r = client.post(f"{API_PREFIX}/accounts", json=payload, headers=auth_headers(token))
    assert r.status_code == 200, r.text
    return r.json()


def test_transfer_between_different_currencies_is_rejected(client):
    token = register_and_get_token(client, "a@a.com", "Password123_")

    cur = get_currency_map(client)
    ars_id = cur["ARS"]
    usd_id = cur["USD"]

    acc_ars = create_account(client, token, "ARS-acc", 10000, currency_id=ars_id)
    acc_usd = create_account(client, token, "USD-acc", 0, currency_id=usd_id)

    r = client.post(
        f"{API_PREFIX}/transfers",
        json={
            "from_account_id": acc_ars["id"],
            "to_account_id": acc_usd["id"],
            "amount_cents": 100,
        },
        headers=auth_headers(token),
    )

    assert r.status_code == 400, r.text
    assert "different currencies" in r.json()["detail"].lower()


def test_transfer_negative_amount_is_422(client):
    token = register_and_get_token(client, "b@b.com", "Password123_")

    cur = get_currency_map(client)
    ars_id = cur["ARS"]

    acc1 = create_account(client, token, "A1", 10000, currency_id=ars_id)
    acc2 = create_account(client, token, "A2", 0, currency_id=ars_id)

    # Pydantic schema has Field(gt=0), so FastAPI returns 422 before hitting service
    r = client.post(
        f"{API_PREFIX}/transfers",
        json={
            "from_account_id": acc1["id"],
            "to_account_id": acc2["id"],
            "amount_cents": -100,
        },
        headers=auth_headers(token),
    )

    assert r.status_code == 422, r.text


def test_transfer_insufficient_funds_is_400(client):
    token = register_and_get_token(client, "c@c.com", "Password123_")

    cur = get_currency_map(client)
    ars_id = cur["ARS"]

    acc1 = create_account(client, token, "From", 50, currency_id=ars_id)
    acc2 = create_account(client, token, "To", 0, currency_id=ars_id)

    r = client.post(
        f"{API_PREFIX}/transfers",
        json={
            "from_account_id": acc1["id"],
            "to_account_id": acc2["id"],
            "amount_cents": 100,
        },
        headers=auth_headers(token),
    )

    assert r.status_code == 400, r.text
    assert "insufficient" in r.json()["detail"].lower()


def test_transfer_success_updates_balances(client):
    token = register_and_get_token(client, "d@d.com", "Password123_")

    cur = get_currency_map(client)
    ars_id = cur["ARS"]

    acc1 = create_account(client, token, "From", 1000, currency_id=ars_id)
    acc2 = create_account(client, token, "To", 0, currency_id=ars_id)

    r = client.post(
        f"{API_PREFIX}/transfers",
        json={
            "from_account_id": acc1["id"],
            "to_account_id": acc2["id"],
            "amount_cents": 200,
        },
        headers=auth_headers(token),
    )
    assert r.status_code == 200, r.text

    # Verify balances via GET /accounts
    r = client.get(f"{API_PREFIX}/accounts", headers=auth_headers(token))
    assert r.status_code == 200, r.text
    accounts = {a["id"]: a for a in r.json()}

    assert accounts[acc1["id"]]["balance_cents"] == 800
    assert accounts[acc2["id"]]["balance_cents"] == 200

