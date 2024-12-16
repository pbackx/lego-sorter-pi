import { useEffect, useRef } from "react"
import useWebSocket from "react-use-websocket"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"

function Camera() {
    const canvasRef = useRef<HTMLCanvasElement|null>(null)
    const {lastMessage} = useWebSocket('ws://localhost:8000/stream')

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
        if (lastMessage) {
            const blob = lastMessage.data
            const img = new Image()
            img.src = URL.createObjectURL(blob)
            img.onload = () => {
                context.drawImage(img, 0, 0, canvas.width, canvas.height)
                URL.revokeObjectURL(img.src)
            }
        }

    }, [canvasRef, lastMessage])

    return <Card>
        <CardHeader>
            <CardTitle>
                Camera view
            </CardTitle>
        </CardHeader>
        <CardContent>
            <canvas ref={canvasRef} width="640" height="480"></canvas>
        </CardContent>
    </Card>
}

export default Camera