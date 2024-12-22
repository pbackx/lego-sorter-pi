import { useEffect, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { useWebSocketContext } from "./WebSocketContext"

export default function BrickDetector() {
    const canvasRef = useRef<HTMLCanvasElement|null>(null)
    const {lastJsonMessage} = useWebSocketContext()

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
            if (lastJsonMessage.referenceImage) {
                const blob = new Blob([Uint8Array.from(atob(lastJsonMessage.referenceImage), (c) => c.charCodeAt(0))])
                const img = new Image()
                img.src = URL.createObjectURL(blob)
                img.onload = () => {
                    context.drawImage(img, 0, 0, canvas.width, canvas.height)
                    URL.revokeObjectURL(img.src)
                }
            }
        }

    }, [canvasRef, lastJsonMessage])

    return <Card>
        <CardHeader>
            <CardTitle>
                Brick Detector
            </CardTitle>
            <CardDescription>
                Some views of how the Brick detector is working
            </CardDescription>
        </CardHeader>
        <CardContent>
            <div className="w-full overflow-scroll">
                <canvas ref={canvasRef} width="640" height="340"></canvas>
            </div>
        </CardContent>
    </Card>
}