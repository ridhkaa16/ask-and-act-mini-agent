
import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function sendMessage(event) {
    event.preventDefault();

    const question = message.trim();
    if (!question || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", text: question },
    ]);
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: question }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: data.answer || "I couldn't generate an answer.",
          tools: data.tools_used || [],
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: "I couldn't connect to the backend. Please check that your FastAPI server is running on port 8000.",
          tools: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="header">
        <div className="logo">✦</div>
        <div>
          <h1>Ask & Act</h1>
          <p>Your personal AI assistant</p>
        </div>
        <span className="status">● Ready</span>
      </header>

      <section className="chat">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">✦</div>
            <h2>How can I help you today?</h2>
            <p>Ask a question. I'll find answers and use tools when needed.</p>
            <div className="suggestions">
              {[
                "What is 25 multiplied by 16?",
                "What is the weather in London?",
                "Search for Python information",
              ].map((item) => (
                <button key={item} onClick={() => setMessage(item)}>
                  {item} →
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="messages">
            {messages.map((item, index) => (
              <div className={`message ${item.role}`} key={index}>
                <div className="message-label">
                  {item.role === "user" ? "You" : "Ask & Act"}
                </div>
                <div className="message-text">{item.text}</div>
                {item.tools?.length > 0 && (
                  <div className="tools">
                    {item.tools.map((tool) => (
                      <span className="tool-badge" key={tool}>
                        ⚙ {tool}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="message assistant">
                <div className="message-label">Ask & Act</div>
                <div className="message-text">Thinking...</div>
              </div>
            )}
          </div>
        )}
      </section>

      <form className="input-area" onSubmit={sendMessage}>
        <input
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask anything..."
          aria-label="Your message"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !message.trim()}>
          {loading ? "..." : "Send ↑"}
        </button>
      </form>

      <footer>Powered by AI · Tools that help you get things done</footer>
    </main>
  );
}

export default App;
