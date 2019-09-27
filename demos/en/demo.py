"""
English language pysud demo

Shows user defined items and events
"""

import pysud_gm as gameMgr
import pysud_events as ev
import pysud

# USER DEFINED EVENT
class EventCabinet(ev.CommandEvent):
    def on_success(self, game):
        myflag = game.get_user_defined_variable('cabinet_opened')
        if not myflag:
            game.set_user_defined_variable('cabinet_opened', True)
            game.iom.show_message("When you open the cabinet you find a medicinal alcohol bottle, almost full, and some bandages, you decide to take'em with you...")
            game.pc.increase_score(1)
            game.set_user_defined_variable('use_alcohol', False)
             # An event success may create a new event:
            game.add_global_event(EventAlcohol(['use alcohol']))
        else:
            game.iom.show_message("You already check there...")


class EventMeetMen(ev.CommandEvent):
    def on_success(self, game):
        myflag = game.get_user_defined_variable('check_men')
        if not myflag:
            game.set_user_defined_variable('check_men', True)
            game.iom.show_message("The man has some serious deep wounds, like bite marks along his face and both arms. In his pocket, you find a lighter.")
            game.pc.increase_score(1)
        else:
            game.iom.show_message("He's not carrying anything else...")


class EventEndingBad(ev.CommandEvent):
    def on_success(self, game):
        game.iom.show_message('When you open the door, one of the employees of the place turns around: his face is covered with blood and his eyes are completely white, he does not speak, yet barely breathing he emits sounds of agony while walking towards you with clumsy movements. Fear prevents you to react and pounces on you ... the last thing you see is another food trailer employee not very far from you, stiff on the ground over a pool of blood')
        game.iom.show_message("And so, the story of " + game.pc.get_name() + " ends. Her score was:")
        game.iom.show_score()
        game.quit_game()


class EventAlcohol(ev.CommandEvent):
    def on_success(self, game):
        myflag = game.get_user_defined_variable('use_alcohol')
        if not myflag:
            game.set_user_defined_variable('use_alcohol', True)
            game.iom.show_message("With the bandages and the alcohol bottle you manage to craft a sort of home made bomb... wow")
            game.pc.increase_score(1)
        else:
            game.iom.show_message("Your bomb is ready...")


class EventEndingGood(ev.CommandEvent):
    def on_success(self, game) :
        lighter = game.get_user_defined_variable('men')
        bomb = game.get_user_defined_variable('use_alcohol')
        if lighter and bomb:
            game.pc.increase_score(1)
            game.iom.show_message("You light the bandages with the lighter and after opening the door you throw your homemade bomb at that strange creature, which escapes running awkwardly a short distance to fall to writhe in pain, you are not sure that it is actually dead, but at least you do not feel helpless .")
            game.iom.show_message("And so, the story of " + game.pc.get_name() + " ends. Her score was:")
            game.iom.show_score()
            game.quit_game()
        else:
            game.iom.show_message("You may be missed out something...")


if __name__ == '__main__':
    # 1 - initializations:
    PLAYER_NAME = input ('Enter your character name:')
    GAME = pysud.Game(PLAYER_NAME)
    # 2 - rooms definitions:
    R1 = pysud.Room('Street', 'You stand by the doorstep of your old apartment. In the street the sun is falling and you don\'t see people anywhere, everything is absolutely silent... far to the north is the won square...', "1")
    R2 = pysud.Room('Home', 'Your humble apartment has seen better times, that is of course before you lived in it, much earlier. It is small and you have accumulated dirty clothes and garbage everywhere. So many cobwebs in the windows prevent you from seeing clearly what is happening on the street. You left the bathroom door opened, again...', "2")
    R3 = pysud.Room('Bathroom', 'The bathroom decoration is in tune with the rest of your home: gross. Under the sink there\'s a small medicine cabinet and behind you is the main and only bedroom of your apartment...', "3")
    R4 = pysud.Room('Park', 'The square is deserted. It has a path that crosses it through the center from north to south and in the middle of it you see a men lying down. To the south is the street that leads to your home, and in the other direction the only food stand in the park.', "4")
    R5 = pysud.Room('Foodstand', 'At the food stand the tables have been thrown to the floor as if serious disturbances had taken place, there are some blood stains on the floor, and especially near the door that leads where the food is prepared. It is ajar. You hear strange noises coming from inside...', "5")
    # 3 - rooms transicions -connect rooms-:
    R1.add_transition(['go home', 'enter home'], R2)
    R2.add_transition(['go outside', 'leave'], R1)
    R2.add_transition(['go to bathroom', 'enter bathroom'], R3)
    R3.add_transition(['go to living room', 'go back', 'back', 'go home'], R2)
    R1.add_transition(['go to park', 'north', 'n'], R4)
    R4.add_transition(['south', 'go to street', 's'], R1)  
    R4.add_transition(['north', 'n', 'follow road', 'go to stand'], R5)
    R5.add_transition(['s', 'park', 'south'], R4)
    # 4 - local events and related variables:
    GAME.set_user_defined_variable('cabinet_opened', False)
    R3.add_local_event(EventCabinet(commands = ['open', 'open cabinet']))
    GAME.set_user_defined_variable('check_men', False)
    R4.add_local_event(EventMeetMen(commands = ['look men', 'examine men']))
    R5.add_local_event(
        ev.ShowMessageEvent(
            ['look food stand', 'examine food stand', 'look stand', 'check stand'],
            'As soon as you lean your head to check the inside of the trailer you can see, a few steps from you, the back of one of the employees of the place. Crouched next to his coworker who lies in a pool of blood... He seems to be chewing an arm...')
    )
    R5.add_local_event(EventEndingBad(['enter']))
    R5.add_local_event(EventEndingGood(['throw bomb', 'use bomb']))
    # 5 - add rooms to game instance:
    GAME.add_rooms( [R1, R2, R3, R4, R5] )
    # 6 - run the game demo:
    GAME.pc.move_to_room(R1)
    GAME_MANAGER = gameMgr.GameManager(GAME)
    GAME_MANAGER.run_game()
