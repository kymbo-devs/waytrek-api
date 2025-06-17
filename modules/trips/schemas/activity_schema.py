from typing_extensions import TypedDict


class ActivityVideosResponse(TypedDict):
    video_id: int
    title: str
    description: str
    activity_id: int
    file_key: str