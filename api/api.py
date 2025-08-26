from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from datetime import datetime
import uuid

from models import ChatMessage, ChatResponse
from websocket_config import ConnectionManager

from chat import afrohistorian, afrohistorian_stream

app = FastAPI()

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",], # TODO: Update with frontend url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

# Http endpoint for single queries
@app.post("/ask", response_model=ChatResponse)
async def ask_afrohistorian(message: ChatMessage):
    """Traditional HTTP endpoint for single queries"""
    try:
        answer = afrohistorian(text=message.query)

        return ChatResponse(
            message="Success",
            response=answer.get("response"),
            conversation_id=message.conversation_id or str(uuid.uuid4()),
            timestamp=datetime.now(),
            sources=[],  # Extract sources from your RAG response if available
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat/{user_id}")
async def websocket_chat_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time chat with streaming responses"""
    await manager.connect(websocket, user_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            query = message_data.get("query", "")
            conversation_id = message_data.get("conversation_id", str(uuid.uuid4()))

            if not query.strip():
                await manager.send_personal_message(
                    {"type": "error", "message": "Query cannot be empty"}, user_id
                )
                continue

            # Send typing indicator
            await manager.send_personal_message(
                {
                    "type": "typing",
                    "message": "Afrohistorian is thinking...",
                    "conversation_id": conversation_id,
                },
                user_id,
            )

            try:
                # Process the query
                answer = afrohistorian(text=query)

                # Send the response
                await manager.send_personal_message(
                    {
                        "type": "response",
                        "message": "Success",
                        "response": answer.get("response"),
                        "conversation_id": conversation_id,
                        "timestamp": datetime.now().isoformat(),
                        "sources": [],  # TODO:Add sources extraction logic
                    },
                    user_id,
                )

            except Exception as e:
                await manager.send_personal_message(
                    {
                        "type": "error",
                        "message": f"Error processing query: {str(e)}",
                        "conversation_id": conversation_id,
                    },
                    user_id,
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        print(f"User {user_id} disconnected")


# STREAMING VERSION - For better UX with slow LLM responses
@app.websocket("/ws/chat-stream/{user_id}")
async def websocket_streaming_chat(websocket: WebSocket, user_id: str):
    """WebSocket with streaming responses for better UX"""
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            query = message_data.get("query", "")
            conversation_id = message_data.get("conversation_id", str(uuid.uuid4()))

            if not query.strip():
                continue

            # Send start of response
            await manager.send_personal_message(
                {"type": "stream_start", "conversation_id": conversation_id}, user_id
            )

            try:
                # Use the streaming generator
                async def stream_chunks():
                    for response in afrohistorian_stream(query):
                        yield response

                async for chunk in stream_chunks():
                    await manager.send_personal_message(
                        {
                            "type": "stream_chunk",
                            "text": chunk.get("response", ""),
                            "conversation_id": conversation_id,
                            "is_final": False,  # We'll send a final message after the stream
                        },
                        user_id,
                    )
                    await asyncio.sleep(0.05)  # Small delay for streaming effect

                # Send final response with sources
                await manager.send_personal_message(
                    {
                        "type": "stream_end",
                        "conversation_id": conversation_id,
                        "sources": [],  # Add your sources here if available
                        "timestamp": datetime.now().isoformat(),
                    },
                    user_id,
                )

            except Exception as e:
                await manager.send_personal_message(
                    {
                        "type": "error",
                        "message": f"Error: {str(e)}",
                        "conversation_id": conversation_id,
                    },
                    user_id,
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


# Health check endpoint
@app.get("/")
async def read_root():
    return {"message": "Afrohistorian API with WebSocket support"}


# Get active connections (for admin monitoring)
@app.get("/admin/connections")
async def get_active_connections():
    return {
        "active_connections": len(manager.active_connections),
        "user_connections": list(manager.user_connections.keys())
    }