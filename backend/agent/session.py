import uuid

class SessionStore:
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id: str | None):
        if session_id is None or session_id not in self.sessions:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = []
        return session_id, self.sessions[session_id]

    def append(self, session_id: str, role: str, content: str):
        self.sessions[session_id].append({
            "role": role,
            "content": content
        })
