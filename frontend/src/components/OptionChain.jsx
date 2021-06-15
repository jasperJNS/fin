import React from 'react';
import Plot from "react-plotly.js";

function OptionChain({ticker}) {
    return (
        <div>
            {Object.keys(ticker).map((data, key) => {
                return (
                    <div key={key}>
                        {data}
                    </div>
                ) 
            })}
        </div>
    )
}

export default OptionChain;