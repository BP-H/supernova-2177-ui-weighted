"""RootCoin balance and ledger page."""
import streamlit as st

from services.coin_adapter import get_balance, tip, ledger


def render() -> None:
    st.markdown("## RootCoin")
    user = st.session_state.get("username", "anon")
    info = get_balance(user)
    if not info.get("available", True):
        st.info("Using in-memory coin stub")
    st.metric("Balance", f"{info.get('balance', 0):.2f}")

    st.subheader("Send Tip")
    to_user = st.text_input("To", key="coin_tip_to_v2")
    amount = st.number_input("Amount", min_value=0.0, key="coin_tip_amount_v2")
    memo = st.text_input("Memo", key="coin_tip_memo_v2")
    if st.button("Send", key="coin_tip_send_v2") and to_user:
        res = tip(user, to_user, amount, memo or None)
        if res.get("ok"):
            st.success("Tip sent")
            info = get_balance(user)
            st.metric("Balance", f"{info.get('balance', 0):.2f}")
        else:
            st.error("Tip failed")

    st.subheader("Ledger")
    led = ledger()
    st.table(led.get("entries", []))


def main() -> None:  # for direct run
    render()


if __name__ == "__main__":
    main()
