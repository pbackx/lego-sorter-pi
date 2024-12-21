import {z} from 'zod'
import WebSocketRequest from './WebSocketRequest'
import WebSocketResponse from './WebSocketResponse'

export type WebSocketRequestType = z.infer<typeof WebSocketRequest>
export type WebSocketResponseType = z.infer<typeof WebSocketResponse>