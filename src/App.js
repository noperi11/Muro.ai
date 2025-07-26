import React, { useState, useRef, useEffect } from 'react';
import './index.css' // Ganti jika kamu pakai ikon lain
import {marked} from 'marked'


const SendIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="white"/>
  </svg>
);
const Chatbot = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Halo! Ada yang bisa saya bantu?' }
  ]);
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages, isLoading]);
    useEffect(() => {
    const textarea = document.querySelector('textarea');
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }, [prompt]);

  const sendPrompt = async () => {
  if (!prompt.trim()) return;

  const newMessages = [...messages, { role: 'user', content: prompt }];
  setMessages(newMessages);
  setPrompt('');
  setIsLoading(true);

  // Ganti pake IP pc server kalo mau dipake di lab
  try {
    const response = await fetch('http://192.168.100.121:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ prompt })
    });

    const data = await response.json();

    // Tangani kasus jika response-nya pakai field `response`, `message`, atau lainnya
    const assistantReply = data.response || data.message || data;

    setMessages([...newMessages, { role: 'assistant', content: assistantReply }]);
  } catch (error) {
    setMessages([...newMessages, {
      role: 'assistant',
      content: 'Terjadi kesalahan saat menghubungi server.'
    }]);
    console.error('Error:', error);
  } finally {
    setIsLoading(false);
  }
};


  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendPrompt();
    }
  };

  const renderContent = (content) => {
  const html = marked.parse(content, {
    breaks: true
  });
  return <div dangerouslySetInnerHTML={{ __html: html }} className="prose prose-invert max-w-none" />;
};


  return (
   <>
  {/* HEADER */}
  <div className="p-4 bg-black flex-shrink-0">
    <div className="flex items-center gap-3">
      <div className="font-baumans text-3xl px-10 py-1 bg-gradient-to-r from-[#41A3FF] to-[#E100FF] rounded-full text-white font-bold w-fit">
        Muro AI
      </div>
      <div className="w-8 h-8 px-5 py-5 rounded-full bg-gradient-to-br from-[#E100FF] to-[#41A3FF]" />
    </div>
  </div>

  {/* LAYOUT UTAMA */}
  <div className="h-[75vh] w-screen bg-black flex flex-col font-sans overflow-hidden">
    
    {/* Kontainer chat box (scrollable) */}
    <div className="flex-1 px-4 overflow-hidden">
      <div className="h-full bg-[#161625] rounded-2xl border border-white/10 p-6 flex flex-col gap-4 overflow-y-auto">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-4 rounded-2xl text-white ${
              msg.role === 'user'
                ? 'bg-[#c863f5] rounded-br-none'
                : 'bg-[#33364a] rounded-bl-none'
            }`}>
              {renderContent(msg.content)}
            </div>
          </div>
        ))}

        {/* Indikator loading */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] p-4 rounded-2xl text-white bg-[#c863f5] rounded-br-none">
              <div className="flex items-center gap-2">
                <span className="text-sm">Muro AI is typing</span>
                <div className="w-2 h-2 bg-white rounded-full animate-pulse [animation-delay:-0.3s]" />
                <div className="w-2 h-2 bg-white rounded-full animate-pulse [animation-delay:-0.15s]" />
                <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  </div>
  {/* FORM INPUT */}
    <div className="fixed bottom-0 left-0 w-full px-4 py-3 z-10 pointer-events-none">
      <div className="max-w-screen mx-auto pointer-events-auto">
        <form
          onSubmit={(e) => { e.preventDefault(); sendPrompt(); }}
          className="flex items-center gap-4"
        >
          <div className="flex-grow">
            <div className="bg-gradient-to-r from-[#E100FF] to-[#41A3FF] p-[2px] rounded-2xl">
              <div className="bg-[#1e1e30] rounded-2xl px-5 py-3">
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Pertanyaanmu disini..."
                  rows={1}
                  className="w-full bg-transparent text-white placeholder-gray-400 border-none focus:outline-none focus:ring-0 resize-none overflow-hidden max-h-[192px]"
                  disabled={isLoading}
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="w-12 h-12 rounded-full bg-gradient-to-br from-[#a33cf5] to-[#e55fa4] flex items-center justify-center text-white transition-transform duration-200 hover:scale-110 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading || !prompt.trim()}
          >
            <SendIcon />
          </button>
        </form>
      </div>
    </div>
</>

  );
};

export default Chatbot;
