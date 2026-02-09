/**
 * SSE Client Utility
 * Xử lý Server-Sent Events streaming từ backend
 */

export class SSEClient {
    constructor(url, options = {}) {
        this.url = url;
        this.options = options;
        this.eventSource = null;
    }

    /**
     * Kết nối và lắng nghe SSE stream
     * @param {Object} callbacks - Object chứa các callback functions
     * @param {Function} callbacks.onMessage - Callback khi nhận message
     * @param {Function} callbacks.onError - Callback khi có lỗi
     * @param {Function} callbacks.onComplete - Callback khi stream kết thúc
     */
    connect(callbacks = {}) {
        const { onMessage, onError, onComplete } = callbacks;

        // Sử dụng fetch với streaming thay vì EventSource
        // vì EventSource không hỗ trợ POST request
        fetch(this.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream',
            },
            body: JSON.stringify(this.options.body || {}),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';

                const readStream = () => {
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            if (onComplete) onComplete();
                            return;
                        }

                        // Decode chunk và thêm vào buffer
                        buffer += decoder.decode(value, { stream: true });

                        // Xử lý các dòng trong buffer
                        const lines = buffer.split('\n');
                        buffer = lines.pop() || ''; // Giữ lại dòng chưa hoàn chỉnh

                        for (const line of lines) {
                            if (line.startsWith('data: ')) {
                                const data = line.slice(6); // Bỏ "data: "

                                if (data === '[DONE]') {
                                    if (onComplete) onComplete();
                                    return;
                                }

                                try {
                                    const parsed = JSON.parse(data);
                                    if (onMessage) onMessage(parsed);
                                } catch (e) {
                                    console.error('Error parsing SSE data:', e);
                                }
                            }
                        }

                        // Tiếp tục đọc
                        readStream();
                    }).catch(error => {
                        if (onError) onError(error);
                    });
                };

                readStream();
            })
            .catch(error => {
                if (onError) onError(error);
            });
    }

    /**
     * Đóng kết nối
     */
    close() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }
}

/**
 * Helper function để gửi chat request với SSE
 * @param {string} message - Tin nhắn từ user
 * @param {string} sessionId - Session ID (optional)
 * @param {Object} callbacks - Callbacks cho các events
 */
export function sendChatMessage(message, sessionId, callbacks) {
    // Sử dụng environment variable cho production, fallback về localhost cho development
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    const client = new SSEClient(`${API_URL}/api/chat`, {
        body: {
            message,
            session_id: sessionId || null,
        },
    });

    client.connect(callbacks);

    return client;
}
