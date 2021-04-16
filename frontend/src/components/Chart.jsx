import { PureComponent } from 'react';
import TradingViewWidget, { Themes } from 'react-tradingview-widget';
import "./Chart.css"

export default class Chart extends PureComponent{
    render() {
        return (
            <TradingViewWidget
                symbol={this.props.symbol}
                theme={this.props.theme}
                autosize
            />
        )
    }
};