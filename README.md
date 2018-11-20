# picklecache
python decorator for caching function results to disk via pickle

    Example:
        >>> @picklecache
        ... def fib(n):
        ...     def fibr(n):
        ...         if n == 0 or n == 1:
        ...             return 1
        ...         else:
        ...             return fibr(n-1) + fibr(n-2)
        ...     return fibr(n)
        ... 
    This should take a few seconds
        >>> fib(36)
        24157817
    This should be miliseconds
        >>> fib(36)
        24157817
    Remember to clear the cache
        >>> fib.clearcache(36)

### Note:  
This is not a good way to calculate fibonacci numbers.
I made this so I could do stuff like below, but the fib 
example runs in doctest.

    Example:
        >>> @picklecache
        ... def loading_and_preprocessing_pipline(where_to_get_raw_data):
        ...     # do a bunch of work which takes a long time.
        ...     # eventually output data in the representaion then I want
        ...     # for modeling.
        ...     
        ...     return Data(whatever)
        ...  
    
