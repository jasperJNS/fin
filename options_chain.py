def get_options_chain(session, params: dict):
    '''
    Arguments:
        ----
        symbol (str, optional): A single symbol to return option chains for

        contract_type (str, optional): Can be `call`, `put`, or `all`. Defaults to `all`.

        strike_count (int, optional): The number of strikes to return above and 
            below the at-the-money price. Defaults to None.

        include_quotes (bool, optional): Include quotes for options in the option chain. 
            Can be `True` or `False`. Defaults to False.

        strategy (str, optional): Passing a value returns a Strategy Chain. Possible values are 
            `single`, `analytical` (allows use of the volatility, underlyingPrice, interestRate, 
            and daysToExpiration params to calculate theoretical values), `covered`, `vertical`, 
            `calendar`, `strangle`, `straddle`, `butterfly`, `condor`, `diagonal`, `collar`, 
            or `roll`. Defaults to `single`.

        interval (str, optional): Strike interval for spread strategy 
            chains (see `strategy` param). Defaults to None.

        strike (float, optional): Provide a strike price to return options only at that
            strike price. Defaults to None.

        opt_range (str, optional): Returns options for the given range. 
            Possible values are: [(`itm`, In-the-money), (`ntm`: Near-the-money),
            (`otm`: Out-of-the-money), (`sak`: Strikes Above Market), (`sbk`: Strikes Below Market)
            (`snk`: Strikes Near Market), (`all`: All Strikes)
            Defaults to `all`.

        from_date (Union[str, datetime], optional): Only return expirations after this date. 
            For strategies, expiration refers to the nearest term expiration in the strategy. 
            Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.Can either be
            a string or `datetime` object.
            Defaults to None.

        to_date (Union[str, datetime], optional): Only return expirations before this date. 
            For strategies, expiration refers to the nearest term expiration in the strategy. 
            Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz. Can either be
            a string or `datetime` object.
            Defaults to None.

        volatility (str, optional): Volatility to use in calculations. Applies only to `analytical` 
            strategy chains (see strategy param). Defaults to None.

        underlying_price (str, optional): Underlying price to use in calculations. Applies only to 
            `analytical` strategy chains (see strategy param). Defaults to None.

        interest_rate (str, optional): Interest rate to use in calculations. Applies only to 
            `analytical` strategy chains (see strategy param). Defaults to None.

        days_to_expiration (str, optional): Days to expiration to use in calculations. Applies 
            only to `analytical` strategy chains (see strategy param). Defaults to None.

        exp_month (str, optional): Return only options expiring in the specified month. Month 
            is given in the three character format. Example: `jan` Defaults to `all`. 
            
        option_type (str, optional): Type of contracts to return. Possible values are:
            [(`s`: Standard contracts), (`ns`: Non-standard contracts), (`all`: All contracts)]
            Defaults to `all`.

    '''

    option_chains = session.get_options_chain(option_chain=params)
    return option_chains
