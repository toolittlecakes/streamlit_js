import os

import streamlit as st
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_js",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_js", path=build_dir)


def st_js(code: str, key=None):
    """
    This is a non-blocking streamlit component that executes JavaScript code.

    Parameters
    ----------
    code: str
        The code to be executed by the component.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    list
        [] if the code is still running.
        [<result>] if the code is finished.
        {"error": <error>} if the code throws an error.
        Where <result> is the value of executed code. It has to be serializable.
        It's already deserialized by Streamlit into Python object.
    """
    return _component_func(code=code, key=key, default=[], height=0)


def st_js_blocking(code, key=None):
    """
    This is a blocking version of streamlit_js.
    It will block the script until the component is finished and result is returned.
    In case of an error, it will raise an exception.
    Then it Streamlit will rerun the script as usual when something changes.
    Usually it finishes in one rerun, but it's not guaranteed by this function due to Streamlit's nature.

    Parameters
    ----------
    code: str
        The code to be executed by the component.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    Unknown
        The value of executed code. It has to be serializable.
        It's already deserialized by Streamlit into Python object.
    """

    result = st_js(code=code, key=key)
    if not result:
        st.stop()
    if isinstance(result, dict):
        assert "error" in result
        raise Exception(result["error"])

    return result[0]


if not _RELEASE:
    # This is a simple example of how to use the component.
    # You can run this script with `streamlit run streamlit_js/__init__.py`
    # and see the result in your browser.

    st.title("streamlit_js example")

    st.write("This is a non-blocking version of the component.")
    st.write("It will not block the script until the component is finished.")
    st.write("It will rerun the script as usual when something changes.")

    # wait 1 second and return "Hello, Streamlit!"
    code = """
    wait = ms => new Promise(resolve => setTimeout(resolve, ms));
    await wait(100);
    return "Hello, Streamlit!";
    """
    result = st_js(code)
    if "first_result" not in st.session_state:
        st.session_state.first_result = result
    st.write("**first_result:**")
    st.write(st.session_state.first_result)
    st.write("**final_result:**")
    st.write(result)

    st.write("---")
    st.write("This is a blocking version of the component.")
    st.write("It will block the script until the component is finished.")
    st.write("Then it Streamlit will rerun the script as usual when something changes.")

    result = st_js_blocking(code, key="blocking")
    if "first_blocking_result" not in st.session_state:
        st.session_state.first_blocking_result = result

    st.write("**first_result:**")
    st.write(st.session_state.first_blocking_result)
    st.write("**final_result:**")
    st.write(result)
