import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { useWebSocketContext } from "./WebSocketContext"
import Request from "../model/WebSocketRequest"
import { z } from "zod"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormField, FormLabel, FormItem, FormControl, FormDescription, FormMessage } from "./ui/form"
import { Button } from "./ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "./ui/table"
import { Input } from "./ui/input"

const bucketMappingSchema = Request.shape.bucketMapping

export default function BucketMapping() {
    const {sendJsonMessage} = useWebSocketContext()
    
    const form = useForm<z.infer<typeof bucketMappingSchema> & {}>({
        resolver: zodResolver(bucketMappingSchema),
        defaultValues: {
            default: 1,
            mapping: {
                "0": ["2780", "4459", "3673"], 
                "1": [],
                "2": [],
                "3": [],
                "4": [],
                "5": ["3023"]
            }
        }
    })

    function onSubmit(values: z.infer<typeof bucketMappingSchema>) {
        sendJsonMessage({
            bucketMapping: values
        })
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
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                    <FormField
                        control={form.control}
                        name="default"
                        render={({field}) => (
                        <FormItem>
                            <FormLabel>Default bucket</FormLabel>
                            <Select 
                                onValueChange={(value) => field.onChange(parseInt(value))} 
                                defaultValue={field.value.toString()}
                            >
                                <FormControl>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select bucket" />
                                    </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                {[...Array(6)].map((_, i) => (
                                    <SelectItem key={i} value={i.toString()}>{i}</SelectItem>
                                ))}
                                </SelectContent>
                            </Select>
                            <FormDescription>
                                The bucket in which to sort all bricks not assigned to a bucket
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                        )}
                    />
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Bucket #</TableHead>
                                <TableHead>Brick types</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {[...Array(6)].map((_, i) => (
                                <TableRow key={i}>
                                    <TableCell>{i.toString()}</TableCell>
                                    <TableCell>
                                        <FormField
                                            control={form.control}
                                            name={`mapping.${i.toString()}`}
                                            render={({field}) => (
                                                <FormItem>
                                                    <FormControl>
                                                        <Input
                                                            onChange={(value) => {
                                                                const values = value.target.value.split(',')
                                                                field.onChange(values)
                                                            }}
                                                            defaultValue={field?.value?.toString()}
                                                        />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    <Button type="submit">Update</Button>
                </form>
            </Form>
    </CardContent>
    </Card>
}