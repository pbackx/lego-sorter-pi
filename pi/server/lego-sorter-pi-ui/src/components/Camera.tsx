import { useEffect, useRef, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import {Eye, EyeOff} from "lucide-react"
import { useWebSocketContext } from "./WebSocketContext"

function Camera() {
    const canvasRef = useRef<HTMLCanvasElement|null>(null)
    const [isEnabled, setEnabled] = useState(false)
    const {lastJsonMessage, sendJsonMessage} = useWebSocketContext()

    useEffect(() => {
        if (!canvasRef) {
            return
        }
        const canvas = canvasRef.current
        if (!canvas) {
            return
        }
        const context = canvas.getContext('2d')
        if (!context) {
            return
        }
        if (lastJsonMessage) {
            if (lastJsonMessage.image) {
                const blob = new Blob([Uint8Array.from(atob(lastJsonMessage.image), (c) => c.charCodeAt(0))])
                const img = new Image()
                img.src = URL.createObjectURL(blob)
                img.onload = () => {
                    context.drawImage(img, 0, 0, canvas.width, canvas.height)
                    URL.revokeObjectURL(img.src)
                }
            }
        }

    }, [canvasRef, lastJsonMessage])

    function toggleCamera(newState: boolean) {
        setEnabled(newState)
        sendJsonMessage({
            streamCamera: newState
        })
    }

    return <Card>
        <CardHeader>
            <CardTitle>
                Camera view
                {isEnabled ? 
                    <Eye className="inline ml-2" onClick={() => toggleCamera(false)} /> : 
                    <EyeOff className="inline ml-2" onClick={() => toggleCamera(true)} />
                }
            </CardTitle>
        </CardHeader>
        <CardContent>
            <canvas ref={canvasRef} width="640" height="480"></canvas>
        </CardContent>
    </Card>
}

export default Camera