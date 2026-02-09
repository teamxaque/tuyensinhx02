/**
 * MessageList Component
 * Hiển thị danh sách messages với Markdown rendering
 */
import React, { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { User, Bot } from 'lucide-react';
import ToolCallIndicator from './ToolCallIndicator';
import './MessageList.css';

export default function MessageList({ messages, toolCalls }) {
    const messagesEndRef = useRef(null);

    // Auto-scroll to bottom khi có message mới
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, toolCalls]);

    return (
        <div className="message-list">
            {messages.map((msg, index) => (
                <div
                    key={index}
                    className={`message ${msg.role} animate-fade-in`}
                >
                    <div className="message-avatar">
                        {msg.role === 'user' ? (
                            <User size={20} />
                        ) : (
                            <Bot size={20} />
                        )}
                    </div>
                    <div className="message-content">
                        <div className="message-role">
                            {msg.role === 'user' ? 'Bạn' : 'AI Assistant'}
                        </div>
                        <div className="message-text markdown-content">
                            <ReactMarkdown
                                components={{
                                    code({ node, inline, className, children, ...props }) {
                                        const match = /language-(\w+)/.exec(className || '');
                                        return !inline && match ? (
                                            <SyntaxHighlighter
                                                style={vscDarkPlus}
                                                language={match[1]}
                                                PreTag="div"
                                                {...props}
                                            >
                                                {String(children).replace(/\n$/, '')}
                                            </SyntaxHighlighter>
                                        ) : (
                                            <code className={className} {...props}>
                                                {children}
                                            </code>
                                        );
                                    },
                                }}
                            >
                                {msg.content}
                            </ReactMarkdown>
                        </div>
                    </div>
                </div>
            ))}

            {/* Hiển thị tool calls đang thực thi */}
            {toolCalls.map((tool, index) => (
                <div key={`tool-${index}`} className="message assistant">
                    <div className="message-avatar">
                        <Bot size={20} />
                    </div>
                    <div className="message-content">
                        <ToolCallIndicator
                            toolName={tool.name}
                            arguments={tool.arguments}
                            result={tool.result}
                        />
                    </div>
                </div>
            ))}

            <div ref={messagesEndRef} />
        </div>
    );
}
