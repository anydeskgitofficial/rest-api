# AnyDesk API  
A Python module which allows you to easily communicate with the [AnyDesk](https://anydesk.com) API.

## Example
```python
import anydesk
api = anydesk.API("YOUR LICENSE ID", "YOUR API KEY")
print(api.sysinfo().name)
```

You can find more examples in `doc/examples`. To run these examples you need to create the file `doc/examples/auth.cfg` and add the following (replace `YOUR LICENSE ID` with your license ID and `YOUR API KEY` with your API key):

```
[Auth]
license=YOUR LICENSE ID
key=YOUR API KEY
```

## Documentation
You can access the documentation for the AnyDesk API by typing the following into your Python REPL:

```python
import anydesk
help(anydesk.API)
```

There are also various examples in `doc/examples`.

## License
See LICENSE.md
