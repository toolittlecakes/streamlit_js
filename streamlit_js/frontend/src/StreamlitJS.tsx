import { ReactNode } from "react"
import {
  ComponentProps,
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

interface State {
  result: any
  finished: boolean
}

class StreamlitJS extends StreamlitComponentBase<State> {
  public constructor(props: ComponentProps) {
    super(props)
    this.state = { result: null, finished: false }
    // Streamlit.setFrameHeight(0)
    Streamlit.setComponentReady()
  }

  componentDidMount = async () => {
    // public componentDidMount = () => {
    console.log("componentDidMount")
    if (this.state.finished) {
      return null
    }
    const code = this.props.args["code"]
    const expectResult = this.props.args["expect_result"]

    const evalWithExceptionHandling = async (code: string) => {
      try {
        const AsyncFunction = Object.getPrototypeOf(async function () { }).constructor
        const asyncFunction = new AsyncFunction(code);
        return [await asyncFunction()];
      } catch (error) {
        console.error(error)
        return { error }
      }
    }
    const wrapped_result = await evalWithExceptionHandling(code)

    this.setState(
      _prevState => ({ result: wrapped_result, finished: true }),
      () => {
        if (expectResult) {
          Streamlit.setComponentValue(this.state.result)
        }
      }
    )

    return null
  }

  public render = (): ReactNode => {
    console.log("render")
    return null
  }
}

export default withStreamlitConnection(StreamlitJS)
