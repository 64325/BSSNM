import ba, _ba

aliases = ['invis']
description = 'невидимость'

using_players_ids = True
timer_compatible = True

def extract_args(client_id, account_id, command):
    return True

def run_command(client_id, account_id, type, command_keys, player):
    set_invisible(player)

def set_invisible(cl_id):
    activity = ba.getactivity()
    for player in activity.players:
        if player.sessionplayer.inputdevice.client_id == cl_id:
            if player.actor and player.actor.node:
                if hasattr(player.actor, 'invisible') and player.actor.invisible:
                    set_character(player.actor, player.character)
                    player.actor._add_effects()
                    player.actor.node.name = player.getname()
                else:
                    player.actor.invisible = True
                    player.actor.node.head_model = None
                    player.actor.node.torso_model = None
                    player.actor.node.pelvis_model = None
                    player.actor.node.upper_arm_model = None
                    player.actor.node.forearm_model = None
                    player.actor.node.hand_model = None
                    player.actor.node.upper_leg_model = None
                    player.actor.node.lower_leg_model = None
                    player.actor.node.toes_model = None
                    player.actor.node.style = 'agent'
                    player.actor.remove_tag()
                    player.actor.remove_ranktag()
                    player.actor.remove_rgb()
                    player.actor.particle_spawner = None
                    player.actor.node.name = ''


def set_character(actor, character):
        from bastd.actor.spazfactory import SpazFactory
        actor.invisible = False
        factory = SpazFactory.get()
        media = factory.get_media(character)
        for attr in media:
            setattr(actor.node, attr, media[attr])