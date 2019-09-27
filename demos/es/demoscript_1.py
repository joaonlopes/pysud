"""
Minidemo para pysud.

Demuestra uso de clase Item y eventos relacionados.
Demuestra uso de salvar y cargar partida.
"""

import pysud_gm as gameMgr
import pysud
import pysud_events as ev

##################################################################
# Items                                                          #
# Heredar de la clase abstracta pysud.Item e implementar use_on()#
##################################################################
class Termo(pysud.Item):
    def use_on(self, game):
        pass

class Mate (pysud.Item):
    def use_on(self, game):
        pass

class Telefono(pysud.Item):
    def __init__(self):
        # La siguiente línea es necesaria si se sobreescribe el
        # constructor de pysud.Item :
        pysud.Item.__init__(self, "telefono", "Un viejo teléfono celular.")
        self.encendido = False
    def use_on(self, game):
        if not self.encendido:
            game.iom.show_message("Enciendes tu teléfono.")
            self.encendido = True
        else:
            game.iom.show_message("Apagas tu teléfono.")
            self.encendido = False


class EsferaAmarilla(pysud.Item):
    pass

class EsferaAzul(pysud.Item):
    pass

class EsferaVerde(pysud.Item):
    pass

##########################
# Eventos Personalizados #
##########################
class CebarUnMate(ev.UseItemWithItemEvent):
    def on_success(self, game):
        game.iom.show_message('Mmmm... te cebas un rico mate...' )

class MirarCajonera(ev.CommandEvent):
    def on_success(self, game):
        if not game.get_user_defined_variable('visto_cajonera'):
            game.set_user_defined_variable('visto_cajonera', True)
            game.iom.show_message('En la cajonera encuentras dos esferas de energía: una amarilla y una azul.')
            am = EsferaAmarilla("esfera amarilla", "Una bonita esfera de energía amarilla...")
            az = EsferaAzul("esfera azul", "Una bonita esfera de energía azul...")
            game.pc.current_room.add_item(am)
            game.pc.current_room.add_item(az)
            game.add_global_event(ev.CombineItemEvent(am, az, EsferaVerde("esfera verde", "Una hermosa esfera de energía verde... parece poderosa...")))
        else:
            game.iom.show_message('No encuentras nada nuevo en la cajonera.')


########
# Main #
########
def gamescript():
    print('pysud minidemo items ...')
    juego = pysud.Game("MiniDemoTester")
    r1 = pysud.Room(
        room_name = "Pequeña habitación",
        room_description = "Esta pequeña habitación de unos 4m cuadrados tiene una cama en un rincón, un escritorio junto a ella y una mesa cuadrada en el centro. También hay un armario empotrado y una cajonera junto a la puerta. \n Un cuadro en un muro lee: 'Los nuevos comandos son agarrar ITEM, usar ITEM, usar ITEM1 con ITEM2, combinar ITEM1 ITEM2, mirar ITEM (de tu inventario), i o inventario (para ver tus cosas), stats para ver donde has estado, puntos para ver tu puntaje, save, load'."
    )
    # agregando items a la habitación:
    t = Termo("termo", "Es un termo Lumilagro, me recuerda a Victor Hugo...")
    m = Mate("mate", "Un mate de lata.")
    cel = Telefono()
    r1.add_item(t)
    r1.add_item(m)
    r1.add_item(cel)
    # agregando eventos locales a la habitación:
    r1.add_local_event(MirarCajonera(["mirar cajonera", "examinar cajonera"]))
    # agregando eventos globales:
    juego.add_global_event(CebarUnMate(t, m))
    juego.set_user_defined_variable('visto_cajonera', False)
    # comenzando:
    juego.add_rooms([r1])
    juego.pc.move_to_room(r1)
    gm = gameMgr.GameManager(juego)
    gm.run_game()

if __name__ == '__main__':
    gamescript()
