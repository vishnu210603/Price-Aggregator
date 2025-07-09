import { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [country, setCountry] = useState('US');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchResults = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ country, query }),
      });

      if (!res.ok) {
        const body = await res.json();
        throw new Error(body.detail || 'Server error');
      }

      const data = await res.json();
      setResults(data);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    }

    setLoading(false);
  };

  return (
    <div className="App" style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Product Price Aggregator</h1>

      <div style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Search product..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ padding: '0.5rem', width: '300px' }}
        />
        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          style={{ marginLeft: '1rem', padding: '0.5rem' }}
        >
          <option value="US">USA</option>
          <option value="IN">India</option>
        </select>
        <button
          onClick={fetchResults}
          style={{ marginLeft: '1rem', padding: '0.5rem 1rem' }}
        >
          {loading ? 'Searching…' : 'Search'}
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {results.length > 0 && (
        <div>
          {results.map((item, idx) => (
            <div
              key={idx}
              style={{
                border: '1px solid #ddd',
                padding: '1rem',
                marginBottom: '1rem',
                borderRadius: '4px',
              }}
            >
              <h3>{item.productName}</h3>
              <p>
                Price: <strong>{item.price} {item.currency}</strong>
              </p>
              <p>Source: {item.source}</p>
              <a href={item.link} target="_blank" rel="noreferrer">
                View on Website
              </a>
            </div>
          ))}
        </div>
      )}

      {!loading && results.length === 0 && !error && (
        <p>No results yet. Enter a query above.</p>
      )}
    </div>
  );
}

export default App;
