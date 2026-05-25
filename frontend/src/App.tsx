import { useEffect, useState } from "react";
import "./App.css";

type AdvisorResponse = {
  symbol: string;
  recommendation: string;
  confidence: number;
  reason: string;
  price: number;
  rsi: number;
  macd: number;
  macd_signal: number;
  ema_20: number;
  ema_200: number;
  rules_passed: string[];
  rules_failed: string[];
};

function App() {
  const [advisor, setAdvisor] = useState<AdvisorResponse | null>(null);

  useEffect(() => {
    fetch(
      "https://legendary-invention-9jpr996vqg63p79q-8000.app.github.dev/advisor/ETH"
    )
      .then((res) => res.json())
      .then((data) => setAdvisor(data))
      .catch((err) => console.error("Error fetching advisor data:", err));
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Sentinel Crypto Advisor</h1>

      {!advisor && <p>Loading advisor data...</p>}

      {advisor && (
        <div>
          <h2>{advisor.symbol}</h2>

          <h3>Recommendation: {advisor.recommendation}</h3>

          <p>Setup Strength: {advisor.confidence}%</p>

          <p>Current Price: ${advisor.price}</p>

          <p>{advisor.reason}</p>

          <h3>Rules Passed</h3>
          <ul>
            {advisor.rules_passed.map((rule) => (
              <li key={rule}>✅ {rule}</li>
            ))}
          </ul>

          <h3>Rules Failed</h3>
          <ul>
            {advisor.rules_failed.map((rule) => (
              <li key={rule}>❌ {rule}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;