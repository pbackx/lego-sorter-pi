import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { useWebSocketContext } from "./WebSocketContext";

export default function Prediction() {
    const [lastPrediction, setLastPrediction] = useState("none")
    const { lastJsonMessage } = useWebSocketContext()

    useEffect(() => {
        if (lastJsonMessage?.prediction) {
            setLastPrediction(lastJsonMessage.prediction)
        }
    }, [lastJsonMessage])

    return <Card>
        <CardHeader>
            <CardTitle>
                Prediction
            </CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-2">
            <p>Last prediction: {lastPrediction}</p>
        </CardContent>
    </Card>
}