import { useEffect, useState } from "react";
import {
  Activity,
  DollarSign,
  Radar,
  ShieldCheck,
  Target,
  TrendingUp,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import "./App.css";

type AdvisorResponse = {
  symbol: string;
  recommendation: string;
  confidence: number;
  reason: string;
  price: number;
  risk?: {
    entry: number;
    stop_loss: number;
    take_profit: number;
    risk_reward: number;
  };
  rules_passed?: string[];
  rules_failed?: string[];
  indicators?: {
    rsi: number;
    macd: number;
    macd_signal: number;
    macd_histogram: number;
    volume: number;
    volume_avg_20: number;
  };
};

type Candle = {
  index: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  ema_20?: number;
  ema_50?: number;
  ema_200?: number;
};

type Trade = {
  symbol: string;
  strategy: string;
  direction: "LONG" | "SHORT";
  score: number;
  max_score: number;
  confidence: number;
  entry: number;
  reason: string[];
  risk: {
    entry: number;
    stop_loss: number;
    take_profit: number;
    risk_reward: number;
  };
  risk_reward: number;
};

type StrategiesResponse = {
  symbol: string;
  trade_count?: number;
  message?: string;
  top_trades: Trade[];
};

function App() {
  const [advisor, setAdvisor] = useState<AdvisorResponse | null>(null);
  const [selectedSymbol, setSelectedSymbol] = useState("ETH")
  const [candles, setCandles] = useState<Candle[]>([]);
  const [scanStep, setScanStep] = useState(0);
  const [strategies, setStrategies] = useState<any>(null);

  const backendUrl =
    "https://legendary-invention-9jpr996vqg63p79q-8000.app.github.dev";

  const scanMessages = [
    "Scanning ETH market structure...",
    "Checking EMA alignment...",
    "Evaluating volume pressure...",
    "Detecting market regime...",
    "Calculating risk model...",
    "Signal package complete.",
  ];

  useEffect(() => {
    fetch(`${backendUrl}/advisor/${selectedSymbol}`)
      .then((res) => res.json())
      .then((data) => setAdvisor(data))
      .catch((err) => console.error("Advisor fetch error:", err));

    fetch(`${backendUrl}/candles/${selectedSymbol}`)
      .then((res) => res.json())
      .then((data) => setCandles(data))
      .catch((err) => console.error("Candles fetch error:", err));

      fetch(`${backendUrl}/strategies/${selectedSymbol}`)
      .then((res) => res.json())
      .then((data) => setStrategies(data))
      .catch((err) => console.error("Strats fetch error:", err)); 

  }, [selectedSymbol]);

  useEffect(() => {
    const interval = setInterval(() => {
      setScanStep((prev) => (prev + 1) % scanMessages.length);
    }, 1400);

    return () => clearInterval(interval);
  }, []);

  if (!advisor) {
    return (
      <div className="loading-screen">
        <div className="radar-loader"></div>
        <h2>Booting Sentinel RF...</h2>
      </div>
    );
  }

  const signalClass = advisor.recommendation.toLowerCase();
  const rsi = advisor.indicators?.rsi;
  const macd = advisor.indicators?.macd;
  const macdSignal = advisor.indicators?.macd_signal;
  const volume = advisor.indicators?.volume;
  const volumeAvg = advisor.indicators?.volume_avg_20;
  const macdHistogram = advisor.indicators?.macd_histogram;
  

  const macdStatus =
    macdHistogram === undefined
      ? "N/A"
      : macdHistogram > 0
      ? "Bullish"
      : "Bearish";

  const volumeStatus =
    volume !== undefined && volumeAvg !== undefined && volume > volumeAvg
      ? "Above Avg"
      : "Below Avg";

  const rsiStatus =
    rsi === undefined
      ? "N/A"
      : rsi > 70
      ? "Overbought"
      : rsi < 30
      ? "Oversold"
      : rsi >= 45 && rsi <= 68
      ? "Healthy"
      : "Neutral";

  return (
    <div className="dashboard">
      <div className="background-grid"></div>

      <header className="topbar">
        <div>
          <h1>SENTINEL RF</h1>
          <p>Autonomous Crypto Signal Intelligence</p>
        </div>
        
        <select
          className="symbol-select"
          value={selectedSymbol}
          onChange={(e) => {
            setAdvisor(null);
            setCandles([]);
            setSelectedSymbol(e.target.value);

          }}
        >
          <option value="ETH">ETH</option>
          <option value="BTC">BTC</option>
          <option value="ADA">ADA</option>
          <option value="XRP">XRP</option>
          <option value="SOL">SOL</option>
        </select> 

        <div className="status-pill">
          <span className="pulse-dot"></span>
          LIVE SCAN
        </div>
      </header>

      <section className="hero-grid">
        <div className={`signal-card ${signalClass}`}>
          <Radar size={42} />
          <p>RECOMMENDATION</p>
          <h2>{advisor.recommendation}</h2>
        </div>

        <div className="card">
          <Activity />
          <p>SETUP STRENGTH</p>
          <h2>{advisor.confidence}%</h2>

          <div className="gauge">
            <div style={{ width: `${advisor.confidence}%` }}></div>
          </div>
        </div>

        <div className="card">
          <DollarSign />
          <p>CURRENT PRICE</p>
          <h2>${advisor.price?.toFixed(2)}</h2>
        </div>

        <div className="card">
          <Target />
          <p>RISK / REWARD</p>
          <h2>{advisor.risk?.risk_reward ?? "N/A"}</h2>
        </div>
      </section>

      {strategies && (
        <section className="strategy-grid">
          {strategies.top_trades.map((trade: Trade) => (
            <div key={trade.strategy} className="strategy-card">
              <div className="strategy-header">
                <h3>{trade.strategy.replaceAll("_", " ")}</h3>
          
                <span
                  className={
                    trade.direction === "LONG"
                      ? "strategy-long"
                      : "strategy-short"
                  }
                >
                  {trade.direction}
                </span>
              </div>
                
              <div className="strategy-confidence">
                <span>Confidence</span>
                <strong>{trade.confidence}%</strong>
              </div>
                
              <div className="strategy-bar">
                <div
                  style={{
                    width: `${trade.confidence}%`,
                  }}
                />
              </div>
                
              <div className="strategy-prices">
                <div>
                  <span>Entry</span>
                  <strong>${trade.risk.entry}</strong>
                </div>
                
                <div>
                  <span>Stop</span>
                  <strong>${trade.risk.stop_loss}</strong>
                </div>
                
                <div>
                  <span>Target</span>
                  <strong>${trade.risk.take_profit}</strong>
                </div>
                
                <div>
                  <span>R:R</span>
                  <strong>{trade.risk_reward}</strong>
                </div>
              </div>
                
              <div className="strategy-reasons">
                {trade.reason.map((reason) => (
                  <p key={reason}>✓ {reason}</p>
                ))}
              </div>
            </div>
          ))}
        </section>
      )}


      <section className="rules-grid">
        <div className="card">
          <div className="section-title">
            <ShieldCheck />
            <h3>Rules Passed</h3>
          </div>

          {advisor.rules_passed?.map((rule, index) => (
            <p className="pass" key={index}>
              ✓ {rule}
            </p>
          ))}
        </div>

        <div className="card">
          <h3>Rules Failed</h3>

          {advisor.rules_failed?.map((rule, index) => (
            <p className="fail" key={index}>
              ✕ {rule}
            </p>
          ))}
        </div>
      </section>

      <section className="main-grid">
        <div className="chart-card">
          <div className="section-title">
            <TrendingUp />
            <h3>{selectedSymbol} Price Feed</h3>
          </div>

          <div className="chart-legend">
            <span><i className="chip price"></i>Price</span>
            <span><i className="chip ema20"></i>EMA20</span>
            <span><i className="chip ema50"></i>EMA50</span>
            <span><i className="chip ema200"></i>EMA200</span>
          </div>

          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={candles}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.15} />
              <XAxis dataKey="index"
                tick={{ fill: "#94a3b8", fontSize: 11 }}
                tickFormatter={(value) =>
                  new Date(value).toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })
                } 
              />
              <YAxis domain={["auto", "auto"]} />
              <Tooltip
                labelFormatter={(label) =>
                  new Date(label).toLocaleString([], {
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false,
                  })
                }
                contentStyle={{
                  background: "rgba(15, 23, 42, 0.95)",
                  border: "1px solid rgba(34, 197, 94, 0.3)",
                  borderRadius: "14px",
                  padding: "14px",
                  backdropFilter: "blur(10px)",
                  boxShadow: "0 12px 30px rgba(0,0,0,0.45)",
                }}
                labelStyle={{
                  color: "#86efac",
                  fontWeight: 700,
                  marginBottom: "8px",
                }}
                itemStyle={{
                  color: "#e2e8f0",
                  padding: "3px 0",
                }}
                formatter={(value: number) => `$${value.toFixed(2)}`}
              />

              <Line
                type="monotone"
                dataKey="close"
                stroke="#89cff0"
                strokeWidth={3}
                dot={false}
                isAnimationActive={true}
              />

              <Line
                type="monotone"
                dataKey="ema_20"
                stroke="#22c55e"
                strokeWidth={2}
                dot={false}
                isAnimationActive={true}
              />

              <Line
                type="monotone"
                dataKey="ema_50"
                stroke="#facc15"
                strokeWidth={2}
                dot={false}
                isAnimationActive={true}
              />

              <Line
                type="monotone"
                dataKey="ema_200"
                stroke="#ef4444"
                strokeWidth={2}
                dot={false}
                isAnimationActive={true}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="scanner-card">
          <h3>TACTICAL SCAN</h3>

          <div className="radar-screen">
            <div className="radar-circle">
              <div className="radar-sweep"></div>
            </div>
          </div>

          <p className="scan-message">{scanMessages[scanStep]}</p>

          <div className="scan-checklist">
            <p>✓ Trend Analysis Complete</p>
            <p>✓ Volume Analysis Complete</p>
            <p>✓ Regime Detection Complete</p>
            <p>✓ Risk Assessment Complete</p>
          </div>
        </div>
      </section>
      
      <section className="diagnostics-grid">
        <div className="indicator-card">
          <p>RSI MOMENTUM</p>
          <h2>{rsi?.toFixed(1) ?? "N/A"}</h2>
          <span className={`indicator-status ${rsiStatus.toLowerCase()}`}>
            {rsiStatus}
          </span>

          <div className="rsi-track">
            <div
              className="rsi-marker"
              style={{ left: `${rsi ?? 0}%` }}
            ></div>
          </div>

          <div className="rsi-labels">
            <span>Oversold</span>
            <span>Neutral</span>
            <span>Overbought</span>
          </div>
        </div>

        <div className="indicator-card">
          <p>MACD MOMENTUM</p>

          <h2 className={macdStatus === "Bullish" ? "bullish-text" : "bearish-text"}>
            {macdStatus}
          </h2>

          <span>MACD: {macd?.toFixed(2) ?? "N/A"}</span>
          <span>Signal: {macdSignal?.toFixed(2) ?? "N/A"}</span>
          <span>Histogram: {macdHistogram?.toFixed(2) ?? "N/A"}</span>

          <div className="macd-meter">
            <div
              className={macdStatus === "Bullish" ? "macd-positive" : "macd-negative"}
              style={{
                width: `${Math.min(Math.abs(macdHistogram ?? 0) * 5, 100)}%`,
              }}
            ></div>
          </div>
        </div>
            
        {/*   */}
      </section>

      <section className="card reason-card">
        <h3>Analyst Summary</h3>
        <p>{advisor.reason}</p>
      </section>
    </div>
  );
}

export default App;