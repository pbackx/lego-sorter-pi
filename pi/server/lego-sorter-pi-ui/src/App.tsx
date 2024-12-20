import './App.css'
import Camera from './components/Camera';
import { Button } from './components/ui/button';
import { WebSocketProvider } from './components/WebSocketContext';

function App() {
  return (
    <WebSocketProvider>
      <div>
        <Camera />
      </div>
      <div>
        <h1>Controls</h1>
        <Button className='bg-green-500'>Start</Button>
      </div>
    </WebSocketProvider>
  )
}

export default App
