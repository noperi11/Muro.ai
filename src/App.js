import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const sendPrompt = async () => {
    if (!prompt.trim()) return;
    setIsLoading(true);
    setResponse('');
    setHistory([...history, { role: 'user', content: prompt }]);

    const res = await fetch('http://192.168.1.11:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    const botReply = data.response || '[ERROR]';

    setResponse(botReply);
    setHistory(prev => [...prev, { role: 'assistant', content: botReply }]);
    setPrompt('');
    setIsLoading(false);
  };

  return (
    <div className="chat-container">
      <h1>LLaMA 3 Chat</h1>

      <div className="chat-box">
        {history.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You:' : 'LLaMA:'}</strong>
            <div>{msg.content}</div>
          </div>
        ))}
        {isLoading && <div className="chat-message assistant">Typing...</div>}
      </div>

      <textarea
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        placeholder="Tulis pertanyaan kamu di sini..."
      />
      <button onClick={sendPrompt}>Kirim</button>
    </div>
  );
}

export default App;

