/**
 * App Component
 * Root component của ứng dụng
 */
import React from 'react';
import ChatWindow from './components/ChatWindow';
import './index.css';

export default function App() {
    return (
        <div className="app">
            <ChatWindow />
        </div>
    );
}
