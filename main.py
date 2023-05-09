import os
import json
from re import M

def read_config():
    with open("./config.json") as f:
        config = json.load(f)
    return config


def build_world():
    config = read_config()

    if not os.path.exists("ZeroTierOne"):
        os.system("git clone https://github.com/zerotier/ZeroTierOne --depth=1")

    for node_config in config:
        identity = node_config["identity"]
        text = "\n\n\n"
        text += '\troots.push_back(World::Root());\n'
        text += f'\troots.back().identity = Identity("{identity}");\n'

        for end in node_config["stableEndpoints"]:
            text += f'\troots.back().stableEndpoints.push_back(InetAddress("{end}"));\n'

    with open("./mkworld_template.cpp") as cpp:
        world = "".join(cpp.readlines())
        world = world.replace("FIXME: PLACEHOLDER", text)

    # with open("./mkworld_tmp.cpp", "w") as tmp:
    #     tmp.write(world)

    with open("./ZeroTierOne/attic/world/mkworld.cpp", "w") as cpp:
        cpp.write(world)
    

    os.system(f"cd ./ZeroTierOne/attic/world; sh ./build.sh; ./mkworld; mv world.bin {os.getcwd()}/planet; cd -")

if __name__ == '__main__':
    build_world()
