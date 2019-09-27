"""
Primer demo para pysud.

Demuestra uso de eventos locales creados por el usuario.
Demuestra uso de variables definidas por el usuario.
"""

import pysud_gm as gameMgr
import pysud_events as ev
import pysud

# EVENTOS DEFINIDOS POR UN USUARIO:
class EventBotiquin(ev.CommandEvent):
    def on_success(self, game):
        myflag = game.get_user_defined_variable('botiquin_abierto')
        if not myflag:
            game.set_user_defined_variable('botiquin_abierto', True)
            game.iom.show_message("Al abrir el botiquín encuentras una botella de alcohol medicinal casi llena y unas gasas, decides llevártelas...")
            game.pc.increase_score(1)
            game.set_user_defined_variable('use_alcohol', False)
             # Vemos como un evento puede habilitar a otro:
            game.add_global_event(EventAlcohol(['usar alcohol']))
        else:
            game.iom.show_message("Ya has revisado eso.")


class EventHombre(ev.CommandEvent):
    def on_success(self, game):
        myflag = game.get_user_defined_variable('hombre')
        if not myflag:
            game.set_user_defined_variable('hombre', True)
            game.iom.show_message("El hombre tiene varias heridas profundas, como de mordeduras, en el rostro y ambos brazos. En el bolsillo de su camisa encuentras un encendedor.")
            game.pc.increase_score(1)
        else:
            game.iom.show_message("Ya no tiene nada más...")


class EventFinalMalo(ev.CommandEvent):
    def on_success(self, game):
        game.iom.show_message("Al abrir la puerta uno de los empleados del lugar se da vuelta, su cara esta cubierta de sangre y tiene los ojos completamente blancos, no habla, sino que emite unos quijidos de dolor y camina hacia ti con movimientos torpes, pero el miedo te impide reaccionar y se abalanza sobre vos... lo último que logras ver es al otro empleado del lugar a unos pocos metros tuyo, tieso en el suelo sobre un charco de sangre...\n")
        game.iom.show_message("Así termina la historia de " + game.pc.get_name() + " con un puntaje de:")
        game.iom.show_score()
        game.quit_game()


class EventAlcohol(ev.CommandEvent):
    def on_success(self, game):
        myflag = game.get_user_defined_variable('use_alcohol')
        if not myflag:
            game.set_user_defined_variable('use_alcohol', True)
            game.iom.show_message("Con las gasas y la botella de alcohol te fabricas una suerte de bomba casera... guau!")
            game.pc.increase_score(1)
        else:
            game.iom.show_message("Ya tienes tu bomba lista para usar...")


class EventFinalBueno(ev.CommandEvent):
    def on_success(self, game) :
        encendedor = game.get_user_defined_variable('hombre')
        bomba = game.get_user_defined_variable('use_alcohol')
        if encendedor and bomba:
            game.pc.increase_score(1)
            game.iom.show_message("Enciendes las gasas con el encendedor y tras abrir la puerta del puesto de comida arrojas tu bomba casera a aquella extraña criatura, la cual escapa corriendo torpemente unos pocos metros hasta caer a retorcerse de dolor, no estás seguro de que esté muerta, pero al menos no te sientes indefenso.")
            game.iom.show_message("Así termina la historia de " + game.pc.get_name() + " con un puntaje de:")
            game.iom.show_score()
            game.quit_game()
        else:
            game.iom.show_message("Te está faltando algo... ¿pero qué será?")


if __name__ == '__main__':
    # 1 - Inicializaciones:
    NOMBRE_USUARIO = input ('Ingrese nombre de personaje:')
    JUEGO = pysud.Game(NOMBRE_USUARIO)
    # 2 - Habitaciones:
    R1 = pysud.Room('Calle', 'Estas en la puerta de tu viejo departamento. En la calle esta cayendo el sol y no ves personas por ningún lado, todo está en absoluto silencio... hacia el norte está la plaza del barrio...', "1")
    R2 = pysud.Room('Casa', 'Tu humilde departamento ha visto mejores épocas, eso es por supuesto antes de que vivieras en él, mucho antes. Es pequeño y has acumulado ropa sucia y basura por doquier. Tantas telarañas en las ventanas te impiden ver con claridad lo que sucede en la calle. Has dejado la puerta del baño abierta...', "2")
    R3 = pysud.Room('Baño', 'El baño lo tienes a tono con la decoración del resto de tu hogar: mugriento a más no poder. Bajo el lavamanos se encuentra un pequeño botiquín y detras tuyo está la habitación principal (y única) de tu departamento...', "3")
    R4 = pysud.Room('Plaza', 'La plaza está desierta; tiene un camino que la atraviesa por el centro de norte a sur y en medio de este ves a un hombre tirado, boca abajo. Hacia el sur está la calle que conduce a tu hogar, y en la otra dirección el único puesto de comida del parque.', "4")
    R5 = pysud.Room('Puesto de comida', 'En el puesto de comida las mesas se han tirado al piso como si hubieran tenido lugar serios disturbios, hay algunas manchas de sangre por el suelo, y especialmente cerca de la entrada a la casilla donde se prepara la comida rápida, la puerta de la misma está entreabierta. Se oyen ruidos extraños que vienen desde adentro...', "5")
    # 3 - Transiciones (conectando habitaciones):
    R1.add_transition(['ir a casa', 'ir a departamento'], R2)
    R2.add_transition(['ir a calle', 'ir afuera'], R1)
    R2.add_transition(['ir a baño', 'ir al baño'], R3)
    R3.add_transition(['ir a living', 'ir al living', 'atras', 'ir a casa', 'ir a sala'], R2)
    R1.add_transition(['ir a plaza', 'norte', 'n'], R4)
    R4.add_transition(['sur', 'ir a calle', 's'], R1)  
    R4.add_transition(['norte', 'n', 'seguir camino', 'ir a puesto'], R5)
    R5.add_transition(['s', 'plaza', 'sur'], R4)
    # 4 - Eventos locales y variables relacionadas:
    JUEGO.set_user_defined_variable('botiquin_abierto', False)
    R3.add_local_event(EventBotiquin(commands = ['abrir botiquin']))
    JUEGO.set_user_defined_variable('hombre', False)
    R4.add_local_event(EventHombre(commands = ['mirar hombre']))
    R5.add_local_event(
        ev.ShowMessageEvent(
            ['mirar casilla', 'examinar casilla', 'mirar puesto', 'examinar puesto'],
            'Asomas la cabeza dentro de la casilla y puedes ver a unos pocos metros tuyo la espalda de uno de los empleados del lugar, agachado junto a su compañero de trabajo quien yace en un charco de sangre... Pareciera estar masticándole un brazo...' )
    )
    R5.add_local_event(EventFinalMalo(['entrar', 'entrar a casilla', 'ir a casilla']))
    R5.add_local_event(EventFinalBueno(['tirar bomba', 'usar bomba']))
    # 5 - Se agregan las habitaciones al juego:
    JUEGO.add_rooms( [R1, R2, R3, R4, R5] )
    # 6 - Por último comenzar el juego:
    JUEGO.pc.move_to_room(R1)
    GAME_MANAGER = gameMgr.GameManager(JUEGO)
    GAME_MANAGER.run_game()
