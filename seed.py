import logging
from db.session import SessionLocal
from modules.trips.models.trip import Location
from modules.activities.models.activity import Activity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data():
    db = SessionLocal()
    try:
        # --- 1. Verificar si ya existe una ubicación de prueba ---
        test_location = db.query(Location).filter(Location.nickname == "Test Location").first()

        if not test_location:
            logger.info("Creando ubicación de prueba...")
            test_location = Location(
                country="Pruebalandia",
                city="Testburgo",
                nickname="Test Location",
                flag_url="http://example.com/flag.png"
            )
            db.add(test_location)
            db.commit()
            db.refresh(test_location)
            logger.info(f"Ubicación de prueba creada con ID: {test_location.id}")
        else:
            logger.info(f"Ubicación de prueba ya existe con ID: {test_location.id}")

        # --- 2. Crear una actividad usando el ID de la ubicación ---
        logger.info("Creando actividad de prueba...")
        
        # Verificar si la actividad ya existe para no duplicarla
        test_activity = db.query(Activity).filter(Activity.name == "Visita a la Plaza de Pruebas").first()

        if not test_activity:
            new_activity = Activity(
                name="Visita a la Plaza de Pruebas",
                description="Un recorrido para probar la creación de actividades.",
                location_id=test_location.id,  # <- Usamos el ID de la ubicación creada
                is_active=True,
                history="Fundada en 2024 por un desarrollador.",
                tip="No olvidar el café.",
                movie="Buscando al Programador Perdido",
                clothes="Ropa cómoda de oficina"
            )
            db.add(new_activity)
            db.commit()
            logger.info("Actividad de prueba creada exitosamente.")
        else:
            logger.info("La actividad de prueba ya existe.")

        logger.info("Proceso de seeding finalizado.")

    finally:
        db.close()

if __name__ == "__main__":
    logger.info("Iniciando el proceso de seeding de datos de prueba...")
    seed_data() 