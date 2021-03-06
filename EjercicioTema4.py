from builtins import print
import sqlite3
import pymysql
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

#engine = create_engine('mysql+pymysql://dm2:dm2@localhost/olimpiadas', echo=True)
engine = create_engine('mysql+pymysql://dm2:dm2@localhost/olimpiadas')
engineSqlite = create_engine('sqlite:///Olimpiadas.sqlite')

class Deportista(Base):
   __tablename__ = 'Deportista'

   id_deportista = Column(Integer, primary_key=True)
   nombre = Column(String)
   sexo = Column(String)
   peso = Column(Integer)
   altura = Column(Integer)


class Olimpiada(Base):
   __tablename__ = 'Olimpiada'

   id_olimpiada = Column(Integer, primary_key=True)
   nombre = Column(String)
   anio = Column(String)
   temporada = Column(String)
   ciudad = Column(String)


class Deporte(Base):
   __tablename__ = 'Deporte'

   id_deporte = Column(Integer, primary_key = True)
   nombre = Column(String)


class Equipo(Base):
   __tablename__ = 'Equipo'

   id_equipo = Column(Integer, primary_key = True)
   nombre = Column(String)
   iniciales = Column(String)


class Evento(Base):
   __tablename__ = 'Evento'

   id_evento = Column(Integer, primary_key = True)
   nombre = Column(String)
   id_olimpiada = Column(Integer, ForeignKey('Olimpiada.id_olimpiada'))
   id_deporte = Column(Integer, ForeignKey('Deporte.id_deporte'))
   olimpiada = relationship("Olimpiada", back_populates="eventos")
   deporte = relationship("Deporte", back_populates="eventos")


Olimpiada.eventos = relationship("Evento", order_by = Olimpiada.id_olimpiada, back_populates = "olimpiada")
Deporte.eventos = relationship("Evento", order_by = Deporte.id_deporte, back_populates = "deporte")


class Participacion(Base):
   __tablename__ = 'Participacion'
   id_deportista = Column(Integer, ForeignKey('Deportista.id_deportista'), primary_key=True)
   id_evento = Column(Integer, ForeignKey('Evento.id_evento'), primary_key=True)
   id_equipo = Column(Integer, ForeignKey('Equipo.id_equipo'))
   edad = Column(Integer)
   medalla = Column(String)
   deportista = relationship("Deportista", back_populates="participaciones")
   evento = relationship("Evento", back_populates="participaciones")
   equipo = relationship("Equipo", back_populates="participaciones")


Deportista.participaciones = relationship("Participacion", order_by=Deportista.id_deportista, back_populates="deportista")
Evento.participaciones = relationship("Participacion", order_by=Evento.id_evento, back_populates="evento")
Equipo.participaciones = relationship("Participacion", order_by=Equipo.id_equipo, back_populates="equipo")


class EjercicioTema4:

    @staticmethod
    def listadoDeport():
        """Metodo que lista los deportistas que hayan participado en diferentes deportes"""

        print("""En que BBDD quieres buscar: 1. MySql
                            2. SQLITE""")
        resp = int(input())
        if resp == 1:

            Session = sessionmaker(bind=engine)
            session = Session()

        elif resp == 2:
            Session = sessionmaker(bind=engineSqlite)
            session = Session()


        print("Dime la temporada 'W' o 'S'")
        temp = input()
        if temp == "W" or temp == "w":
            tempo = 'Winter'
        elif temp == "S" or temp == "s":
            tempo = 'Summer'
        else:
            print("Temporada incorrecta")



        result = session.query(Olimpiada).filter(Olimpiada.temporada == tempo)
        for row in result:
                print(str(row.id_olimpiada)+"--"+row.nombre+"--"+row.ciudad)





        print("Seleciona la edicion olimpica")
        edicion = input()


        result = session.query(Evento).filter(Evento.id_olimpiada == edicion).group_by(Evento.id_deporte)

        for row in result:
            print(str(row.deporte.id_deporte) + "--" + row.deporte.nombre)


        print("Seleciona el deporte")
        deporte = input()


        result = session.query(Evento).filter(Evento.id_olimpiada == edicion).filter(Evento.id_deporte == deporte)
        for row in result:
            print(str(row.id_evento) + "--" + row.nombre)


        print("Seleciona el evento")
        evento = [input()]

        result = session.query(Participacion).filter(Participacion.id_evento == evento)

        print(str(result[0].evento.olimpiada.temporada) + "--" + str(result[0].evento.olimpiada.nombre) + "--" +
                str(result[0].evento.deporte.nombre) + "--" + str(result[0].evento.nombre))

        for row in result:

            print(str(row.deportista.nombre) + " -- " + str(row.deportista.altura) + " -- " + str(row.deportista.peso)
                  + " -- " + str(row.edad) + " -- " + str(row.equipo.nombre) + " -- "
                  + str(row.medalla))





    @staticmethod
    def modifiMeda():
        """Metodo que permitirá modificar la información sobre medallas de  un deportista"""

        print("""En que BBDD quieres buscar: 1. MySql
                                    2. SQLITE""")
        resp = int(input())
        if resp == 1:

            Session = sessionmaker(bind=engine)
            session = Session()

        elif resp == 2:
            Session = sessionmaker(bind=engineSqlite)
            session = Session()


        print("Dime nombre del deportista")
        deportis = input()

        if resp == 1:

            result = session.query(Deportista).filter(Deportista.nombre.like("%"+deportis+"%"))
            for row in result:
                print(str(row.id_deportista) + "--" + row.nombre)


        print("Dime el ID del deportista")
        IDdep = int(input())

        result = session.query(Participacion).filter(Participacion.id_deportista == IDdep)
        for row in result:
            print(str(row.evento.id_evento) + "--" + (str(row.evento.nombre)))


        print("Dime el ID del evento")
        IDeven = int(input())

        if resp == 1:

            participacion = session.query(Participacion).filter(Participacion.id_deportista == IDdep)\
                .filter(Participacion.id_evento == IDeven).first()

            print("Su medalla es: "+str(participacion.medalla))

            print("¿Quieres modificarla?")
            resp = input()
            if resp == "s":
                print("Introduzca la nueva medalla")
                nuevaMedalla = input()
                participacion.medalla=nuevaMedalla
                session.commit()

                print("Actualizado")

            else:
                print("Se ha cancelado la actualizacion")


    @staticmethod
    def nuevaParticipacionDeportista():
        """Metodo que añade un deportista si no exite y le asigna una nueva participacion """

        print("""En que BBDD quieres buscar: 1. MySql
                            2. SQLITE""")
        resp = int(input())
        if resp == 1:

            Session = sessionmaker(bind=engine)
            session = Session()

        elif resp == 2:
            Session = sessionmaker(bind=engineSqlite)
            session = Session()

        print("Dime nombre del deportista")
        deportis = input()

        contDeport = session.query(Deportista).filter(Deportista.nombre.like("%" + deportis + "%")).count()


        if contDeport == 0:
            print("No se ha encontrado ningun deportista por lo que se va a crear")

            print("Dime sexo")
            sexo = input()

            print("Dime peso")
            peso = input()

            print("Dime altura")
            altura = input()


            ID = session.query(Deportista).filter(Deportista.id_deportista)

            for row in ID:
                ultimoID=row.id_deportista

            IDdep = ultimoID+1

            nuevoDeportis = Deportista(id_deportista=IDdep, nombre=deportis, sexo=sexo, peso=peso, altura=altura)

            session.add(nuevoDeportis)
            session.commit()

        else:

            result = session.query(Deportista).filter(Deportista.nombre.like("%" + deportis + "%"))
            for row in result:
                print(str(row.id_deportista) + "--" + row.nombre)

            print("Dime el ID del deportista")
            IDdep = int(input())


        print("Dime la temporada 'W' o 'S'")
        temp = input()
        if temp == "W" or temp == "w":
            tempo = 'Winter'
        elif temp == "S" or temp == "s":
            tempo = 'Summer'
        else:
            print("Temporada incorrecta")

        result = session.query(Olimpiada).filter(Olimpiada.temporada == tempo)
        for row in result:
            print(str(row.id_olimpiada) + "--" + row.nombre + "--" + row.ciudad)


        print("Seleciona la edicion olimpica")
        edicion = input()

        result = session.query(Evento).filter(Evento.id_olimpiada == edicion).group_by(Evento.id_deporte)

        for row in result:
            print(str(row.deporte.id_deporte) + "--" + row.deporte.nombre)


        print("Seleciona el deporte")
        deporte = input()

        result = session.query(Evento).filter(Evento.id_olimpiada == edicion).filter(Evento.id_deporte == deporte)
        for row in result:
            print(str(row.id_evento) + "--" + row.nombre)

        print("Seleciona el evento")
        IDEvento = int(input())


        print("Dime la medalla")
        medalla = input()

        nuevaParti = Participacion(id_deportista=IDdep, id_evento=IDEvento, id_equipo=1, edad=0, medalla=medalla)

        session.add(nuevaParti)
        session.commit()

    @staticmethod
    def eliminarPart():
        """Metodo que elimina una participacion de un deportista """

        print("""En que BBDD quieres buscar: 1. MySql
                            2. SQLITE""")
        resp = int(input())
        if resp == 1:

            Session = sessionmaker(bind=engine)
            session = Session()


        elif resp == 2:
            Session = sessionmaker(bind=engineSqlite)
            session = Session()



        print("Dime nombre del deportista")
        deportis=input()

        result = session.query(Deportista).filter(Deportista.nombre.like("%" + deportis + "%"))
        for row in result:
            print(str(row.id_deportista) + "--" + row.nombre)


        print("Dime el ID del deportista")
        IDdep = int(input())

        result = session.query(Participacion).filter(Participacion.id_deportista==IDdep)
        for row in result:
            print(str(row.evento.id_evento) + "--" + row.evento.nombre)


        print("Dime el ID del evento")
        IDeven = int(input())

        contPart = session.query(Participacion).filter(Participacion.id_deportista == IDdep).count()


        if contPart > 1:
            print("Se va a proceder a borrar solo la participacion")
            session.query(Participacion).filter(Participacion.id_deportista == IDdep).filter(
                Participacion.id_evento == IDeven).delete()
            session.commit()
            print("Borrada")

        else:
            print("Se va a proceder a borrar el deportista y la participacion")
            session.query(Participacion).filter(Participacion.id_deportista == IDdep).filter(
                Participacion.id_evento == IDeven).delete()

            session.query(Deportista).filter(Deportista.id_deportista == IDdep).delete()
            session.commit()
            print("Borrado")



    @staticmethod
    def menu():
        """Metodo para la ejecucion del menu del programa"""

        resp = 9
        while (resp != 0):
            print("""
   1. Listado de deportistas participantes
   2. Modificar medalla deportista
   3. Añadir deportista/participación
   4. Eliminar participación

   0. Salir""")

            resp = int(input())
            Tema4 = EjercicioTema4()
            if (resp == 1):
                Tema4.listadoDeport()

            elif (resp == 2):
                Tema4.modifiMeda()

            elif (resp == 3):
                Tema4.nuevaParticipacionDeportista()

            elif (resp == 4):
                Tema4.eliminarPart()




Tema4 = EjercicioTema4()
Tema4.menu()
