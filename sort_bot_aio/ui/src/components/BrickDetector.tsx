import { useEffect, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { useWebSocketContext } from "./WebSocketContext"

export default function BrickDetector() {
    const refCanvasRef = useRef<HTMLCanvasElement|null>(null)
    const threshCanvasRef = useRef<HTMLCanvasElement|null>(null)
    const {lastJsonMessage} = useWebSocketContext()

    useEffect(() => {
        if (!refCanvasRef || !threshCanvasRef) {
            return
        }
        if (lastJsonMessage) {
            let blob: Blob|null = null
            let canvas: HTMLCanvasElement|null = null

            if (lastJsonMessage.referenceImage) {
                blob = new Blob([Uint8Array.from(atob(lastJsonMessage.referenceImage), (c) => c.charCodeAt(0))])
                canvas = refCanvasRef.current
            } else if (lastJsonMessage.thresholdImage) {
                blob = new Blob([Uint8Array.from(atob(lastJsonMessage.thresholdImage), (c) => c.charCodeAt(0))])
                canvas = threshCanvasRef.current
            }

            if (blob && canvas) {
                const context = canvas.getContext('2d')
                if (!context) {
                    return
                }        
                const img = new Image()
                img.src = URL.createObjectURL(blob)
                img.onload = () => {
                    context.drawImage(img, 0, 0, canvas.width, canvas.height)
                    URL.revokeObjectURL(img.src)
                }
            }
        }

    }, [refCanvasRef, lastJsonMessage])

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
                <canvas ref={refCanvasRef} width="640" height="340"></canvas>
            </div>
            <div className="w-full overflow-scroll">
                <canvas ref={threshCanvasRef} width="640" height="340"></canvas>
            </div>
        </CardContent>
    </Card>
}