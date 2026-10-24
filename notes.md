
# Project Notes

- **Tradeoffs with the 2-day constraint:** I focused on getting the main flow working end to end: a React chat UI, a FastAPI backend, and three tools. I kept the knowledge base small and used simple keyword search instead of adding a vector database. I also kept the UI and setup straightforward, and left authentication, persistent chat history, and deployment out of scope.

- **Trickiest part of tool-calling:** Making sure the model’s tool choice was translated into a valid call, the tool result was returned to the model, and the final response explained the result rather than just displaying raw tool output. Handling invalid arguments and tool/API errors was also important.

- **Scaling to 50 tools:** I would use a central tool registry with clear descriptions and input schemas, and keep each tool’s implementation separate from the agent. I’d group tools by capability or retrieve only the most relevant tools for each question, rather than presenting all 50 to the model every time. I’d also add stronger validation, timeouts, logging, and tests for tool selection and multi-tool workflows.
