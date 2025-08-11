# Shopify MCP OpenAI Agents

Welcome to **Shopify MCP OpenAI Agents**! This project enables seamless integration of OpenAI and Gemini APIs with your Shopify store using the Model Context Protocol (MCP).

---

## 🚀 Features

- **Easy Integration**: Connect your Shopify store with OpenAI and Gemini APIs.
- **MCP Endpoint**: Expose a standardized MCP endpoint for your store.
- **Configurable**: Use environment variables for quick setup.
- **Modern Python Project**: Built with best practices and easy to extend.

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/muhammadahmad1857/shopify_mcp_openai_agents.git
   cd shopify_mcp_openai_agents
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or, if using Poetry:
   ```bash
   poetry install
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your keys and store name:
     ```bash
     cp .env.example .env
     # Edit .env with your API keys and Shopify store name
     ```

4. **Configure environment variables**
   - Activate your virtual environment:
     ```bash
     .venv/Scripts/activate
     ```
---

## ⚡ Usage

1. **Start the MCP server**
   ```bash
   python main.py
   ```

2. **Access your MCP endpoint**
   - The endpoint will be:
     ```
     https://<STORE_NAME>.myshopify.com/api/mcp
     ```
   - Example:
     ```
     https://example.myshopify.com/api/mcp
     ```

---

## 📄 Environment Variables

Edit your `.env` file:

```env
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
STORE_NAME=YOUR_SHOPIFY_STORE_NAME
```

---

## 🧩 MCP Endpoint Details

- **Path:** `/api/mcp`
- **Base URL:** `https://<STORE_NAME>.myshopify.com`
- **Example:** `https://example.myshopify.com/api/mcp`

---