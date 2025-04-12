from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Personaje, Mision
from database import crear_base_datos, get_db
from cola_misiones import MissionQueue

app = FastAPI()

# Crear la base de datos si no existe
crear_base_datos()

# -------------------- PERSONAJES --------------------
@app.post("/personajes")
def crear_personaje(nombre: str, db: Session = Depends(get_db)):
    personaje = Personaje(nombre=nombre)
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    return personaje

# -------------------- MISIONES --------------------
@app.post("/misiones")
def crear_mision(nombre: str, descripcion: str = "", experiencia: int = 10, db: Session = Depends(get_db)):
    mision = Mision(nombre=nombre, descripcion=descripcion, experiencia=experiencia, estado="pendiente")
    db.add(mision)
    db.commit()
    db.refresh(mision)
    return mision

# -------------------- ACEPTAR MISION (Encolar) --------------------
@app.post("/personajes/{id_personaje}/misiones/{id_mision}")
def aceptar_mision(id_personaje: int, id_mision: int, db: Session = Depends(get_db)):
    cola = MissionQueue(id_personaje, db)
    cola.enqueue(id_mision)
    return {"mensaje": "Misión encolada correctamente."}

# -------------------- COMPLETAR MISION (Desencolar) --------------------
@app.post("/personajes/{id_personaje}/completar")
def completar_mision(id_personaje: int, db: Session = Depends(get_db)):
    cola = MissionQueue(id_personaje, db)
    mision = cola.dequeue()
    personaje = db.query(Personaje).get(id_personaje)
    return {"mensaje": f"Misión '{mision.nombre}' completada.", "xp_total": personaje.experiencia}

# -------------------- LISTAR MISIONES DEL PERSONAJE --------------------
@app.get("/personajes/{id_personaje}/misiones")
def listar_misiones(id_personaje: int, db: Session = Depends(get_db)):
    cola = MissionQueue(id_personaje, db)
    return cola.listar()
