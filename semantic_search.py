import os, config, openai
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage


openai.api_key = os.environ["OPENAI_API_KEY"] = config.openaiApiKey
openai.organization = config.openaiApiOrganization

# Build and store index locally in directory "storage"
#documents = SimpleDirectoryReader("commentary_59_James_English", recursive=True, required_exts=[".md"]).load_data()
#index = GPTVectorStoreIndex.from_documents(documents)
#index.storage_context.persist(persist_dir="storage")

# rebuild storage context from local directory "storage"
storage_context = StorageContext.from_defaults(persist_dir="storage")
# load index
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

response = query_engine.query("What are the main themes of chapter 1?")
print(response)

"""
Output:

The main themes of James 1 are faith, wisdom, and perseverance. In this chapter, James encourages believers to have faith in God and to trust in His wisdom. He also emphasizes the importance of persevering in the face of trials and temptations. He encourages us to be patient and to remain steadfast in our faith, knowing that God will reward those who remain faithful.
"""

response = query_engine.query("Who wrote the letter?  Why did he write it?")
print(response)

"""
Output:

It is unclear who wrote the letter, as some scholars believe it was written by James, the brother of Jesus, while others believe it was written by a different James who was also a leader in the early Christian church. 

The letter was likely written to encourage and instruct fellow believers in the Christian faith. The author identifies himself as a servant of God and Jesus, emphasizing his submission to them and his desire to serve them. He also uses the greeting to affirm his belief in the divinity of Jesus.
"""
