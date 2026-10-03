import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Financial Copilot",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Financial Copilot")
st.caption("Ask about any publicly listed US company. The financial data is fetched live from SEC EDGAR.")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("metadata"):
            meta = message["metadata"]
            score = meta.get("judge_score", 0)
            score_label = (
                f"{score}/5" if score >= 4
                else f"{score}/5" if score == 3
                else f"{score}/5"
            )
            cols = st.columns(3)
            cols[0].caption(f"**Company:** {meta['company']}")
            cols[1].caption(f"**Tool:** `{meta['tool']}`")
            cols[2].caption(f"**Accuracy:** {score_label}")
            if meta.get("judge_reasoning"):
                st.caption(f"_{meta['judge_reasoning']}_")


if prompt := st.chat_input("e.g. What is Apple's revenue trend?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": prompt},
                    timeout=60
                )
                if not response.ok:
                    raise requests.exceptions.HTTPError(response=response)
                data = response.json()

                answer = data["answer"]
                metadata = {
                    "company": data["company"],
                    "tool": data["tool"],
                    "judge_score": data.get("judge_score", 0),
                    "judge_reasoning": data.get("judge_reasoning", ""),
                }

                st.markdown(answer)
                score = data.get("judge_score", 0)
                score_label = (
                    f"{score}/5" if score >= 4
                    else f"{score}/5" if score == 3
                    else f"{score}/5"
                )
                cols = st.columns(3)
                cols[0].caption(f"**Company:** {metadata['company']}")
                cols[1].caption(f"**Tool:** `{metadata['tool']}`")
                cols[2].caption(f"**Accuracy:** {score_label}")
                if metadata.get("judge_reasoning"):
                    st.caption(f"_{metadata['judge_reasoning']}_")


            except requests.exceptions.ConnectionError:
                answer = "Could not connect to the API. Make sure the FastAPI server is running on port 8000."
                metadata = None
                st.error(answer)

            except requests.exceptions.HTTPError as e:
                try:
                    detail = e.response.json().get("detail", str(e))
                except Exception:
                    detail = str(e)
                answer = f"{detail}"
                metadata = None
                st.error(answer)

            except Exception as e:
                answer = f"Error: {str(e)}"
                metadata = None
                st.error(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "metadata": metadata
    })
