import os
from pypdf import PdfReader

class LocalRAG:

    def __init__(self):
        self.documents = []

    def load_file(self, filepath):

        if filepath.endswith(".pdf"):

            reader = PdfReader(filepath)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            return text

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    def ingest_documents(self, data_folder="data"):

        self.documents = []

        print(f"Loading documents from: {data_folder}")

        for filename in os.listdir(data_folder):

            filepath = os.path.join(
                data_folder,
                filename
            )

            text = self.load_file(filepath)

            self.documents.append(
                {
                    "source": filename,
                    "text": text
                }
            )

        print("Documents Loaded:")
        print(self.documents)

    def retrieve(self, query, top_k=3):

        if not self.documents:
            return []

        query_words = query.lower().split()

        results = []

        for doc in self.documents:

            score = 0

            text = doc["text"].lower()

            for word in query_words:

                if word in text:
                    score += 1

            results.append(
                {
                    "source": doc["source"],
                    "text": doc["text"],
                    "score": score
                }
            )

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:top_k]