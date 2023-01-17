import random
import settings

logger = settings.logging.getLogger(__name__)

vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)

def text_to_owo(text):
    """ Convierte el texto a OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')

    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

    for v in vowels:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

    return text


async def load_videocmds(bot):
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    for extension_file in settings.VIDEOCMDS_DIR.glob("*.py"):
        if extension_file.name != "__init__.py" and not extension_file.name.startswith("_"):
            await bot.load_extension(f"{settings.VIDEOCMDS_DIR.name}.{extension_file.name[:-3]}")
            logger.debug(f"Loadded CMD: {extension_file.name}")