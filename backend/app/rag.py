import os
import logging
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from tqdm import tqdm
from backend.app.utils import get_all_json_content

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RAG:

    def __init__(self, data_directory: str):
        self.data_directory = data_directory
        self.embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        if not os.path.exists("./db/wikipedia"):
            self.save_jsons_files_in_vector_db()
        else:
            self.db = FAISS.load_local("./db/wikipedia", self.embedding, allow_dangerous_deserialization=True)

    def save_jsons_files_in_vector_db(self):
        """
        Traite tous les fichiers JSON d'un dossier et les ajoute à la base vectorielle
        Crée la db si elle n'existe pas
        """
        jsons_list = get_all_json_content(self.data_directory)
        documents = []
        
        for json_content in tqdm(jsons_list):
            if isinstance(json_content, dict) and "text" in json_content:
                documents.append(Document(page_content=json_content["text"]))
            elif isinstance(json_content, list):
                for item in json_content:
                    if isinstance(item, dict) and "text" in item:
                        documents.append(Document(page_content=item["text"]))
        logger.info("Parse document")
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        logger.info("Cut document into chunks")
        docs = splitter.split_documents(documents)
        logger.info("Split document")
        if os.path.exists("./db/wikipedia"):
            logger.info("Save Document in the VectorDB")
            db = FAISS.load_local("./db/wikipedia", self.embedding)
            db.add_documents(docs)
        else:
            logger.info("Save document in new VectorDB")
            db = FAISS.from_documents(docs, self.embedding)
        db.save_local("./db/wikipedia")
        print(f"Base vectorielle mise à jour avec {len(docs)} chunks de documents")

    def similarity_search(self, query: str):
        docs = self.db.similarity_search(query, k=3)
        context = "\n\n".join([d.page_content for d in docs])
        return context
