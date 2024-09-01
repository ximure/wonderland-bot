from enum import Enum


class MessageType(Enum):
    TEXT = "text"
    STICKER = "sticker"
    VOICE = "voice"
    VIDEO_NOTE = "video_note"
    PHOTO = "photo"
    AUDIO = "audio"
    DOCUMENT = "document"
    REPLY = "reply"
    FORWARD = "forward"
    OTHER = "other"
