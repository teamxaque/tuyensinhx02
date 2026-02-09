/**
 * MessageInput Component
 * Input box để nhập tin nhắn
 */
import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import './MessageInput.css';

export default function MessageInput({ onSend, disabled }) {
    const [message, setMessage] = useState('');
    const textareaRef = useRef(null);

    // Auto-resize textarea
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
        }
    }, [message]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (message.trim() && !disabled) {
            onSend(message);
            setMessage('');
        }
    };

    const handleKeyDown = (e) => {
        // Submit on Enter (without Shift)
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <form className="message-input-container" onSubmit={handleSubmit}>
            <div className="input-wrapper glass-effect">
                <textarea
                    ref={textareaRef}
                    className="message-textarea"
                    placeholder="Nhập tin nhắn của bạn... (Enter để gửi, Shift+Enter để xuống dòng)"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={disabled}
                    rows={1}
                />
                <button
                    type="submit"
                    className="send-button"
                    disabled={disabled || !message.trim()}
                    title="Gửi tin nhắn"
                >
                    <Send size={20} />
                </button>
            </div>
        </form>
    );
}
