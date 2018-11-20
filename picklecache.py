import glob
import itertools
import pickle
import string
import os


def picklecache(func):
    ''' 
    decorator which caches results to disk as a pickle file 
    
    args:
        func (Callable): function or callable who's results should be cached

    return:
        wrapped callable


    Example:
        >>> from utils.misc import picklecache
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

    '''
    tr = str.maketrans(dict(zip(itertools.chain(string.punctuation, string.whitespace), itertools.repeat(''))))
    
    
    def makename(*args, **kwargs):
        '''
        helper function to create cachefile names
        cache filename is all arguments sorted,
        truncated to 20 characters, and concatanated
        with an extention ending in _picklecache 
        '''
        return ('.'.join(('', (''.join(map(lambda e : str(e)[:20], itertools.chain( args, 
            (kv for kv in sorted(kwargs.items())))))).translate(tr), func.__name__+'_picklecache')))
    
    def clearcache(*args, **kwargs):
        '''
        delete the cached result for these particular arguments
        '''
        cachename = makename(args, kwargs)
        try:
            os.remove(cachename)
            
        except FileNotFoundError:
            pass
        
    
    def clearallcache():
        '''
        delete all chached results for this function
        '''
        for f in glob.iglob(''.join(('.*', func.__name__, '_picklecache'))):
            try:
                os.remove(f)
            except FileNotFoundError:
                pass
            
    
    def wrapper(*args, **kwargs):
        '''
        wrapper which does the actual caching
        '''
        cachename = makename(args, kwargs)
        
        try:
            result = pickle.load(open(cachename, 'rb'))
            
        except FileNotFoundError:
            result = func(*args, **kwargs)
            pickle.dump(result, open(cachename, 'wb'))
        
        return result
    
    # attach clearcache and clearallcache to wrapper 
    wrapper.clearcache = clearcache
    wrapper.clearallcache = clearallcache
    
    return wrapper

