from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from TreeExceptions import *


class Tree:
    def __init__(self, dof=(None, 0), uof=(None, 0)):
        self.twigs = dict()
        self.dof = dof
        self.uof = uof

    def make_twig(self, name=None, bot=None, user=None):
        if name:
            self.twigs[str(name)] = Twig(str(name), bot=bot if bot and not self.dof[1] else self.dof[0], user=user if user and not self.uof[1] else self.uof[0])
        else:
            self.twigs[str(len(self.twigs))] = Twig(str(len(self.twigs)), bot=bot if bot and not self.dof[1] else self.dof[0], user=user if user and not self.uof[1] else self.uof[0])

    def set_bot(self, bot):
        self.dof[0] = bot
        if self.dof[1]:
            for i in len(self):
                self.twigs[i].bot = bot

    def set_user(self, user):
        self.uof[0] = user
        if self.uof[1]:
            for i in len(self):
                self.twigs[i].set_user(user)

    def __len__(self):
        return len(self.twigs)

    def __getitem__(self, ind):
        try:
            return self.twigs[ind]
        except:
            try:
                return self.twigs[list(self.twigs.keys())[ind]]
            except:
                return None

    def __str__(self):
        return str(self.twigs)
    

class Twig:
    def __init__(self, name, bot, user):
        self.signals = dict()
        self.name = name
        self.bot = bot
        self.user = user
        self.callback_handlers = {}

    def __getitem__(self, ind):
        try:
            return self.signals[ind]
        except:
            try:
                return self.signals[list(self.signals.keys())[ind]]
            except:
                return None

    def __len__(self):
        return len(self.signals)
                 
    def __call__(self, data=None,  ind=0):
        try:
                sig = self.signals[ind]
                n = [i for i in range(len(self[ind])) if self[ind][i](data)]
                if not n:
                    msg = self.bot.send_message(sig[0].chat_id, 'Неверный ввод')
                    self.bot.register_next_step_handler(msg, self, ind=ind)
                else:
                    n = n[0]
                    if sig[n].content_type == 'text':
                        msg = self.bot.send_message(*list(sig[n].params.values()))
                        self.bot.register_next_step_handler(msg, self, ind=ind + 1)
                    elif sig[n].content_type == 'twig':
                        sig[n].params['twig'](ind=0)
        except:
            pass

    def __repr__(self):
        return str(self.signals)

    def __str__(self):
        return str(self.signals)

    def set_bot(self, bot):
        self.bot = bot

    def set_user(self, user):
        if user.isdigi():
            self.user = user
            for i in self.signals:
                for j in self.signals[i]:
                    self.signals[i][j]['chat_id'] = self.user
            return True
        return False

    @staticmethod
    def switch_conditions(leaf1, leaf2):
        leaf1.condition, leaf2.condition = leaf2.condition, leaf1.condition

    @staticmethod
    def switch_keyboards(leaf1, leaf2):
        leaf1.keyboard, leaf2.keyboard = leaf2.keyboard, leaf1.keyboard

    def make_metre(self, cont): # 
        if (not isinstance(cont, Twig)) and (not isinstance(cont, Leaf)):
                return False
        n = len(self) if len(self) > 0 else len(self) + 1
        self.signals[n - 1] = {0: cont}
        self.signals[len(self)] = lambda x: x
        self.callback_handlers[n - 1] = {0: {}}
        if cont.keyboard != None:
            for i, value in enumerate(cont.keyboard.keyboard):
                self.callback_handlers[n - 1][0][i] = self.bot.callback_query_handler(func=lambda x: x == value[0].callback_data)(lambda: self(data=str(value[0].callback_data), ind=n))
        return True

    def replace_metre(self, cont, ind): #
        if ind not in range(len(self)):
            return False
        if (not isinstance(cont, Twig)) and (not isinstance(cont, Leaf)):
                return False
        self.signals[ind] = {0: cont}
        self.callback_handlers[ind] = {0: {}}
        if cont.keyboard != None:
            for i, value in enumerate(cont.keyboard.keyboard):
                self.callback_handlers[n - 1][0][i] = self.bot.callback_query_handler(func=lambda x: x == value[0].callback_data)(lambda: self(data=str(value[0].callback_data), ind=n))
        return True

    def switch_metre(self, switchable, switched): #
        if switchable not in range(len(self)) or switched not in range(len(self)):
            return False
        self.signals[switchable], self.signals[switched] = self.signals[switched], self.signals[switchable]
        return True

    def switch_metre_without_conds(self, switchable, switched): #
        if switchable not in range(len(self)) or switched not in range(len(self)):
            return False
        if len(self[switchable]) != len(self[switched]):
            return False
        for i in range(len(self[switchable])):
            Twig.switch_conditions(self[switchable][i], self[switched][i])
        self.signals[switchable], self.signals[switched] = self.signals[switched], self.signals[switchable]
        return True

    def del_condition(self, ind): #
        if ind not in range(len(self)):
            return False
        if len(self[ind]) != 1:
            return False
        self[ind][0].set_condition(lambda x: True)
        return True

    def set_conditions(self, ind, conditions):
        if ind not in range(len(self)):
            return False
        if len(conditions) != len(self[ind]):
            return False
        if not all([type(i) == type(lambda x: True) for i in conditions]):
            return False
        if any([i('-300') for i in conditions]):
            return False
        for i in range(len(self[ind])):
            self[ind][i].set_condition(condition[i])
        return True

    def set_condition(self, ind, n, condition): #
        if type(condition) != type(lambda x: True):
            return False
        if ind not in range(len(self)):
            return False
        if n not in range(len(self[ind])):
            return False
        if condition('-300'):
            return False
        self[ind][n].set_condition(condition)
        return True

    def switch_conditions_without_metres(self, switchable, switched): #
        if switchable not in range(len(self)) or switched not in range(len(self)):
            return False
        if len(self[switchable]) != len(self[switched]):
            return False
        for i in range(len(self[switchable])):
            Twig.switch_conditions(self[switchable][i], self[switched][i])
        return True


    def switch_conditions_without_leafs(self, ind, switchable, switched):
        if ind not in range(len(self)):
            return False
        if switchable not in range(len(self)) or switched not in range(len(self)):
            return False
        Twig.switch_conditions(self[ind][switchable], self[ind][switched])
        return True

    def replace_leaf(self, cont, ind, n): #
        if ind not in range(len(self)):
            return False
        if n not in range(len(self[ind])):
            return False
        self.signals[ind][n] = cont
        self.callback_handlers[ind][n] = {}
        if cont.keyboard != None:
            for i, value in enumerate(cont.keyboard.keyboard):
                self.callback_handlers[n - 1][n][i] = self.bot.callback_query_handler(func=lambda x: x == value[0].callback_data)(lambda: self(data=str(value[0].callback_data), ind=n))
        return True

    def switch_leaf_without_conds(self, ind, switchable, switched):
        if ind not in range(len(self)):
            return False
        if switchable not in range(len(self)) or switched not in range(len(self)):
            return False
        Twig.switch_conditions(self[ind][switchable], self[ind][switched])
        self.signals[ind][switchable], self.signals[ind][switched] = self.signals[ind][switched], self.signals[ind][switchable]
        return True
    
    def add_leaf(self, cont, ind): #
            if ind not in range(len(self)):
             return False
            if (not isinstance(cont, Twig)) and (not isinstance(cont, Leaf)):
                return False
            n = len(self[ind])
            self.signals[ind][n] = cont
            self.callback_handlers[ind][n] = {}
            if cont.keyboard != None:
                for i, value in enumerate(cont.keyboard.keyboard):
                    self.callback_handlers[ind][n][i] = self.bot.callback_query_handler(func=lambda x: x == value[0].callback_data)(lambda: self(data=str(value[0].callback_data), ind=n))
            return True

    def del_metre(self, ind):
        if ind not in range(len(self)):
            return False
        k = list(self.signals.keys())
        for i in range(ind, len(self) - 1):
            self.signals[k[i]] =  self[k[i + 1]]
        del self.signals[k[-1]]
        return True

    def del_leaf(self, ind, n):
        if ind not in range(len(self)):
            return False
        if n not in range(len(self[ind])):
            return False
        k = list(self[ind].keys())
        for i in range(n, len(self[ind]) - 1):
            self[ind][k[i]] =  self[ind][k[i + 1]]
        del self[ind][k[-1]]
        return True

    def get_leaf(self, ind, n):
        if ind not in range(len(self)):
            return False
        if n not in range(len(self[ind])):
            return False
        return self[ind][n]

    def set_message_handler(self):
        pass

    def set_callback_query_handler(self):
        pass

    def get_connection(self, ind=0):
        cons = ''
        for i in self.signals:
            for j in self[i]:
                cons += f'{i}.{j} -> '
        cons += ' ...'
        return cons


class Leaf:
    def __init__(self, content_type, keyboard=None, condition=lambda x: True):
        if not ((keyboard != None) == (isinstance(keyboard, InlineKeyboardMarkup) or isinstance(keyboard, ReplyKeyboardMarkup))):
            raise TypeError({'Error': {'Type': type(keyboard)}, 'attribute': {'Name': 'keyboard', 'Types': [type(InlineKeyboardMarkup()), type(ReplyKeyboardMarkup())]}})
        if content_type not in ['text', 'photo', 'document']:
            raise TypeError({'Error': {'Type': type(content_type)}, 'attribute': {'Name': 'condition', 'Types': [type('')]}})
        if type(condition) != type(lambda: True):
            raise TypeError({'Error': {'Type': type(condition)}, 'attribute': {'Name': 'condition', 'Types': [type(lambda x: True)]}})
        self.content_type = ''
        self.condition = lambda x: True
        self.keyboard = None
        self.types = {"text": {'chat_id': None, 
                               'text': None, 
                               'parse_mode': None, 
                               'entities': None, 
                               'disable_web_page_preview': None, 
                               'disable_notification': None, 
                               'protect_content': None, 
                               'reply_to_message_id': None, 
                               'allow_sending_without_reply': None, 
                               'reply_markup': None, 
                               'timeout': None, 
                               'message_thread_id': None},
                      "photo": {'chat_id': None,
                                'photo': None,
                                'caption': None,
                                'parse_mode': None,
                                'caption_entities': None,
                                'disable_notification': None,
                                'protect_content': None,
                                'reply_to_message_id': None,
                                'allow_sending_without_reply': None,
                                'reply_markup': None,
                                'timeout': None,
                                'message_thread_id': None,
                                'has_spoiler': None},
                      "document": {'chat_id': None,
                                   'document': None,
                                   'reply_to_message_id': None,
                                   'caption': None,
                                   'reply_markup': None,
                                   'parse_mode': None,
                                   'disable_notification': None,
                                   'timeout': None,
                                   'thumbnail': None,
                                   'caption_entities': None,
                                   'allow_sending_without_reply': None,
                                   'visible_file_name': None,
                                   'disable_content_type_detection': None,
                                   'data': None,
                                   'protect_content': None,
                                   'message_thread_id': None,
                                   'thumb': None},
                      "twig": {'twig': None}}
        self.params = self.types[content_type]

    def __iter__(self):
        return iter(self.params)

    def __str__(self):
        return str(self.params)

    def __repr__(self):
        return f'Lf({str(self)})'

    def check_condition(self, arg):
        return self.condition(arg)

    def set_content_type(self, content_type):
        if content_type not in ['text', 'photo', 'document']:
            raise TypeError({'Error': {'Type': type(content_type)}, 'attribute': {'Name': 'condition', 'Types': [type('')]}})
        self.content_type = content_type
        self.params = self.types[content_type]
        return True

    def set_condition(self, condition):
        if type(condition) != type(lambda: True):
            raise TypeError({'Error': {'Type': type(condition)}, 'attribute': {'Name': 'condition', 'Types': [type(lambda x: True)]}})
        self.condition = condition
        return True

    def set_keyboard(self, keyboard):
        if self.content_type == 'twig':
            raise TypeError({'Error': {'Type': 'twig'}, 'attribute': {'Name': 'keyboard', 'Types': ["'text'", "'photo'", "'document'"]}})
        if not ((keyboard != None) == (isinstance(keyboard, InlineKeyboardMarkup) or isinstance(keyboard, ReplyKeyboardMarkup))):
            raise TypeError({'Error': {'Type': type(keyboard)}, 'attribute': {'Name': 'keyboard', 'Types': [type(InlineKeyboardMarkup()), type(ReplyKeyboardMarkup())]}})
        self.keyboard = keyboard
        return True

    def get_params(self):
        return self.params

    def set_params(self, params: dict):
        if type(params) != dict:
            raise TypeError(f'Wrong type for "params" {type(params)}')
        if list(self.params.keys()) != list(params.keys()):
            raise ConnectionError({'Error': {'Type': ''}, 'attribute': {'Name': 'params', 'Types': ['', '', '']}})
        self.params = params
        return True
