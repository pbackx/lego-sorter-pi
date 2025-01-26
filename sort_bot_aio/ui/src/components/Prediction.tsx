import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { useWebSocketContext } from "./WebSocketContext";

export default function Prediction() {
    const [lastPrediction, setLastPrediction] = useState("none")
    const [lastPredictionImage, setLastPredictionImage] = useState<string|undefined>(undefined)
    const { lastJsonMessage } = useWebSocketContext()

    useEffect(() => {
        if (lastJsonMessage?.prediction) {
            setLastPrediction(lastJsonMessage.prediction)
            setLastPredictionImage(lastJsonMessage.prediction_url)
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
            {lastPredictionImage && 
                <img src={lastPredictionImage} width="100" height="100" />
            }
        </CardContent>
    </Card>
}