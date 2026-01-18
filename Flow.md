Nice 😄 — you’ve got everything wired correctly.
Now let’s **exercise the system end-to-end** the same way an interviewer (or you) would.

Below are **three ways** to try it, from fastest to most “backend-engineer legit”.

---

## 1️⃣ Fastest: Swagger UI (recommended first)

FastAPI gives you Swagger **for free**.

### Open

```
http://localhost:8000/docs
```

You should see:

* `auth`
* `accounts`
* `transfers`

---

### Step-by-step flow

#### 1. Register

**POST /auth/register**

```json
{
  "email": "user@example.com",
  "password": "supersecret123"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

#### 2. Authorize

* Click **Authorize** (top right)
* Paste:

```
Bearer <your_token_here>
```

✔ Now all protected endpoints work

---

#### 3. Create accounts

**POST /accounts**

```json
{
  "name": "Main account",
  "initial_balance_cents": 10000
}
```

Create a second account:

```json
{
  "name": "Savings",
  "initial_balance_cents": 0
}
```

---

#### 4. List accounts

**GET /accounts**

You should see balances.

---

#### 5. Transfer money (transaction!)

**POST /transfers**

```json
{
  "from_account_id": 1,
  "to_account_id": 2,
  "amount_cents": 2500
}
```

✔ Atomic
✔ Row-locked
✔ Transaction-safe

---

#### 6. Verify balances

**GET /accounts**

Balances should now reflect the transfer.

---

## 2️⃣ cURL (interview-friendly)

### Register

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"supersecret123"}'
```

Save the token:

```bash
TOKEN=eyJhbGciOi...
```

---

### Create account

```bash
curl -X POST http://localhost:8000/accounts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Main","initial_balance_cents":10000}'
```

---

### Transfer

```bash
curl -X POST http://localhost:8000/transfers \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"from_account_id":1,"to_account_id":2,"amount_cents":5000}'
```

---

## 3️⃣ Pro mode: validate transactions + rollback

### Try insufficient funds

```json
{
  "from_account_id": 1,
  "to_account_id": 2,
  "amount_cents": 999999
}
```

Expected:

* HTTP 400
* Balances unchanged

That proves:

* Transaction boundaries
* Rollback behavior
* Business rules in service layer

---

## 4️⃣ Verify DB directly (optional but reassuring)

```bash
docker compose exec db psql -U postgres -d appdb
```

```sql
select * from accounts;
select * from transfers;
```

---

## 5️⃣ What to say in the interview

If they ask **“How did you test it?”**:

> “I validated the full auth flow via Swagger, then verified transactional integrity by forcing failure cases and checking balances stayed consistent. I also verified persistence directly in Postgres.”

If they ask **“How would you deploy this?”**:

> “Right now it runs in Docker Compose; in production I’d build a slim image, run Alembic migrations as a job, and deploy behind a reverse proxy.”

---

## 6️⃣ If you want one last polish before interview

Optional but impressive:

* Add `GET /transfers` (history)
* Add request IDs / logging
* Add a README with:

  * architecture diagram
  * transaction explanation
  * how to run locally

---

If you want, next I can:

* 🔥 Convert this to **async SQLAlchemy**
* 🎯 Write **2–3 killer tests**
* 🧠 Give you **exact interview Q&A** based on this project

Just tell me.
