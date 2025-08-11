import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams


_: bool = load_dotenv(find_dotenv())
store_name=os.getenv("STORE_NAME")
# URL of our standalone MCP server (from shared_mcp_server)
MCP_SERVER_URL = f"{store_name}/api/mcp" # Ensure this matches your running server
gemini_api_key = os.getenv("GEMINI_API_KEY")

#Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

sys_msg = """
You are an expert e-commerce assistant tasked with helping users with their shopping and product-related queries. You must provide detailed, accurate responses about products, including comprehensive information about pricing, availability, specifications, and purchasing options. You have access to powerful tools through the MCP (Multi-Channel Platform) to assist you:

1. **get_product_details**: This tool retrieves detailed product information including:
   - Product name and description
   - Current price and any discounts
   - Available sizes, colors, and variants
   - Stock levels and availability
   - Product specifications and features
   - Brand information
   - Product categories and tags
   - Customer ratings and reviews
   - Shipping options and estimated delivery times

2. **search_products**: This tool allows you to search the product catalog by:
   - Keywords and product names
   - Categories and departments
   - Price ranges
   - Brands
   - Availability status
   - Rating thresholds
   - Special offers and promotions
   - Recently added items
   
**Precautions:**
- Read the tool list clearly to analyze which arguments are required and which are not!!
- And always understand the user query and if something you cant understand from that but its required you have to ask user about that?

Use these tools effectively to provide accurate product recommendations, compare options, check availability, and help users make informed purchasing decisions. Always include relevant product details, pricing information, and availability status in your responses.
"""

def get_instructions_with_history(base_instructions, message_history):
    """Create instructions that include recent conversation history"""
    if not message_history:
        return base_instructions
    
    history_text = "\n\n**Recent Conversation History (Last 5 messages):**\n"
    for i, message in enumerate(message_history[-5:], 1):
        history_text += f"{i}. {message}\n"
    
    return base_instructions + history_text

async def main():
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
    
    # Store conversation history (last 5 messages)
    message_history = []

    async with MCPServerStreamableHttp(params=mcp_params, name="MySharedMCPServerClient") as mcp_server_client:
        print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' created and entered context.")
        print("The SDK will use this client to interact with the MCP server.")

        try:
            tools = await mcp_server_client.list_tools()
            print(f"Tools: {tools}")
            print("--------------------------------")
            print("E-commerce Assistant is ready! Type 'exit' or 'stop' to quit.")
            print("================================")
            
            while True:
                try:
                    query = input("\nENTER YOUR QUERY: ").strip()
                    
                    # Check for exit conditions
                    if query.lower() in ['exit', 'stop']:
                        print("Goodbye! Thanks for using the E-commerce Assistant.")
                        break
                    
                    if not query:
                        print("Please enter a valid query or type 'exit' to quit.")
                        continue
                    
                    # Create agent with current conversation history
                    current_instructions = get_instructions_with_history(sys_msg, message_history)
                    assistant = Agent(
                        name="MyMCPConnectedE-commerceAssistant",
                        instructions=current_instructions,
                        mcp_servers=[mcp_server_client],
                        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
                    )
                    
                    # Run the query
                    result = await Runner.run(assistant, query)
                    response = result.final_output
                    
                    print(f"\n[AGENT RESPONSE]: {response}")
                    
                    # Update message history (keep last 5 messages total)
                    message_history.append(f"User: {query}")
                    message_history.append(f"Assistant: {response}")
                    
                    # Keep only last 5 messages (alternating user/assistant pairs)
                    if len(message_history) > 5:
                        message_history = message_history[-5:]
                    
                    print("\n" + "="*50)
                    
                except KeyboardInterrupt:
                    print("\n\nInterrupted by user. Goodbye!")
                    break
                except Exception as e:
                    print(f"\nAn error occurred while processing your query: {e}")
                    print("Please try again or type 'exit' to quit.")

        except Exception as e:
            print(f"An error occurred during agent setup or tool listing: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An unhandled error occurred in the agent script: {e}")