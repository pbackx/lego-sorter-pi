import { useEffect, useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { useWebSocketContext } from "./WebSocketContext";

export default function Controls() {
    const [machineRunning, setMachineRunning] = useState(false)
    const {sendJsonMessage,lastJsonMessage} = useWebSocketContext()

    function setBucket(num: number) {
        console.log(`Setting bucket ${num}`)
        sendJsonMessage({
            bucket: num
        })
    }

    useEffect(() => {
        if (lastJsonMessage) {
            setMachineRunning(lastJsonMessage.machineRunning)
        }
    }, [lastJsonMessage])

    return <Card>
        <CardHeader>
            <CardTitle>
                Controls
            </CardTitle>
            <CardDescription>
                Machine is {machineRunning ? "running." : "stopped."}
            </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-2">
            <div className="flex flexrow gap-1">
                <Button
                    className='bg-green-500'
                    onClick={() => sendJsonMessage({ start: true })}>
                    Start
                </Button>
                <Button
                    className='bg-red-500'
                    onClick={() => sendJsonMessage({ stop: true })}>
                    Stop
                </Button>
            </div>
            <h1>Bucket</h1>
            <div className="flex flexrow gap-1">

                {[...Array(6)].map((_, i) => (
                    <Button key={i} onClick={() => setBucket(i)}>{i}</Button>
                ))}

            </div>
            <div className="flex flexrow gap-1">
                <Button
                    onClick={() => sendJsonMessage({ clearBelt: true })}>
                    Clear belt
                </Button>
            </div>
            <div className="flex flexrow gap-1">
                <Button
                    onClick={() => sendJsonMessage({ makeReferenceImage: true })}>
                    Take new reference image
                </Button>
                <Button
                    onClick={() => sendJsonMessage({ nextBrick: true })}>
                    Move to next brick
                </Button>
                <Button
                    onClick={() => sendJsonMessage({ predictOne: true })}>
                    Predict one brick
                </Button>
            </div>
        </CardContent>
    </Card>
}