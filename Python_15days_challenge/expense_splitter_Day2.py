import io
from typing import List, Dict, Tuple
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Expense Splitter", page_icon="🧮", layout="centered")

# -------------------------------
# Helpers
# -------------------------------
def normalize_name(i: int, name: str) -> str:
    n = (name or "").strip()
    return n if n else f"Person {i+1}"

def minimal_settlements(balances: Dict[str, float], decimals: int = 2) -> List[Tuple[str, str, float]]:
    """
    Given per-person balances (positive = should receive, negative = owes),
    return a minimal set of transfers (payer -> receiver -> amount).
    Greedy creditor/debtor matching.
    """
    # Round small floating noise
    bal = {k: round(v, decimals) for k, v in balances.items()}
    debtors = [(p, -amt) for p, amt in bal.items() if amt < 0]   # owes (positive magnitude)
    creditors = [(p, amt) for p, amt in bal.items() if amt > 0]  # to receive

    debtors.sort(key=lambda x: x[1], reverse=True)   # largest debtor first
    creditors.sort(key=lambda x: x[1], reverse=True) # largest creditor first

    i = j = 0
    transfers: List[Tuple[str, str, float]] = []
    while i < len(debtors) and j < len(creditors):
        d_name, d_amt = debtors[i]
        c_name, c_amt = creditors[j]
        pay = min(d_amt, c_amt)
        pay_r = round(pay, decimals)

        if pay_r > 0:
            transfers.append((d_name, c_name, pay_r))

        d_amt = round(d_amt - pay, decimals)
        c_amt = round(c_amt - pay, decimals)

        if d_amt == 0:
            i += 1
        else:
            debtors[i] = (d_name, d_amt)

        if c_amt == 0:
            j += 1
        else:
            creditors[j] = (c_name, c_amt)

    return transfers

def to_currency(x: float, symbol: str, decimals: int) -> str:
    return f"{symbol}{x:,.{decimals}f}"

# -------------------------------
# Sidebar: settings
# -------------------------------
st.sidebar.header("⚙️ Settings")
currency = st.sidebar.text_input("Currency symbol", value="₹", help="Examples: ₹, $, €, £")
decimals = st.sidebar.number_input("Rounding decimals", min_value=0, max_value=4, value=2, step=1)
st.sidebar.caption("Note: All outputs are rounded to this precision.")

# Upload (optional)
uploaded = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"], help="Columns: name, paid")
st.sidebar.divider()

# -------------------------------
# Header
# -------------------------------
st.title("🧮 Expense Splitter (Splitwise-style)")

colA, colB = st.columns(2)
with colA:
    total_amount = st.number_input("Total amount (bill/overall spend)", min_value=0.0, value=0.0, step=100.0, format="%.2f")
with colB:
    n_people = st.number_input("Number of people", min_value=1, value=3, step=1)

st.caption("Tip: You can either enter the *total* and split equally, **or** enter per-person contributions (the app will reconcile both).")

# -------------------------------
# Editable table: names & contributions
# -------------------------------
if uploaded is not None:
    try:
        df_init = pd.read_csv(uploaded)
        # normalize columns
        df_init.columns = [c.strip().lower() for c in df_init.columns]
        if "name" not in df_init.columns or "paid" not in df_init.columns:
            st.error("CSV must contain 'name' and 'paid' columns.")
            st.stop()
        # Coerce
        df_init = df_init[["name", "paid"]].copy()
        df_init["name"] = df_init["name"].astype(str)
        df_init["paid"] = pd.to_numeric(df_init["paid"], errors="coerce").fillna(0.0)
        # If uploaded has different count than n_people, pad/trim
        if len(df_init) < n_people:
            for i in range(n_people - len(df_init)):
                df_init.loc[len(df_init)] = ["", 0.0]
        elif len(df_init) > n_people:
            df_init = df_init.head(n_people)
    except Exception as e:
        st.error(f"Failed to parse CSV: {e}")
        st.stop()
else:
    df_init = pd.DataFrame({
        "name": [f"Person {i+1}" for i in range(n_people)],
        "paid": [0.0] * n_people
    })

# Allow dynamic row count to match n_people
if len(df_init) != n_people:
    if len(df_init) < n_people:
        for _ in range(n_people - len(df_init)):
            df_init.loc[len(df_init)] = ["", 0.0]
    else:
        df_init = df_init.head(n_people)

st.subheader("Participants & Contributions")
edited = st.data_editor(
    df_init,
    column_config={
        "name": st.column_config.TextColumn("Name", help="Optional; leave blank for Person i"),
        "paid": st.column_config.NumberColumn("Paid", help="Amount contributed/paid", format="%.2f", step=0.5),
    },
    hide_index=True,
    num_rows="fixed",
    key="editor",
)

compute = st.button("Compute Split", type="primary", width="stretch")

# -------------------------------
# Compute results
# -------------------------------
if compute:
    # Prepare participants
    participants = []
    for i, row in edited.iterrows():
        nm = normalize_name(i, str(row.get("name", "")))
        paid = float(row.get("paid", 0.0) or 0.0)
        participants.append({"name": nm, "paid": paid})

    df = pd.DataFrame(participants)
    paid_total = round(float(df["paid"].sum()), decimals)

    # Determine pot/total to split:
    # - If user entered TOTAL > 0: we use that as ground truth.
    # - Else: we use the sum of "paid".
    pot = round(total_amount if total_amount > 0 else paid_total, decimals)

    # Equal share target
    share = round(pot / len(df), decimals) if len(df) else 0.0

    # Compute balances (positive => should receive, negative => owes)
    df["share"] = share
    df["balance"] = (df["paid"] - df["share"]).round(decimals)

    # Info & warnings
    info_cols = st.columns(3)
    info_cols[0].metric("People", len(df))
    info_cols[1].metric("Total to split", to_currency(pot, currency, decimals))
    info_cols[2].metric("Equal share", to_currency(share, currency, decimals))

    if total_amount > 0 and abs(paid_total - total_amount) > (10 ** -decimals):
        st.warning(
            f"Note: Sum of contributions ({to_currency(paid_total, currency, decimals)}) "
            f"differs from entered total ({to_currency(total_amount, currency, decimals)}). "
            "Using the entered total for the split."
        )

    st.subheader("Balances")
    show_df = df[["name", "paid", "share", "balance"]].copy()
    show_df.columns = ["Name", "Paid", "Fair Share", "Balance (receive + / owe −)"]
    st.dataframe(show_df, width="stretch", hide_index=True)

    # Build settlements
    balances_dict = {r["name"]: float(r["balance"]) for _, r in df.iterrows()}
    settlements = minimal_settlements(balances_dict, decimals=decimals)

    st.subheader("Suggested Settlements")
    if not settlements:
        st.success("All settled! No transfers needed 🎉")
    else:
        rows = [{"Payer": a, "Receiver": b, "Amount": to_currency(amt, currency, decimals)}
                for a, b, amt in settlements]
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

    # Download results (CSV)
    out = df.copy()
    out["Amount to Receive (+) / Pay (−)"] = out["balance"]
    out = out[["name", "paid", "share", "Amount to Receive (+) / Pay (−)"]]
    out.columns = ["Name", "Paid", "Fair Share", "Balance"]
    buf = io.StringIO()
    out.to_csv(buf, index=False)
    st.download_button(
        "⬇️ Download Balances (CSV)",
        data=buf.getvalue().encode("utf-8"),
        file_name="balances.csv",
        mime="text/csv",
        width="stretch",
    )

# -------------------------------
# Footer
# -------------------------------
with st.expander("How it works"):
    st.markdown(
        """
- Enter **total amount** and **number of people**.
- Optionally enter **names** and **how much each person paid**.
- App computes an **equal fair share** and each person's **balance**:
  - **Positive** balance → should **receive** money.
  - **Negative** balance → **owes** money.
- We also compute a **compact set of settlements** using a greedy creditor/debtor match.
- You can **upload a CSV** with `name,paid` columns or download the results.
        """
    )
