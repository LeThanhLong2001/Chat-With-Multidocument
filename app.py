import streamlit as st
import os
import tempfile
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_parse import LlamaParse
from dotenv import load_dotenv

import os
load_dotenv()

groq_api_key=os.getenv('GROQ_API_KEY')
# Khởi tạo Groq LLM
llm = Groq(
    api_key= groq_api_key,
    model="llama-3.1-70b-versatile"
)
Settings.llm = llm

# Embedding model
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Splitter
text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=30)
Settings.text_splitter = text_splitter

# Hàm xử lí dữ liệu tải lên
def process_files(uploaded_files):
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in uploaded_files:
            file_path = os.path.join(temp_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

        # set up parser
        parser = LlamaParse(
            result_type="text"  
        )

        file_extractor = {".pdf": parser, '.doc': parser, '.pptx': parser}
        documents = SimpleDirectoryReader(input_dir = temp_dir, file_extractor=file_extractor).load_data()
        index = VectorStoreIndex.from_documents(documents, transformations=[text_splitter])
        return index

# Hàm lấy phản hồi từ LLM
def get_response_from_llm(prompt):
    
    system_prompt = """You are a helpful AI assistant. For general knowledge questions, 
    provide accurate and informative answers. Keep responses concise and relevant."""

    response = llm.complete(
        prompt=f"System: {system_prompt}\nHuman: {prompt}\nAssistant:"
    )
    return response.text

def main():
    # Title
    st.title("RAG Chatbot với Llama 3.1 (Groq)")

    uploaded_files = st.file_uploader(
        "Upload tài liệu của bạn",
        accept_multiple_files=True,
        type=['pdf', 'pptx', 'docx']
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tải file lên
    if uploaded_files:
        if 'index' not in st.session_state:
            with st.spinner('Đang xử lý tài liệu...'):
                index = process_files(uploaded_files)
                st.session_state.index = index
            st.success('Đã xử lý xong tài liệu!')

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Hỏi về tài liệu của bạn hoặc câu hỏi bất kì"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner('Đang suy nghĩ...'):
                    if hasattr(st.session_state, 'index'):
                        # configure retriever
                        retriever = VectorIndexRetriever(
                            index=st.session_state.index,
                            similarity_top_k=1,
                        )
                        # configure response synthesizer
                        response_synthesizer = get_response_synthesizer()
                        # assemble query engine
                        query_engine = RetrieverQueryEngine(
                            retriever=retriever,
                            response_synthesizer=response_synthesizer,
                            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.6)],
                        )
                        doc_response = query_engine.query(prompt)
                        response_text = f"Dựa trên tài liệu của bạn:\n{doc_response}"
                        similarity_score = doc_response.source_nodes[0].score if doc_response.source_nodes else 0

                        # Nếu câu hỏi liên quan đến tài liệu thì sử dụng RAG, không thì sử dụng LLM
                        if similarity_score >= 0.6:
                          response_text = f"Dựa trên tài liệu của bạn:\n{doc_response}"
                        else:
                          llm_response = get_response_from_llm(prompt)
                          response_text = f"Dựa trên kiến thức của tôi:\n{llm_response}"

                    # Hiển thị phản hồi
                    st.markdown(response_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )
    else:
        # Trường hợp người dùng không tải lên tài liệu và chat trực tiếp
        st.info("Vui lòng tải lên tài liệu hoặc hỏi câu hỏi.")

        # Vẫn cho phép hỏi câu hỏi chung khi chưa có tài liệu
        if prompt := st.chat_input("Hỏi câu hỏi chung"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner('Đang suy nghĩ...'):
                    response = get_response_from_llm(prompt)
                    response_text = f"Dựa trên kiến thức của tôi:\n{response}"
                    st.markdown(response_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )


if __name__ == "__main__":
    main()