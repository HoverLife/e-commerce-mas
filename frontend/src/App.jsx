import React, { useState } from 'react';
import axios from 'axios';
import ResultCard from './components/ResultCard';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [ctr, setCtr] = useState(null);

  const fetchRecommendations = () => {
    axios.get('/simulate?count=1')
      .then(response => {
        setRecommendations(response.data.recommendations);
        setCtr(response.data.ctr);
      })
      .catch(error => {
        console.error('Error fetching recommendations:', error);
      });
  };

  return (
    <div className="App">
      <h1>Рекомендации товаров</h1>
      <button onClick={fetchRecommendations}>Получить рекомендации</button>
      {ctr !== null && (
        <p>CTR последней сессии: {(ctr * 100).toFixed(2)}%</p>
      )}
      <div className="results">
        {recommendations.map(item => (
          <ResultCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}

export default App;
