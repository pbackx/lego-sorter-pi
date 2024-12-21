import './App.css'
import Camera from './components/Camera';
import Controls from './components/Controls'
import { WebSocketProvider } from './components/WebSocketContext';

function App() {
  return (
    <WebSocketProvider>
      <div className='grid grid-flow-row grid-cols-2 grid-rows-2 gap-2'>
        <div>
          <Camera />
        </div>
        <div>
          <h1>TODO filtered view</h1>
        </div>
        <div>
          <Controls />
        </div>
      </div>
    </WebSocketProvider>
  )
}

export default App
