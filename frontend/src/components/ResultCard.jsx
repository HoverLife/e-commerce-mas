import React from 'react';

function ResultCard({ item }) {
  return (
    <div className="result-card">
      <h3>{item.name}</h3>
      <p>Категория: {item.category}</p>
      <p>Цена: ${item.price}</p>
    </div>
  );
}

export default ResultCard;
