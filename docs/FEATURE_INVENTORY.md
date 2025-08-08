# Feature Inventory

| Feature | File | Lines | Notes |
|---|---|---|---|
| Profile update adapter | `profile_adapter.py` | 14-38 | Calls `/users/me` when backend enabled; stubbed response otherwise. |
| System status adapter | `system_status_adapter.py` | 17-29 | Attempts to fetch `/status`; returns `None` if offline. |
| Chat interface echo | `chat_ui.py` | 75-80 | Uses simple echo because chat backend endpoints are missing. |
| Video chat manager | `realtime_comm/video_chat.py` | 82-88, 96-101 | WebRTC negotiation and voice send are placeholder stubs. |

The backend app in `backend/app.py` currently omits endpoints such as `/users/me`, `/status`, `/ws/video`, and `/api/chat/*`, so the related features fall back to stub implementations or simplified behaviors.

