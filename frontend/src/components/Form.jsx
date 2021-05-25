import React, {useState} from 'react';
import {json as requestJson} from 'd3-request';

function StockForm({addStockLog}) {
    const handleSubmit = (e) => {
        addStockLog([ticker])
        e.preventDefault();
        fetch(`http://localhost:5000/api/options/${ticker}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'crossDomain': true
            }
        }).then((error, response) => {
            if (!error) {
                console.log(response)
            }
        })
    
    }
    const [ticker, setTicker] = useState();


    return (
        <form onSubmit={e => {handleSubmit(e)}}>
            <label>STONK</label>
            <br />
            <input
                name='ticker'
                type='text'
                value={ticker}
                onChange={e => setTicker(e.target.value)}
            />

            <input
                className='submitButton'
                type='submit'
                value='Get Options'
            />
        </form>
    )
}

export default StockForm;