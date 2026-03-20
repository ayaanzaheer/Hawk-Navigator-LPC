import chromadb
import csv
from firecrawl import Firecrawl
import replicate
import os
from flask import Flask, request, send_from_directory
import pathlib

firecrawl = Firecrawl(api_key=os.environ.get("FIRECRAWL_API_KEY"))

docs = firecrawl.crawl(url="https://www.laspositascollege.edu/",
                       limit=200,
                       max_discovery_depth=2,
                       scrape_options={"formats": ["markdown"]})

print(docs)
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "Content", "Markdown"])

    for doc in docs.data:
        writer.writerow([
            getattr(doc.metadata, 'sourceURL', '')
            if hasattr(doc, 'metadata') else '',
            getattr(doc.metadata, 'title', '') if hasattr(doc, 'metadata') else
            '', doc.markdown if hasattr(doc, 'markdown') else ''
        ])

client = chromadb.CloudClient(api_key=os.environ.get("CHROMADB_API_KEY"),
                              tenant='36bcfb8c-b4cc-4a7d-ac21-07216e071735',
                              database='info')

collection_2_1 = client.get_collection(name="lebron67goatmaster")


def defineGPTMain(question):
    results = collection_2_1.query(
        query_texts=[question],
        n_results=2,
        include=['documents', 'metadatas', 'distances'])
    print(results)

    text = ""
    for event in replicate.stream(
            "openai/gpt-5",
            input={
                "prompt": question + str(results),
                "messages": [],
                "verbosity": "medium",
                "image_input": [],
                "reasoning_effort": "minimal"
            },
    ):
        text += str(event)

    return str(text)


collection_2_1.add(ids=["id1", "id2", "id3", "id4", "id5", "id6", "id7"],
                   documents=[
                       "Shaq",
                       "Michael Jeffrey Jordan",
                       "Lebron Raymone James",
                       "Kevin Hart",
                       "G.O.A.T.",
                       "lionel Messi",
                       "Cristiano Ronaldo",
                   ])
print("Lebron is the chosen one!!")

# Create a Flask application instance
app = Flask(__name__)

ROOT = pathlib.Path(__file__).parent.resolve()


@app.route('/')
def serve_ui():
    return send_from_directory(ROOT / 'static', 'index.html')


# handles search queries
@app.route('/api', methods=['GET'])
def hello_world():
    query = request.args.get('query', '').strip()
    if not query:
        return "No query provided.", 200
    return defineGPTMain(query)


# Define a route for the root URL ("/")
@app.route('/test')
def hop():
    query = request.args.get('query', 'default_query')

    return defineGPTMain(query)


# Run the Flask development server if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
