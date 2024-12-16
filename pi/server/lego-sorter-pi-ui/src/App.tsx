import './App.css'
import Camera from './components/Camera';
import { Button } from './components/ui/button';

function App() {
  return (
    <>
      <div>
        <Camera />
      </div>
      <div>
        <h1>Controls</h1>
        <Button className='bg-green-500'>Start</Button>
      </div>
    </>
  )
}

export default App
