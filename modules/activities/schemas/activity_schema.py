from typing import List, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class ActivityVideosResponse(TypedDict):
    video_id: int
    title: str
    description: str
    activity_id: int
    file_key: str

class ActivityVideosFilters(BaseModel):
    activity_id: Optional[int] = None

# Schemas para ActivityPhoto
class ActivityPhotoCreate(BaseModel):
    name: str = Field(..., description="Name of the photo")
    url: str = Field(..., description="URL of the photo")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Vista frontal del monumento",
                "url": "https://example.com/photo1.jpg"
            }
        }

class ActivityPhoto(ActivityPhotoCreate):
    id: int
    activity_id: int

    class Config:
        from_attributes = True

# Schemas para ActivityReview
class ActivityReviewCreate(BaseModel):
    content: str = Field(..., description="Content of the review")

class ActivityReview(ActivityReviewCreate):
    id: int
    activity_id: int

    class Config:
        from_attributes = True

# Schemas para ActivityTip
class ActivityTipCreate(BaseModel):
    tip_type: str = Field(..., description="Type of tip: foodie, weather_clothing, or pro_traveler")
    tip: str = Field(..., description="Content of the tip")

class ActivityTip(ActivityTipCreate):
    id: int
    activity_id: int

    class Config:
        from_attributes = True

class ActivityCreate(BaseModel):
    name: str = Field(..., description="The name of the activity")
    description: str = Field(..., description="The description of the activity")
    location_id: int = Field(..., description="The location of the activity")
    is_active: bool = Field(False, description="Whether the activity is active by default")
    history: str | None = Field(default=None, description="The history of the activity")
    movie: str | None = Field(default=None, description="The movie of the activity")
    clothes: str | None = Field(default=None, description="The clothes of the activity")
    tags: List[str] = Field(default=[], description="Tags to categorize the activity")
    population: int | None = Field(default=None, description="Population of the area where the activity takes place", ge=0)
    title: str | None = Field(default=None, description="Title of the activity")
    category: str | None = Field(default=None, description="Category of the activity")
    city: str | None = Field(default=None, description="City where the activity takes place")
    country_code: str | None = Field(default=None, description="Country code (e.g., JP, US)")
    location_name: str | None = Field(default=None, description="Detailed location description")
    weather: str | None = Field(default=None, description="Weather information")
    entrance: str | None = Field(default=None, description="Entrance information")
    opening_hours: str | None = Field(default=None, description="Opening hours")
    rating: float | None = Field(default=None, description="Rating of the activity", ge=0, le=5)
    foundation_date: str | None = Field(default=None, description="Foundation date")
    price_min: int | None = Field(default=None, description="Minimum price", ge=0)
    price_max: int | None = Field(default=None, description="Maximum price", ge=0)
    
    photos: List[ActivityPhotoCreate] = Field(default=[], description="List of photo objects with name and URL")
    reviews: List[str] = Field(default=[], description="List of review contents")
    foodie_tips: List[str] = Field(default=[], description="List of foodie tips")
    weather_and_clothing_tips: List[str] = Field(default=[], description="List of weather and clothing tips")
    pro_travelers_tips: List[str] = Field(default=[], description="List of pro traveler tips")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Templo Sensoji",
                "description": "El templo budista más antiguo de Tokio, ubicado en el distrito de Asakusa",
                "location_id": 1,
                "is_active": True,
                "history": "Fundado en el año 628, es el templo más antiguo de Tokio y uno de los más visitados",
                "movie": "Aparece en varias películas como 'Lost in Translation'",
                "clothes": "Viste modestamente, cubre hombros y rodillas",
                "tags": [
                    "templo",
                    "budismo", 
                    "cultura tradicional",
                    "asakusa",
                    "historia"
                ],
                "population": 50000,
                "title": "Templo Sensoji - Asakusa",
                "category": "Religioso/Cultural",
                "city": "Tokyo",
                "country_code": "JP",
                "location_name": "2-3-1 Asakusa, Taito City, Tokyo 111-0032, Japón",
                "weather": "Mejor visitarlo en primavera u otoño por el clima agradable",
                "entrance": "Entrada gratuita",
                "opening_hours": "6:00 AM - 5:00 PM",
                "rating": 4.5,
                "foundation_date": "628 d.C.",
                "price_min": 0,
                "price_max": 0,
                "photos": [
                    {
                        "name": "Puerta Kaminarimon",
                        "url": "https://example.com/kaminarimon-gate.jpg"
                    },
                    {
                        "name": "Salon principal del templo",
                        "url": "https://example.com/main-hall.jpg"
                    },
                    {
                        "name": "Pagoda de cinco pisos",
                        "url": "https://example.com/five-story-pagoda.jpg"
                    }
                ],
                "reviews": [
                    "Una experiencia espiritual increíble, el ambiente es muy tranquilo",
                    "Perfecto para aprender sobre la cultura japonesa tradicional",
                    "Las vistas desde la pagoda son espectaculares"
                ],
                "foodie_tips": [
                    "Prueba los ningyo-yaki (pasteles con forma de muñeca) en la calle Nakamise",
                    "No te pierdas el melon pan recién horneado",
                    "Los tempura de las tiendas locales son deliciosos"
                ],
                "weather_and_clothing_tips": [
                    "En verano lleva sombrero y protector solar",
                    "En invierno abrígate bien, puede hacer mucho frío",
                    "Usa zapatos cómodos para caminar por los terrenos del templo"
                ],
                "pro_travelers_tips": [
                    "Visita durante los festivales tradicionales para una experiencia única",
                    "Toma el tren hasta la estación Asakusa para llegar fácilmente",
                    "Compra amuletos omamori como souvenirs auténticos",
                    "Respeta las costumbres locales: inclínate ante el altar principal"
                ]
            }
        }


class ActivityUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    location_id: int | None = None
    is_active: bool | None = None
    history: str | None = None
    movie: str | None = None
    clothes: str | None = None
    tags: List[str] | None = None
    population: int | None = Field(default=None, description="Population of the area where the activity takes place", ge=0)
    title: str | None = None
    category: str | None = None
    city: str | None = None
    country_code: str | None = None
    location_name: str | None = None
    weather: str | None = None
    entrance: str | None = None
    opening_hours: str | None = None
    rating: float | None = Field(default=None, description="Rating of the activity", ge=0, le=5)
    foundation_date: str | None = None
    price_min: int | None = Field(default=None, description="Minimum price", ge=0)
    price_max: int | None = Field(default=None, description="Maximum price", ge=0)


class Activity(BaseModel):
    id: int
    name: str
    description: str
    location_id: int
    is_active: bool
    history: str | None = None
    movie: str | None = None
    clothes: str | None = None
    tags: List[str] = []
    population: int | None = None
    title: str | None = None
    category: str | None = None
    city: str | None = None
    country_code: str | None = None
    location_name: str | None = None
    weather: str | None = None
    entrance: str | None = None
    opening_hours: str | None = None
    rating: float | None = None
    foundation_date: str | None = None
    price_min: int | None = None
    price_max: int | None = None
    
    # Relaciones cargadas
    photos: List[ActivityPhoto] = Field(default=[], description="List of activity photos")
    reviews: List[ActivityReview] = Field(default=[], description="List of activity reviews")
    tips: List[ActivityTip] = Field(default=[], description="List of activity tips")

    class Config:
        from_attributes = True

class ActivityResponse(BaseModel):
    id: int
    name: str
    description: str
    location_id: int
    is_active: bool
    history: str | None = None
    movie: str | None = None
    clothes: str | None = None
    tags: List[str] = []
    population: int | None = None
    title: str | None = None
    category: str | None = None
    city: str | None = None
    country_code: str | None = None
    location_name: str | None = None
    weather: str | None = None
    entrance: str | None = None
    opening_hours: str | None = None
    rating: float | None = None
    foundation_date: str | None = None
    price_min: int | None = None
    price_max: int | None = None
    
    photos: List[ActivityPhoto] = Field(default=[], description="List of activity photos")
    reviews: List[str] = Field(default=[], description="List of review contents")
    foodie_tips: List[str] = Field(default=[], description="List of foodie tips")
    weather_and_clothing_tips: List[str] = Field(default=[], description="List of weather and clothing tips")
    pro_travelers_tips: List[str] = Field(default=[], description="List of pro traveler tips")

    class Config:
        from_attributes = True

class ActivityFilter(BaseModel):
    skip: int = 0
    limit: int = 100
    location_id: Optional[int] = None
    is_active: Optional[bool] = None
    tag: Optional[str] = Field(default=None, description="Search activities by partial tag match")
    min_price: Optional[float] = Field(default=None, description="Minimum price filter", ge=0)
    max_price: Optional[float] = Field(default=None, description="Maximum price filter", ge=0)
    min_population: Optional[int] = Field(default=None, description="Minimum population filter", ge=0)
    max_population: Optional[int] = Field(default=None, description="Maximum population filter", ge=0)
    category: Optional[str] = Field(default=None, description="Filter by category")
    city: Optional[str] = Field(default=None, description="Filter by city")
    country_code: Optional[str] = Field(default=None, description="Filter by country code")
    min_rating: Optional[float] = Field(default=None, description="Minimum rating filter", ge=0, le=5)
    max_rating: Optional[float] = Field(default=None, description="Maximum rating filter", ge=0, le=5)


class VideoCreate(BaseModel):
    title: str = Field(..., description="The title of the video")
    description: str = Field(..., description="The description of the video")

class Video(VideoCreate):
    id: int

    class Config:
        from_attributes = True

class VideoSignedUrlResponse(BaseModel):
    video_id: int = Field(..., description="The ID of the video")
    signed_url: str = Field(..., description="The pre-signed URL to access the video")
    expires_in: int = Field(..., description="The expiration time in seconds")

class VideoUpdate(BaseModel):
    title: str | None = Field(default=None, description="The title of the video")
    description: str | None = Field(default=None, description="The description of the video")
