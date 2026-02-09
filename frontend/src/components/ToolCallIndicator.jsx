/**
 * ToolCallIndicator Component
 * Hiển thị trạng thái khi Agent đang gọi tools
 */
import React from 'react';
import { Wrench, Loader2 } from 'lucide-react';
import './ToolCallIndicator.css';

export default function ToolCallIndicator({ toolName, arguments: args, result }) {
    return (
        <div className="tool-call-indicator animate-fade-in">
            <div className="tool-call-header">
                <Wrench size={16} className="tool-icon" />
                <span className="tool-name">Đang sử dụng công cụ: {toolName}</span>
                {!result && <Loader2 size={16} className="animate-spin" />}
            </div>

            {args && (
                <div className="tool-arguments">
                    <div className="args-label">Tham số:</div>
                    <pre className="args-content">
                        {JSON.stringify(args, null, 2)}
                    </pre>
                </div>
            )}

            {result && (
                <div className="tool-result">
                    <div className="result-label">Kết quả:</div>
                    <pre className="result-content">
                        {JSON.stringify(result, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
}
