import './App.css'
import BrickDetector from './components/BrickDetector';
import BucketMapping from './components/BucketMapping';
import Camera from './components/Camera';
import Controls from './components/Controls'
import Prediction from './components/Prediction';
import { WebSocketProvider } from './components/WebSocketContext';

function App() {
  return (
    <WebSocketProvider>
      <div className='flex flex-row gap-4'>
        <div className='flex flex-col gap-4'>
          <div>
            <Camera />
          </div>
          <div>
            <Controls />
          </div>
          <div>
            <BucketMapping />
          </div>
        </div>
        <div className='flex flex-col gap-4'>
          <div>
            <BrickDetector />
          </div>
          <div>
            <Prediction />
          </div>
        </div>
      </div>
    </WebSocketProvider>
  )
}

export default App
