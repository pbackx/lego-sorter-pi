import { createContext, useContext, ReactNode } from 'react';
import useWebSocket from 'react-use-websocket';

export interface WebSocketResponse {
    image?: string
}

export interface WebSocketRequest {
    streamCamera?: boolean
}

interface WebSocketContextType {
  lastJsonMessage: WebSocketResponse | null;
  sendJsonMessage: (message: WebSocketRequest) => void;
}

const WebSocketContext = createContext<WebSocketContextType | null>(null);

export function WebSocketProvider({ children }: { children: ReactNode }) {
    const { lastJsonMessage, sendJsonMessage } = useWebSocket<WebSocketResponse>('ws://localhost:8000/stream', {
        shouldReconnect: () => true
    });

  return (
    <WebSocketContext.Provider value={{ lastJsonMessage, sendJsonMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
}

export function useWebSocketContext() {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocketContext must be used within a WebSocketProvider');
  }
  return context;
}