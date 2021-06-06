import './App.css';
import React from 'react';
import {useState} from 'react';
import StockForm from './components/Form';
import OptionChain from './components/OptionChain';

function App() {
  const [ticker, setTicker] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  return (
    <section>
      <StockForm setIsLoading={setIsLoading} setTicker={setTicker}/>
      <OptionChain ticker={ticker}/>
    </section>
  );
}

export default App;
