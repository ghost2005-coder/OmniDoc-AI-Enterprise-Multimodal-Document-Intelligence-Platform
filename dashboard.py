import streamlit as st
import requests
API = st.sidebar.text_input("API URL", "http://127.0.0.1:8000")
st.title("OmniDoc AI — Document Intelligence")
st.caption("Educational MVP. The baseline QA returns retrieved passages rather than an LLM-generated answer.")
tab1, tab2 = st.tabs(["Index text", "Ask a question"])
with tab1:
    doc_id = st.text_input("Document ID", "demo-report")
    filename = st.text_input("Filename", "demo.txt")
    text = st.text_area("Paste document text", height=240)
    if st.button("Index document") and text.strip():
        r = requests.post(f"{API}/documents/text", json={"document_id":doc_id,"filename":filename,"text":text}, timeout=30)
        st.write(r.status_code, r.json())
with tab2:
    question = st.text_input("Question")
    doc_filter = st.text_input("Optional document ID filter")
    if st.button("Search") and question.strip():
        payload = {"question":question,"top_k":4}
        if doc_filter.strip(): payload["document_id"] = doc_filter.strip()
        r = requests.post(f"{API}/qa", json=payload, timeout=30)
        st.json(r.json())
