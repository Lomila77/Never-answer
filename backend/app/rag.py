import os
import json
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from tqdm import tqdm
from backend.app.utils import get_all_json_content


class RAG:

    def __init__(self, data_directory: str):
        self.data_directory = data_directory
        self.embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        if not os.path.exists("./db/faiss_index"):
            self.save_jsons_files_in_vector_db()
        else:
            self.db = FAISS.load_local("./db/faiss_index", self.embedding)

    def save_jsons_files_in_vector_db(self):
        """
        Traite tous les fichiers JSON d'un dossier et les ajoute à la base vectorielle
        Crée la db si elle n'existe pas
        """
        jsons_list = get_all_json_content(self.data_directory)
        documents = []
        
        for json_content in tqdm(jsons_list):
            documents.append(Document(page_content=json_content["text"]))
        
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(documents)

        if os.path.exists("./db/faiss_index"):
            db = FAISS.load_local("./db/faiss_index", self.embedding)
            db.add_documents(docs)
        else:
            db = FAISS.from_documents(docs, self.embedding)
        db.save_local("./db/faiss_index")
        print(f"Base vectorielle mise à jour avec {len(docs)} chunks de documents")

    def similarity_search(self, query: str):
        docs = self.db.similarity_search(query, k=3)
        context = "\n\n".join([d.page_content for d in docs])
        return context
