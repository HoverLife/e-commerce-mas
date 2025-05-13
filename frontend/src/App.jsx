import React, { useState } from 'react';
import ResultCard from './ResultCard';

function App() {
  const [messages, setMessages] = useState([]);
  const [agreement, setAgreement] = useState(false);

  const handleSimulate = async () => {
    const response = await fetch('/simulate', { method: 'POST' });
    const data = await response.json();
    setMessages(data.messages);
    setAgreement(data.agreement);
  };

  return (
    <div className="App">
      <button onClick={handleSimulate}>Simulate Negotiation</button>
      {messages.map((msg, index) => (
        <ResultCard key={index} sender={msg.sender} text={msg.text} />
      ))}
      {agreement && <div>Agreement reached!</div>}
    </div>
  );
}

export default App;
