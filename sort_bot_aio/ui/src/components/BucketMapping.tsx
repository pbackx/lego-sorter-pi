import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { useWebSocketContext } from "./WebSocketContext";
import Request from "../model/WebSocketRequest"
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

const bucketMappingSchema = Request.shape.bucketMapping

export default function BucketMapping() {
    
    const form = useForm<z.infer<typeof bucketMappingSchema> & {}>({
        resolver: zodResolver(bucketMappingSchema),
        defaultValues: {
            default: 1,
            mapping: {
                "0": ["2780", "4459", "3673"]
            }
        }
    })

    function onSubmit(values: z.infer<typeof bucketMappingSchema>) {
        console.log(values)
    }

    //TODO finish form according to ShadCN explanation: https://ui.shadcn.com/docs/components/form

    return <Card>
        <CardHeader>
            <CardTitle>
                Bucket Mapping
            </CardTitle>
            <CardDescription>
                Specify what bricks will go to what buckets.
            </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
            </div>
        </CardContent>
    </Card>
}