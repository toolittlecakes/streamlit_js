# streamlit-js

Streamlit component that allows you to run JS code with both blocking and non-blocking modes.

The package is based on the [streamlit-javascript](https://github.com/thunderbug1/streamlit-javascript).

The main difference is that the package above doesn't allow distinguishing if the JS code is executed or not in all situations (e.g. when the code returns `null`).

It's important because Streamlit components works in asyncronous mode and cannot return value immediately. They need several reruns to get the value. So, it's important to know when the code is finished and when it's not.

This package solves this issue by returning `[]` when the code is not finished and `[None]` when the code is finished and returns `null`. Also, it allows to block the script until the JS code is executed and app is refreshed.

## Installation instructions

```sh
pip install streamlit-js
```

## Usage instructions

```python
import streamlit as st

from streamlit_js import st_js, st_js_blocking

value = st_js(code='return null;')
if not value:
    st.write('Loading...')
    st.stop()
st.write(value) # [None]
st.write(value[0] # None

# This will block the script until the js code is executed
value = st_js_blocking(code='return null;')
st.write(value) # None
```
