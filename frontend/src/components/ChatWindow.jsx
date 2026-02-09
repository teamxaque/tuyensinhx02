/**
 * ChatWindow Component
 * Container chính cho chat interface
 */
import React, { useState, useEffect } from 'react';
import { MessageSquare, Trash2, Loader2 } from 'lucide-react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { sendChatMessage } from '../utils/sseClient';
import './ChatWindow.css';

export default function ChatWindow() {
    const [messages, setMessages] = useState([]);
    const [sessionId, setSessionId] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [toolCalls, setToolCalls] = useState([]);
    const [currentResponse, setCurrentResponse] = useState('');

    const handleSendMessage = (message) => {
        // Thêm user message vào UI
        setMessages(prev => [...prev, { role: 'user', content: message }]);
        setIsLoading(true);
        setCurrentResponse('');
        setToolCalls([]);

        // Gửi request với SSE
        sendChatMessage(message, sessionId, {
            onMessage: (event) => {
                const { type, content } = event;

                switch (type) {
                    case 'session':
                        // Nhận session_id từ server
                        setSessionId(content.session_id || event.session_id);
                        break;

                    case 'text':
                        // Nhận text chunk
                        setCurrentResponse(prev => prev + content);
                        break;

                    case 'tool_call_start':
                        // Bắt đầu gọi tool
                        setToolCalls(prev => [
                            ...prev,
                            { name: content.name, arguments: null, result: null }
                        ]);
                        break;

                    case 'tool_call':
                        // Tool call với arguments
                        setToolCalls(prev => {
                            const updated = [...prev];
                            const lastIndex = updated.length - 1;
                            if (lastIndex >= 0) {
                                updated[lastIndex] = {
                                    ...updated[lastIndex],
                                    arguments: content.arguments
                                };
                            }
                            return updated;
                        });
                        break;

                    case 'tool_result':
                        // Kết quả từ tool
                        setToolCalls(prev => {
                            const updated = [...prev];
                            const toolIndex = updated.findIndex(
                                t => t.name === content.name && !t.result
                            );
                            if (toolIndex >= 0) {
                                updated[toolIndex] = {
                                    ...updated[toolIndex],
                                    result: content.result
                                };
                            }
                            return updated;
                        });
                        break;

                    case 'done':
                        // Hoàn thành - thêm assistant response vào messages
                        if (currentResponse || content) {
                            setMessages(prev => [
                                ...prev,
                                { role: 'assistant', content: content || currentResponse }
                            ]);
                        }
                        setCurrentResponse('');
                        setToolCalls([]);
                        setIsLoading(false);
                        break;

                    case 'error':
                        // Lỗi
                        console.error('Chat error:', content);
                        setMessages(prev => [
                            ...prev,
                            {
                                role: 'assistant',
                                content: `❌ Lỗi: ${content}`
                            }
                        ]);
                        setIsLoading(false);
                        setToolCalls([]);
                        break;
                }
            },

            onError: (error) => {
                console.error('SSE error:', error);
                setMessages(prev => [
                    ...prev,
                    {
                        role: 'assistant',
                        content: `❌ Lỗi kết nối: ${error.message}`
                    }
                ]);
                setIsLoading(false);
                setToolCalls([]);
            },

            onComplete: () => {
                setIsLoading(false);
            }
        });
    };

    const handleClearChat = () => {
        if (window.confirm('Bạn có chắc muốn xóa toàn bộ lịch sử chat?')) {
            setMessages([]);
            setSessionId(null);
            setToolCalls([]);
            setCurrentResponse('');
        }
    };

    // Hiển thị assistant response đang được stream
    const displayMessages = [...messages];
    if (currentResponse && isLoading) {
        displayMessages.push({
            role: 'assistant',
            content: currentResponse
        });
    }

    return (
        <div className="chat-window">
            {/* Header */}
            <div className="chat-header glass-effect">
                <div className="header-title">
                    <MessageSquare size={24} className="header-icon" />
                    <h1 className="gradient-text">OpenAI Agent Chat</h1>
                </div>
                <button
                    className="clear-button"
                    onClick={handleClearChat}
                    title="Xóa lịch sử chat"
                >
                    <Trash2 size={20} />
                </button>
            </div>

            {/* Messages */}
            <div className="chat-messages">
                {displayMessages.length === 0 ? (
                    <div className="empty-state">
                        <MessageSquare size={64} className="empty-icon" />
                        <h2>Chào mừng đến với OpenAI Agent Chat!</h2>
                        <p>Tôi có thể giúp bạn với:</p>
                        <ul>
                            <li>🌤️ Kiểm tra thời tiết</li>
                            <li>🔍 Tìm kiếm thông tin trong database</li>
                            <li>💬 Trả lời câu hỏi và hỗ trợ</li>
                        </ul>
                        <p className="hint">Hãy bắt đầu bằng cách gửi tin nhắn!</p>
                    </div>
                ) : (
                    <MessageList messages={displayMessages} toolCalls={toolCalls} />
                )}

                {/* Loading indicator */}
                {isLoading && !currentResponse && toolCalls.length === 0 && (
                    <div className="loading-indicator">
                        <Loader2 size={24} className="animate-spin" />
                        <span>AI đang suy nghĩ...</span>
                    </div>
                )}
            </div>

            {/* Input */}
            <MessageInput onSend={handleSendMessage} disabled={isLoading} />
        </div>
    );
}
