import React from 'react';

function ResultCard({ sender, text }) {
  return (
    <div className="result-card">
      <strong>{sender}:</strong> {text}
    </div>
  );
}

export default ResultCard;
