import './App.css';
import React from 'react';
import {useState} from 'react';
import StockForm from './components/Form';
import OptionChain from './components/OptionChain';

function App() {
  const [tickers, setTickers] = useState([]);

  const addTicker = (ticker) => {
    let stocks = [...tickers, ticker];
    setTickers(stocks);
  }

  return (
    <section>
      <StockForm addStockLog={addTicker}/>
      <OptionChain stocks={tickers}/>
    </section>
  );
}

export default App;
