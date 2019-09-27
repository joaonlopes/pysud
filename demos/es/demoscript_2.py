"""
Minidemo (usando pysud_make) para pysud.

Demuestra uso de carga de datos generados por pysud_make.py
"""

import pysud_gm as gameMgr
import pysud
import pysud_events as ev

# Fichero de datos de juego creado con pysud_make:
DATAFILE = 'game.data'

##################################################################
# Items                                                          #
# Heredar de la clase abstracta pysud.Item e implementar use_on()#
##################################################################

class LlaveDeTrampilla(pysud.Item):
    def __init__(self):
        pysud.Item.__init__(self, "llave", "Una pequeña llave de hierro.")
    def use_on(self, game):
        my_flag = game.pc.current_room == game.get_room_by_id('5')
        if my_flag:
            game.set_user_defined_variable('trampilla_abierta', True)
            game.iom.show_message("Abres la trampilla con la pequeña llave. Ya no la necesitarás.")
            game.remove_item_from_player(self)
        else:
            game.iom.show_message("No creo que sea el lugar indicado para usar esta llave.")

class Mazo(pysud.Item):
    def __init__(self):
        pysud.Item.__init__(self, "mazo", "Una pesada maza de madera con cabeza de metal.")
    def use_on(self, game):
            jugador_en_bosque = game.pc.current_room == game.get_room_by_id('2')
            my_flag = game.get_user_defined_variable('jarro_destruido')
            if jugador_en_bosque:
                if not my_flag:
                    game.iom.show_message("Golpeas con tu mazo el jarro abriendole un gran hueco.")
                    game.set_user_defined_variable('jarro_destruido', True)
                else:
                    game.iom.show_message("Ya no necesitas seguir castigando al pobre jarro.")
            else:
                game.iom.show_message("No se te ocurre que cosa deberías machacar...")

##################################################################
# Eventos Personalizados                                         #
# Normalmente heredan de alguna subclase de events.Event e       #
# implementan el método on_success(game)                         #
##################################################################
class RevisarJarro(ev.CommandEvent):
    """ Revisar el jarro que se encuentra en el bosque. """
    def on_success(self, game):
        my_flag = game.get_user_defined_variable('jarro_destruido')
        if my_flag:
            game.iom.show_message("Extiendes la mano a través del hueco para revisar dentro del jarro y encuentras una pequeña llave.")
            # se agrega directamente la llave al inventario del personaje:
            game.add_item_to_player(LlaveDeTrampilla())
            # NOTA: un objeto agregado de esta forma al inventario no
            # suma puntos automáticamente:
            game.pc.increase_score(1)
            game.set_user_defined_variable('jarro_destruido', True)
        else:
            game.iom.show_message("Un gran jarro de arcilla, la tapa parece estar sellada.")

class RevisarEstante(ev.CommandEvent):
    """ Revisar el estante de armas del puesto de guardia. """
    def on_success(self, game):
        my_flag = game.get_user_defined_variable('estante_revisado')
        if not my_flag:
            mazo = Mazo()
            game.pc.current_room.add_item(mazo)
            game.iom.show_message("En el estante de armas solo queda un mazo en buen estado.")
            game.set_user_defined_variable('estante_revisado', True)
        else:
            game.iom.show_message("No encuentras nada nuevo.")

class SubirEscalera(ev.CommandEvent):
    """ Subir por la escalera con trampilla de la habitacion 5. """
    def on_success(self, game):
        my_flag = game.get_user_defined_variable('trampilla_abierta')
        if my_flag:
            game.iom.show_message("Pasas por la trampilla abierta y subes al siguiente piso.")
            destination_room = game.get_room_by_id('6')
            game.pc.move_to_room(destination_room)
            game.iom.show_current_room()
            game.iom.show_message("Has completado esta demo, espero haya sido de tu agrado.")
        else:
            game.iom.show_message("Una trampilla cerrada te impide ascender al siguiente piso.")
########
# Main #
########
def gamescript():
    print('pysud minidemo pysud_make ...\n')
    JUEGO = pysud.Game("")
    GM = gameMgr.GameManager(JUEGO)
    # usar GM para cargar los datos de un nuevo juego:
    GM.load_game_data(DATAFILE)
    # una vez hecho esto, el juego ya no esta en la
    #   variable JUEGO sino en GM.game
    # agregar eventos globales / este script no usa:
    # agregar variables definidas por el usuario:
    GM.game.set_user_defined_variable('estante_revisado' , False)
    GM.game.set_user_defined_variable('trampilla_abierta', False)
    GM.game.set_user_defined_variable('jarro_destruido'  , False)
    # recolectar habitaciones del juego (solamente las necesarias):
    ROOM1 = GM.game.get_room_by_id('1')
    ROOM2 = GM.game.get_room_by_id('2')
    ROOM4 = GM.game.get_room_by_id('4')
    ROOM5 = GM.game.get_room_by_id('5')
    # agregar eventos locales a las habitaciones:
    LE1 = RevisarEstante(commands = ['mirar estante','revisar estante','ver estante'])
    ROOM4.add_local_event(LE1)
    LE2 = RevisarJarro  (commands = ['mirar jarro', 'examinar jarro', 'ver jarro'])
    ROOM2.add_local_event(LE2)
    LE3 = SubirEscalera (commands = ['subir escalera','subir'])
    ROOM5.add_local_event(LE3)
    # Poner al personaje en el escenario inicial:
    GM.game.pc.move_to_room(ROOM1)
    # Mostrar algunos mensajes:
    GM.game.iom.show_welcome_message()
    GM.game.iom.show_help()
    # Iniciar el juego:
    GM.run_game()

if __name__ == '__main__':
    GM = gamescript()
