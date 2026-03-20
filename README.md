# Hawk Navigator - LPC AI Chatbot

An AI-powered chatbot for Las Positas College that answers questions about the school using web-scraped data and GPT.

## Tech Stack

- **Firecrawl** — Web scraping the LPC website
- **ChromaDB** — Vector database for storing and querying content
- **Replicate (GPT)** — AI responses
- **Flask** — Web server

## Setup

1. Clone the repo
2. Install dependencies:
```
   pip install -r requirements.txt
```
3. Set environment variables:
```
   FIRECRAWL_API_KEY=your_key_here
   REPLICATE_API_TOKEN=your_key_here
   CHROMADB_API_KEY=your_key_here
```
4. Run the app:
```
   python main.py
```

## Usage

Visit `https://www.laspositascollege.edu/` and ask questions about Las Positas College.

## Author

Created by the Las Positas College Data Science Club
