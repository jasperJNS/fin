import React, {useState} from 'react';

function StockForm({setIsLoading, setTicker}) {

    const handleSubmit = (e) => {
        e.preventDefault();
        
        fetch(`http://localhost:5000/api/options/${tickerQuery}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'crossDomain': true
            }
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            setTicker(JSON.stringify(data));
            setIsLoading(false);
        }, [])
        .catch(err => {
            console.log(err);
        })
    
    }
    const [tickerQuery, setTickerQuery] = useState(null);

    return (
        <form onSubmit={e => {handleSubmit(e)}}>
            <label>STONK</label>
            <br />
            <input
                name='ticker'
                type='text'
                onChange={e => setTickerQuery(e.target.value)}
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