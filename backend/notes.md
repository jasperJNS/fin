
5 min returns of stock intraday and overnights/weekends
variance for every block for a few years
aggregate by days in the monthly expiration cycle

variance-time is now our measuring stick.

time flows slow on the weekend
faster on weekdays
fastest on earnings day

lots of variance on monday morning 9:35 to 9:40 am -> time flows fast in that 5 min block
renormalize variance for proper units

toss out variance data from earnings days (black hole of vol)

how far back?
A: bias vs variance

market crash?
probably toss out depending on model

Aggregate monthly or weekly?



delta: change of option value as a function of the underlying
    underlying moves in your favor -> make more than you should
    underlying moves against you -> lose less than you should

the "should" is paid for in premium
delta -> how much to hedge your position to be indifferent to small moves
      -> allows us to remove risk we're not being paid to take
      -> isolate the risks we do want

gamma: change in delta as a function of the underlying price
    basically refers to how much the "more than you should" and "less than you should" are expressed
    deep OTM options have no gamma, since the underlying barely affects the option's value
    deep ITM options, ie where delta approaches 1, also have no gamma, since the option just behaves like 100 shares of underlying
    concentrated ATM -> most desirable options -> where the liquidity and volume are since everyone piles into there

    as IV increases, gamma of options ATM reduces, and gamma at either extremes of OTM and ITM(where delta approaches 0 and 1 respectively) increases


theta: change in option value as function of time
    both OTM and ITM options have little theta, ie are less affected by time;
    for OTM, the option value is basically nonexistent.
    for deep ITM, the option behaves almost exactly like the stock, for which the underlying is unaffected by time directly
    again, concentrated ATM

    note: gamma == theta

the big one
vega: the change in option price as a function of change in volatility
    not observable directly, it is only real in the context of a model
    options are primarily about trading vega
    buy options, hedged, plenty of time value -> PnL purely defined by vega
    vega is model dependent -> very difficult to pinpoint exact exposure



Potential catalysts:
    Analyst re-ratings
        - after a stock drops on news only tangentially related to the stock itself (e.g. sector-wide news)
    Earnings reports
        - almost always a short vol play here 

    Random news (CEO dying or another TSLA car crash)
        - not reliably actionable