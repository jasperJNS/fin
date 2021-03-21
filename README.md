Exploratory data analysis of the financial world.



Ideas:
    difficulty ribbon, inversion of 3-mo and 12-mo MA's of production costs leading to increased future scarcity/price (first used with mining data for Bitcoin)
    by inversion we mean that the 3-mo fell below the 12-mo with the 6-mo MA in between (essentially signaling a recent shift in production levels)


Sections:
    Options chain analysis
    10-k sentiment analysis
    GUI compilation of data when searching a ticker, ie newsfeed + 10-k sentiment + options data



NOPE_MAD:
    0. Caveat: need historical options data for this, only available if I build the thinkorswim parser, or pay the ORATS premium, although we could build a bandaid solution by running a cronjob and just collecting the daily data manually
    
    1. Calculate today's NOPE score (this can be done end of day or intraday, with the true value being EOD of course)

    2. Calculate the end of day NOPE scores on the ticker for the previous 30 trading days

    3. Compute the median of the previous 30 trading days' NOPEs

    4. From the median, find the 30 days' median absolute deviation

    5. Find today's deviation as compared to the MAD calculated by: 
    
    [(today's NOPE) - (median NOPE of last 30 days)] / (median absolute deviation of last 30 days)

    
    This is usually reported as sigma (σ), and has a few interesting properties:

    The mean of NOPE_MAD for any ticker is almost exactly 0.

    [Lily's Speculation's Speculation] NOPE_MAD acts like a spring, and has a tendency to reverse direction as a function of its magnitude. No proof on this yet, but exploring it!


    So the last section was a lot of words and theory, and a lot of what I'm mentioning here is empirically derived (aka I've tested it out, versus just blabbered).

    In general, the following holds true:

    3 sigma NOPE_MAD tends to be "the threshold": For very low NOPE_MAD magnitudes (+- 1 sigma), it's effectively just noise, and directionality prediction is low, if not non-existent. It's not exactly like 3 sigma is a play and 2.9 sigma is not a play; NOPE_MAD accuracy increases as NOPE_MAD magnitude (either positive or negative) increases.

    NOPE_MAD is only useful on highly optioned tickers: In general, I introduce another parameter for sifting through "candidate" ERs to play: option volume * 100/share volume. When this ends up over let's say 0.4, NOPE_MAD provides a fairly good window into predicting earnings behavior.

    NOPE_MAD only predicts during the after-market/pre-market session: I also have no idea if this is true, but my hunch is that next day behavior is mostly random and driven by market movement versus earnings behavior. NOPE_MAD for now only predicts direction of price movements right between the release of the ER report (AH or PM) and the ending of that market session. This is why in general I recommend playing shares, not options for ER (since you can sell during the AH/PM).

    NOPE_MAD only predicts direction of price movement: This isn't exactly true, but it's all I feel comfortable stating given the data I have. On observation of ~2700 data points of ER-ticker events since Mar 2019 (SPY 500), I only so far feel comfortable predicting whether stock price goes up (>0 percent difference) or down (<0 price difference). This is +1 for why I usually play with shares.

    Some statistics:

    #0) As a baseline/null hypothesis, after ER on the SPY500 since Mar 2019, 50-51% price movements in the AH/PM are positive (>0) and ~46-47% are negative (<0).

    #1) For NOPE_MAD >= +3 sigma, roughly 68% of price movements are positive after earnings.

    #2) For NOPE_MAD <= -3 sigma, roughly 29% of price movements are positive after earnings.

    #3) When using a logistic model of only data including NOPE_MAD >= +3 sigma or NOPE_MAD <= -3 sigma, and option/share vol >= 0.4 (around 25% of all ERs observed), I was able to achieve 78% predictive accuracy on direction.