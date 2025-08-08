"""List and create universe forks."""
import streamlit as st

from services.federation_adapter import list_forks, create_fork


def render() -> None:
    st.markdown("## Forks")
    forks = list_forks()
    if not forks.get("available", True):
        st.info("Using stub federation adapter")
    st.table(forks.get("forks", []))

    st.subheader("Create Fork")
    creator = st.session_state.get("username", "anon")
    cfg_text = st.text_input(
        "Config (key=value, comma separated)", key="fork_cfg_v2"
    )
    if st.button("Create Fork", key="fork_create_btn_v2"):
        cfg: dict[str, str] = {}
        for pair in cfg_text.split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                cfg[k.strip()] = v.strip()
        res = create_fork(creator, cfg)
        if res.get("ok"):
            st.success(f"Created fork {res.get('fork_id')}")
        else:
            st.error("Fork creation failed")


def main() -> None:
    render()


if __name__ == "__main__":
    main()
