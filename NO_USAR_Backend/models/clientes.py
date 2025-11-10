from sqlalchemy import Column, String, Date, UniqueConstraint
from datetime import date
from sqlalchemy.orm import declarative_base

# Usamos la misma Base que en databases/sqlconect si se importa desde allí.
try:
	from Backend.databases.sqlconect import Base
except Exception:  # fallback si el import relativo falla en algunos entornos
	Base = declarative_base()


class Cliente(Base):
	__tablename__ = "Clientes"

	# Clave primaria compuesta segun el esquema (Nombre, Apellido, DNI)
	Nombre = Column(String, primary_key=True, nullable=False)
	Apellido = Column(String, primary_key=True, nullable=False)
	DNI = Column(String, primary_key=True, nullable=False)

	Telefono = Column(String, nullable=True)
	Email = Column(String, nullable=True)
	# Fecha de registro: por defecto se establece a la fecha actual desde Python
	# Nota: usamos default=date.today (callable) para que SQLAlchemy la asigne al insertar
	# sin requerir cambios en el esquema de la base de datos existente.
	Fecha_Registro = Column(Date, nullable=False, default=date.today)

	# Ejemplo de restricción extra si se desea evitar emails duplicados (opcional)
	__table_args__ = (
		UniqueConstraint("Email", name="uq_clientes_email"),
	)

	def __repr__(self) -> str: # esto sirve para debuggear
		return (
			f"Cliente(Nombre='{self.Nombre}', Apellido='{self.Apellido}', DNI='{self.DNI}', "
			f"Telefono='{self.Telefono}', Email='{self.Email}', Fecha_Registro={self.Fecha_Registro})"
		)

	@property  # property es un decorador que convierte el método en un atributo de solo lectura
	def nombre_completo(self) -> str: # propiedad calculada que devuelve el nombre completo
		return f"{self.Nombre} {self.Apellido}"

