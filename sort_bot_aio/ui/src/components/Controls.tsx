import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { useWebSocketContext } from "./WebSocketContext";

export default function Controls() {
    const {sendJsonMessage} = useWebSocketContext()

    function setBucket(num: number) {
        console.log(`Setting bucket ${num}`)
        sendJsonMessage({
            bucket: num
        })
    }

    return <Card>
    <CardHeader>
        <CardTitle>
            Controls
        </CardTitle>
    </CardHeader>
    <CardContent className="flex flex-col gap-2">
        <Button className='bg-green-500'>Start</Button>
        <h1>Bucket</h1>
        <div className="flex flexrow gap-1">

            {[...Array(6)].map((_, i) => (
                <Button key={i + 1} onClick={() => setBucket(i + 1)}>{i + 1}</Button>
            ))}
            
        </div>
        <Button 
            onClick={() => sendJsonMessage({clearBelt: true})}>
            Clear belt
        </Button>
        <Button 
            onClick={() => sendJsonMessage({makeReferenceImage: true})}>
            Take new reference image
        </Button>
    </CardContent>
</Card>
}