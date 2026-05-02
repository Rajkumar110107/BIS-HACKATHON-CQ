import { useState } from 'react';
import axios from 'axios';
import { Search, Loader2, Zap, FileText } from 'lucide-react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [latency, setLatency] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults([]);
    setLatency(null);

    try {
      const response = await axios.post('http://localhost:5000/search', {
        query: query
      });

      if (response.data && response.data.retrieved_standards) {
        setResults(response.data.retrieved_standards);
        
        // Check if latency is provided
        if (response.data.latency_seconds !== undefined) {
          setLatency(response.data.latency_seconds);
        }
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error("API Error:", err);
      setError(err.response?.data?.error || 'Failed to connect to the recommendation engine.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>⚡ BIS AI Standard Finder</h1>
        <p>AI-powered recommendation engine for Indian Standards</p>
      </header>

      <form className="search-section" onSubmit={handleSearch}>
        <input
          type="text"
          className="search-input"
          placeholder="Enter query (cement, steel, soil...)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="search-button" disabled={loading || !query.trim()}>
          {loading ? <Loader2 className="spinner" size={20} /> : <Search size={20} />}
          <span style={{ marginLeft: '8px' }}>{loading ? 'Searching' : 'Search'}</span>
        </button>
      </form>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          <Loader2 className="spinner" size={30} style={{ animation: 'spin 1s linear infinite' }} />
          <span>Crunching semantic vectors...</span>
        </div>
      )}

      {!loading && results.length > 0 && (
        <div className="results-grid">
          {results.map((standard, index) => (
            <div 
              key={`${standard}-${index}`} 
              className="result-card"
              style={{ animationDelay: `${index * 0.15}s` }}
            >
              <div className="rank-badge">{index + 1}</div>
              <FileText color="#38bdf8" size={24} />
              <h3 className="standard-name">{standard}</h3>
            </div>
          ))}
        </div>
      )}

      {!loading && latency !== null && results.length > 0 && (
        <div className="latency-display">
          <Zap size={16} color="#10b981" />
          <span>Latency:</span>
          <span className="latency-value">{latency.toFixed(3)}s</span>
        </div>
      )}
      
      {/* Required spin animation for lucide-react Loader2 */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default App;
