import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from documentation_loader import load_kubernetes_docs
from langchain_text_splitters import RecursiveCharacterTextSplitter

GENERATE_EMBEDINGS = os.getenv("GENERATE_EMBEDINGS")
QUERY = os.getenv("QUERY")

class VectorStoreManager():
    def __init__(self):
        self.vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
            persist_directory="/tmp/testcontainer/chroma_langchain_db",  # Where to save data locally
        )
        self.plain_docs = []

    def load_docs(self):
        directory_path = "/tmp/website/content/en"  # Change this to the path where your files are stored. we could index other languages.
        self.plain_docs = load_kubernetes_docs(directory_path)

    def embed_docs(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2048,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        splited_documents = []
        print("LEN OF PLAIN DOCS")
        print(len(self.plain_docs))
        #indexing all of the documents from kubernetes in english with chunk size 2048 should take less than 4 mins using a mackbook pro m3
        for i, doc in enumerate(self.plain_docs):
            print(f'embeding doc #{i}')
            splited_docs = text_splitter.create_documents([doc], [{"source": "documentation"}])
            splited_documents += splited_docs

        uuids = [str(uuid4()) for _ in range(len(splited_documents))]
        print("number of docs after spliting ######")
        print(len(splited_documents))#this is not representative of the documents in the store, is only true of loaded instances at this point
        self.vector_store.add_documents(documents=splited_documents, ids=uuids)

    def query_docs(self, query):
        results = self.vector_store.similarity_search(
            query,
            k=2,
            filter={"source": "documentation"},
        )  
        print("\n\n\nRESULT FROM QUERY\n\n")  
        print(query)

        for res in results:
            print(f"* {res.page_content} [{res.metadata}]")

    def query_docs_with_score(self, query):
        results = self.vector_store.similarity_search_with_score(
            query, k=1, filter={"source": "documentation"}
        )
        print("\n\n\nSYMILARITY SEARCH RESULT WITH SCORE RESULLT ######\n\n")
        print(query)

        for res, score in results:
            print(f"* [SIM={score:3f}] {res.page_content} [{res.metadata}]")


vsm = VectorStoreManager()
# 1. load documents and create embedings 
if GENERATE_EMBEDINGS == "True":
    vsm.load_docs()
    vsm.embed_docs()
    print("\n\nGENERATED NEW EMBEDINGS <<<<<<<<<<<<")
else: 
    print("\n\nUSING EXISTING EMBEDINGS <<<<<<<<<<<<")

# 2. Retrieve relevant context from VDB embedings
if QUERY != None:
    vsm.query_docs(QUERY)
else:
    vsm.query_docs("what is a proxy?")
