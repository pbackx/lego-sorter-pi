import './App.css'
import BrickDetector from './components/BrickDetector';
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
          <BrickDetector />
        </div>
        <div>
          <Controls />
        </div>
      </div>
    </WebSocketProvider>
  )
}

export default App
