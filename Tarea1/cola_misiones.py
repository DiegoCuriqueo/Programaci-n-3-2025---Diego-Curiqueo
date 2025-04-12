from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Mision, Personaje, MisionPersonaje

class MissionQueue:
    def __init__(self, personaje_id: int, db: Session):
        self.personaje_id = personaje_id
        self.db = db

    def enqueue(self, mision_id: int): #Aceptar Mision
        total_misiones = self.db.query(MisionPersonaje).filter_by(personaje_id=self.personaje_id).count()
        relacion = MisionPersonaje(personaje_id=self.personaje_id, mision_id=mision_id, orden=total_misiones)
        mision = self.db.query(Mision).get(mision_id)
        if mision.estado == 'completada':
            raise HTTPException(status_code=400, detail="Esta misión ya ha sido completada.")        
        self.db.add(relacion)
        self.db.commit()

    def dequeue(self): #Completar Mision
        relacion = self.db.query(MisionPersonaje).filter_by(personaje_id=self.personaje_id).order_by(MisionPersonaje.orden).first()
        if not relacion:
            raise HTTPException(status_code=404, detail="No hay misiones para completar.")
        mision = self.db.query(Mision).get(relacion.mision_id)
        personaje = self.db.query(Personaje).get(self.personaje_id)
        personaje.experiencia += mision.experiencia
        mision.estado = "completada"
        self.db.delete(relacion)
        self.db.commit()
        return mision

    def first(self):
        relacion = self.db.query(MisionPersonaje).filter_by(personaje_id=self.personaje_id).order_by(MisionPersonaje.orden).first()
        if not relacion:
            return None
        return self.db.query(Mision).get(relacion.mision_id)

    def is_empty(self):
        return self.db.query(MisionPersonaje).filter_by(personaje_id=self.personaje_id).count() == 0

    def size(self):
        return self.db.query(MisionPersonaje).filter_by(personaje_id=self.personaje_id).count()

    def listar(self):
        relaciones = self.db.query(MisionPersonaje).filter_by(personaje_id=self.personaje_id).order_by(MisionPersonaje.orden).all()
        misiones = []
        for r in relaciones:
            mision = self.db.query(Mision).get(r.mision_id)
            misiones.append({"id": mision.id, "nombre": mision.nombre, "estado": mision.estado, "orden": r.orden})
        return misiones