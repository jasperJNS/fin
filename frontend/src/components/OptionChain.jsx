import React, {useState} from 'react';

function OptionChain(props) {
    return (
        <table>
            <thead>
                <tr>
                    <th>STONKS</th>
                </tr>
            </thead>
            {props.stocks.map((v, i) => {
                return <tr>
                    <th>{v[0]}</th>
                </tr>
            })}
        </table>
    )
}

export default OptionChain;