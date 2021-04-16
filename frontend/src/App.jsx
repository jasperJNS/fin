import Chart from "./components/Chart.jsx"
import React, { useState } from "react"
import "./components/Chart.css"

function App() {
  return (
    <div className="box">
      <div className="chart">
        <Chart
          symbol="AAPL"
          theme="DARK"
        />
      </div>
      <div className="control-panel">

      </div>
    </div>
  );
}

export default App;
